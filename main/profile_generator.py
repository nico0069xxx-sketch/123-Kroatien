"""
KI-Profiltext-Generator für Professionals
Generiert 8 einzigartige Profiltexte in verschiedenen Stilen
"""
import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Stil-Definitionen für die 8 Vorschläge
PROFILE_STYLES = {
    'professional_1': {
        'name_ge': 'Professionell & Seriös (Variante 1)',
        'name_en': 'Professional & Serious (Variant 1)',
        'instruction': 'Schreibe einen sehr professionellen, seriösen Profiltext. Verwende Fachbegriffe, betone Kompetenz und Erfahrung. Formeller Ton.',
    },
    'professional_2': {
        'name_ge': 'Professionell & Seriös (Variante 2)',
        'name_en': 'Professional & Serious (Variant 2)',
        'instruction': 'Schreibe einen professionellen Text mit Fokus auf Qualifikationen und Zertifizierungen. Sachlich und vertrauenswürdig.',
    },
    'friendly_1': {
        'name_ge': 'Freundlich & Persönlich (Variante 1)',
        'name_en': 'Friendly & Personal (Variant 1)',
        'instruction': 'Schreibe einen warmen, einladenden Profiltext. Persönliche Ansprache, zugänglich, sympathisch. Betone Kundenorientierung.',
    },
    'friendly_2': {
        'name_ge': 'Freundlich & Persönlich (Variante 2)',
        'name_en': 'Friendly & Personal (Variant 2)',
        'instruction': 'Schreibe einen herzlichen Text der Vertrauen aufbaut. Erzähle von der Motivation und Leidenschaft für die Arbeit.',
    },
    'short_1': {
        'name_ge': 'Kurz & Knapp (Variante 1)',
        'name_en': 'Short & Concise (Variant 1)',
        'instruction': 'Schreibe einen sehr kurzen, prägnanten Profiltext. Maximal 3 Sätze. Nur die wichtigsten Fakten.',
    },
    'short_2': {
        'name_ge': 'Kurz & Knapp (Variante 2)',
        'name_en': 'Short & Concise (Variant 2)',
        'instruction': 'Schreibe einen kompakten Text mit Bullet-Points oder kurzen Stichpunkten. Übersichtlich und scanbar.',
    },
    'detailed_1': {
        'name_ge': 'Ausführlich & Detailliert (Variante 1)',
        'name_en': 'Detailed & Comprehensive (Variant 1)',
        'instruction': 'Schreibe einen ausführlichen Profiltext. Beschreibe Dienstleistungen, Arbeitsweise und Erfahrung im Detail.',
    },
    'detailed_2': {
        'name_ge': 'Ausführlich & Detailliert (Variante 2)',
        'name_en': 'Detailed & Comprehensive (Variant 2)',
        'instruction': 'Schreibe einen umfassenden Text mit Schwerpunkt auf Spezialisierungen und Alleinstellungsmerkmalen.',
    },
}

PROFESSIONAL_TYPE_NAMES = {
    'real_estate_agent': {'ge': 'Immobilienmakler', 'en': 'Real Estate Agent', 'hr': 'Agencija za nekretnine'},
    'construction_company': {'ge': 'Bauunternehmen', 'en': 'Construction Company', 'hr': 'Građevinska tvrtka'},
    'lawyer': {'ge': 'Rechtsanwalt', 'en': 'Lawyer', 'hr': 'Odvjetnik'},
    'tax_advisor': {'ge': 'Steuerberater', 'en': 'Tax Advisor', 'hr': 'Porezni savjetnik'},
    'architect': {'ge': 'Architekt', 'en': 'Architect', 'hr': 'Arhitekt'},
}

REGION_NAMES = {
    'istrien': 'Istrien',
    'kvarner': 'Kvarner',
    'dalmatien-nord': 'Nord-Dalmatien',
    'dalmatien-mitte': 'Mittel-Dalmatien',
    'dalmatien-sued': 'Süd-Dalmatien',
    'zagreb': 'Zagreb',
    'slavonien': 'Slawonien',
    'lika-gorski-kotar': 'Lika & Gorski Kotar',
}


def generate_profile_texts(data, language='ge'):
    """
    Generiert 8 einzigartige Profiltexte basierend auf den Basisdaten.
    
    Args:
        data: Dict mit name, company_name, professional_type, region, city, languages_spoken, etc.
        language: Sprache für die Ausgabe
    
    Returns:
        Dict mit 8 Texten: {'professional_1': '...', 'professional_2': '...', ...}
    """
    
    prof_type = data.get('professional_type', '')
    prof_name = PROFESSIONAL_TYPE_NAMES.get(prof_type, {}).get(language, prof_type)
    region_name = REGION_NAMES.get(data.get('region', ''), data.get('region', ''))
    
    base_info = f"""
Name: {data.get('name', '')}
Firma: {data.get('company_name', '')}
Berufsgruppe: {prof_name}
Region: {region_name}
Stadt: {data.get('city', '')}
Sprachen: {data.get('languages_spoken', '')}
Webseite: {data.get('website', '')}
"""
    
    lang_instruction = {
        'ge': 'Schreibe auf Deutsch.',
        'en': 'Write in English.',
        'hr': 'Piši na hrvatskom.',
    }.get(language, 'Schreibe auf Deutsch.')
    
    results = {}
    
    for style_key, style_info in PROFILE_STYLES.items():
        prompt = f"""Du bist ein Experte für Profiltexte auf einer Immobilien-Plattform in Kroatien.

AUFGABE: Erstelle einen einzigartigen Profiltext für diesen Dienstleister.

BASISDATEN:
{base_info}

STIL-ANWEISUNG:
{style_info['instruction']}

WICHTIGE REGELN:
- {lang_instruction}
- Der Text muss EINZIGARTIG sein (nicht kopierbar)
- Keine generischen Floskeln
- Keine falschen Behauptungen
- Maximal 150 Wörter
- SEO-freundlich aber natürlich
- Für {prof_name} in Kroatien passend

Schreibe NUR den Profiltext, keine Erklärungen."""

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Du erstellst professionelle Profiltexte für Dienstleister."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.9  # Höhere Kreativität für Varianz
            )
            
            results[style_key] = {
                'style_name': style_info.get(f'name_{language}', style_info['name_ge']),
                'text': response.choices[0].message.content.strip()
            }
            
        except Exception as e:
            print(f"Fehler bei Stil {style_key}: {e}")
            results[style_key] = {
                'style_name': style_info.get(f'name_{language}', style_info['name_ge']),
                'text': f"Fehler bei der Generierung. Bitte versuchen Sie es erneut."
            }
    
    return results


def check_spelling(text, language='ge'):
    """
    Prüft Rechtschreibung und gibt Korrekturvorschläge zurück.
    """
    lang_name = {'ge': 'Deutsch', 'en': 'English', 'hr': 'Kroatisch'}.get(language, 'Deutsch')
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Du bist ein {lang_name}-Korrektor. Finde Rechtschreib- und Grammatikfehler."},
                {"role": "user", "content": f"""Prüfe diesen Text auf Rechtschreibung und Grammatik.

TEXT:
{text}

Antworte im JSON-Format:
{{
    "has_errors": true/false,
    "corrected_text": "korrigierter Text",
    "errors": ["Fehler 1", "Fehler 2", ...]
}}

Nur JSON ausgeben, keine Erklärungen."""}
            ],
            max_tokens=500,
            temperature=0.1
        )
        
        result = response.choices[0].message.content.strip()
        
        # JSON parsen
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        
        return json.loads(result)
        
    except Exception as e:
        print(f"Rechtschreibprüfung Fehler: {e}")
        return {"has_errors": False, "corrected_text": text, "errors": []}


def improve_text(text, language='ge'):
    """
    Verbessert einen Text stilistisch.
    """
    lang_name = {'ge': 'Deutsch', 'en': 'English', 'hr': 'Kroatisch'}.get(language, 'Deutsch')
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Du verbesserst Texte auf {lang_name} für eine professionelle Immobilien-Plattform."},
                {"role": "user", "content": f"""Verbessere diesen Profiltext stilistisch. 
Mache ihn professioneller, klarer und ansprechender.
Behalte die Kernaussagen bei.

ORIGINALTEXT:
{text}

Gib NUR den verbesserten Text aus, keine Erklärungen."""}
            ],
            max_tokens=400,
            temperature=0.5
        )
        
        return response.choices[0].message.content.strip()
        
    except Exception as e:
        print(f"Textverbesserung Fehler: {e}")
        return text


def translate_profile(text, target_languages):
    """
    Übersetzt einen Profiltext in alle 12 Sprachen.
    
    Args:
        text: Originaltext
        target_languages: Liste der Zielsprachen ['en', 'hr', 'fr', ...]
    
    Returns:
        Dict mit Übersetzungen: {'en': '...', 'hr': '...', ...}
    """
    
    lang_names = {
        'ge': 'Deutsch', 'en': 'Englisch', 'hr': 'Kroatisch', 'fr': 'Französisch',
        'nl': 'Niederländisch', 'pl': 'Polnisch', 'cz': 'Tschechisch', 'sk': 'Slowakisch',
        'ru': 'Russisch', 'gr': 'Griechisch', 'sw': 'Schwedisch', 'no': 'Norwegisch'
    }
    
    translations = {}
    
    for lang in target_languages:
        if lang == 'ge':  # Original ist Deutsch
            translations[lang] = text
            continue
        
        lang_name = lang_names.get(lang, lang)
        
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": f"Du bist ein professioneller Übersetzer. Übersetze ins {lang_name}."},
                    {"role": "user", "content": f"""Übersetze diesen Profiltext ins {lang_name}.
Behalte den Stil und die Professionalität bei.

TEXT:
{text}

Gib NUR die Übersetzung aus."""}
                ],
                max_tokens=400,
                temperature=0.3
            )
            
            translations[lang] = response.choices[0].message.content.strip()
            
        except Exception as e:
            print(f"Übersetzung {lang} Fehler: {e}")
            translations[lang] = text  # Fallback auf Original
    
    return translations


def generate_seo_slug(name, company_name, city, professional_type):
    """
    Generiert einen SEO-optimierten Slug.
    """
    import re
    from django.utils.text import slugify
    import uuid
    
    # Basis-Slug erstellen
    parts = []
    
    if company_name:
        parts.append(company_name)
    elif name:
        parts.append(name)
    
    if city:
        parts.append(city)
    
    # Slug erstellen
    base_slug = slugify('-'.join(parts))
    
    # Einzigartig machen
    unique_slug = f"{base_slug}-{str(uuid.uuid4())[:8]}"
    
    return unique_slug
