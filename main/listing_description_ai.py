# -*- coding: utf-8 -*-
"""
KI-Generator für Immobilien-Beschreibungen
Erstellt professionelle, sachliche Texte ohne Phrasen oder Emojis
"""
import asyncio
import uuid
from emergentintegrations.llm.openai import LlmChat, UserMessage

EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"


async def _generate_description_async(listing_data, language, session_id):
    """Generiert eine sachliche Immobilien-Beschreibung."""
    
    lang_map = {
        'ge': 'Deutsch',
        'de': 'Deutsch',
        'hr': 'Kroatisch',
        'en': 'Englisch',
    }
    lang_name = lang_map.get(language, 'Deutsch')
    
    prompt = f"""Schreibe eine sachliche Immobilien-Beschreibung auf {lang_name}.

DATEN:
- Typ: {listing_data.get('typ', 'Immobilie')}
- Preis: {listing_data.get('preis', 0):,} EUR
- Lage: {listing_data.get('ort', '')}, {listing_data.get('region', '')}
- Wohnfläche: {listing_data.get('wohnflaeche', 0)} m²
- Grundstück: {listing_data.get('grundstueck', 0)} m²
- Schlafzimmer: {listing_data.get('schlafzimmer', 0)}
- Badezimmer: {listing_data.get('badezimmer', 0)}
- Etagen: {listing_data.get('etagen', 1)}
- Garage: {listing_data.get('garage', 0)} Stellplätze
- Extras: {listing_data.get('extras', '')}

REGELN:
1. Schreibe 80-150 Wörter
2. NUR Fakten - keine Phrasen wie "Traumimmobilie", "einzigartig", "perfekt"
3. KEINE Emojis oder Icons
4. KEINE übertriebenen Adjektive
5. Sachlich und informativ
6. Erwähne Lage, Größe, Zimmeraufteilung, besondere Merkmale
7. Ende mit praktischen Informationen (Verfügbarkeit, Besichtigung)

Schreibe NUR den Beschreibungstext, keine Überschrift."""

    try:
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message="Du bist ein sachlicher Immobilientexter. Schreibe nur Fakten, keine Marketing-Phrasen."
        ).with_model("openai", "gpt-4o").with_params(temperature=0.5, max_tokens=500)
        
        response = await llm.send_message(UserMessage(text=prompt))
        return response.strip()
    except Exception as e:
        print(f"KI-Fehler: {e}")
        return None


def generate_listing_description(listing_data, language='ge'):
    """
    Hauptfunktion: Generiert Beschreibung für eine Immobilie.
    
    listing_data = {
        'typ': 'Villa',
        'preis': 450000,
        'ort': 'Rovinj',
        'region': 'Istrien',
        'wohnflaeche': 250,
        'grundstueck': 800,
        'schlafzimmer': 4,
        'badezimmer': 2,
        'etagen': 2,
        'garage': 2,
        'extras': 'Pool, Meerblick'
    }
    """
    session_id = f"listing_desc_{uuid.uuid4().hex[:8]}"
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _generate_description_async(listing_data, language, session_id)
            )
            return result
        finally:
            loop.close()
    except Exception as e:
        print(f"Fehler: {e}")
        return None


def generate_description_from_listing(listing, language='ge'):
    """Generiert Beschreibung aus einem Listing-Objekt."""
    
    typ_map = {
        'House': 'Haus',
        'Appartment': 'Wohnung',
        'Villa': 'Villa',
        'Property': 'Grundstück',
        'New Building': 'Neubau',
    }
    
    listing_data = {
        'typ': typ_map.get(listing.property_type, listing.property_type),
        'preis': listing.property_price or 0,
        'ort': listing.city or '',
        'region': listing.location or '',
        'wohnflaeche': listing.size or 0,
        'grundstueck': listing.area or 0,
        'schlafzimmer': listing.bedrooms or 0,
        'badezimmer': listing.bathrooms or 0,
        'etagen': listing.floors or 1,
        'garage': listing.garage or 0,
        'extras': '',
    }
    
    return generate_listing_description(listing_data, language)
