# -*- coding: utf-8 -*-
"""
KI-Matching: Findet passende Professionals basierend auf Kundenanfragen
"""
import asyncio
import uuid
try:
    from emergentintegrations.llm.openai import LlmChat, UserMessage
except ImportError:
    LlmChat = None
    UserMessage = None
from .professional_models import Professional, PROFESSIONAL_TYPES, REGIONS

EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"


def get_active_professionals():
    """Holt alle aktiven, verifizierten Professionals"""
    return Professional.objects.filter(
        is_verified=True,
        is_active=True
    ).select_related()


async def _analyze_request_async(anfrage, language, session_id):
    """Analysiert die Kundenanfrage und extrahiert Kriterien"""
    
    lang_map = {'ge': 'Deutsch', 'de': 'Deutsch', 'hr': 'Kroatisch', 'en': 'Englisch'}
    lang_name = lang_map.get(language, 'Deutsch')
    
    prompt = f"""Analysiere diese Kundenanfrage und extrahiere die wichtigsten Informationen.

ANFRAGE: {anfrage}

Antworte NUR im folgenden JSON-Format (keine anderen Texte):
{{
    "berufsgruppe": "real_estate_agent|construction_company|lawyer|tax_advisor|architect|unklar",
    "region": "istrien|kvarner|dalmatien-nord|dalmatien-mitte|dalmatien-sued|zagreb|slavonien|lika-gorski-kotar|unklar",
    "sprache": "de|en|hr|it|fr|unklar",
    "zusammenfassung": "Kurze Zusammenfassung des Anliegens in 1-2 Saetzen auf {lang_name}",
    "suchbegriffe": ["begriff1", "begriff2", "begriff3"]
}}

REGELN:
- Immobilienkauf/verkauf/miete → real_estate_agent
- Hausbau/Renovierung/Sanierung → construction_company
- Recht/Vertrag/Grundbuch/Erbschaft → lawyer
- Steuern/Finanzen/Buchhaltung → tax_advisor
- Planung/Design/Baugenehmigung → architect
- Wenn unklar, setze "unklar"
"""

    try:
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message="Du bist ein Experte fuer Immobilien in Kroatien. Antworte nur im JSON-Format."
        ).with_model("openai", "gpt-4o").with_params(temperature=0.3, max_tokens=300)
        
        response = await llm.send_message(UserMessage(text=prompt))
        return response.strip()
    except Exception as e:
        print(f"KI-Analyse Fehler: {e}")
        return None


def analyze_customer_request(anfrage, language='ge'):
    """Analysiert die Kundenanfrage"""
    import json
    session_id = f"matching_{uuid.uuid4().hex[:8]}"
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _analyze_request_async(anfrage, language, session_id)
            )
            
            if result:
                # JSON parsen
                result = result.replace('```json', '').replace('```', '').strip()
                return json.loads(result)
        finally:
            loop.close()
    except Exception as e:
        print(f"Analyse-Fehler: {e}")
    
    return None


def find_matching_professionals(kriterien, max_results=5):
    """Findet passende Professionals basierend auf den Kriterien"""
    from django.db.models import Q
    
    queryset = Professional.objects.filter(is_verified=True, is_active=True)
    
    # Nach Berufsgruppe filtern
    berufsgruppe = kriterien.get('berufsgruppe', 'unklar')
    if berufsgruppe and berufsgruppe != 'unklar':
        queryset = queryset.filter(professional_type=berufsgruppe)
    
    # Nach Region filtern (optional)
    region = kriterien.get('region', 'unklar')
    if region and region != 'unklar':
        queryset = queryset.filter(
            Q(region=region) | Q(service_regions__icontains=region)
        )
    
    # Nach Sprache filtern (optional)
    sprache = kriterien.get('sprache', 'unklar')
    if sprache and sprache != 'unklar':
        queryset = queryset.filter(spoken_languages__icontains=sprache)
    
    return queryset[:max_results]


def get_professional_matches(anfrage, language='ge'):
    """
    Hauptfunktion: Analysiert Anfrage und findet passende Professionals
    Gibt Dictionary zurueck mit Analyse und Ergebnissen
    """
    # 1. Anfrage analysieren
    kriterien = analyze_customer_request(anfrage, language)
    
    if not kriterien:
        return {
            'success': False,
            'error': 'Konnte Anfrage nicht analysieren',
            'professionals': []
        }
    
    # 2. Passende Professionals finden
    professionals = find_matching_professionals(kriterien)
    
    # 3. Ergebnisse formatieren
    prof_list = []
    for p in professionals:
        prof_list.append({
            'id': str(p.id),
            'name': p.name,
            'company': p.company_name or '',
            'type': p.get_professional_type_display(),
            'city': p.city,
            'region': p.get_region_display(),
            'languages': p.spoken_languages,
            'website': p.website or '',
            'phone': p.phone or '',
            'email': p.email,
            'logo_url': p.company_logo.url if p.company_logo else None,
        })
    
    return {
        'success': True,
        'kriterien': kriterien,
        'zusammenfassung': kriterien.get('zusammenfassung', ''),
        'professionals': prof_list,
        'anzahl': len(prof_list)
    }
