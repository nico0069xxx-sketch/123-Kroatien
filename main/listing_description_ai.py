# -*- coding: utf-8 -*-
"""
KI-Generator für Immobilien-Beschreibungen
"""
import asyncio
import uuid
from emergentintegrations.llm.openai import LlmChat, UserMessage

EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"


async def _generate_description_async(listing_data, language, session_id):
    lang_map = {'ge': 'Deutsch', 'de': 'Deutsch', 'hr': 'Kroatisch', 'en': 'Englisch'}
    lang_name = lang_map.get(language, 'Deutsch')
    
    prompt = f"""Schreibe eine sachliche Immobilien-Beschreibung auf {lang_name}.

DATEN:
- Typ: {listing_data.get('typ', 'Immobilie')}
- Preis: {listing_data.get('preis', 0):,} EUR
- Lage: {listing_data.get('ort', '')}, {listing_data.get('region', '')}
- Wohnflaeche: {listing_data.get('wohnflaeche', 0)} m2
- Grundstueck: {listing_data.get('grundstueck', 0)} m2
- Schlafzimmer: {listing_data.get('schlafzimmer', 0)}
- Badezimmer: {listing_data.get('badezimmer', 0)}

REGELN: 80-150 Woerter, NUR Fakten, KEINE Emojis, sachlich.

Schreibe NUR den Beschreibungstext."""

    try:
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message="Du bist ein sachlicher Immobilientexter."
        ).with_model("openai", "gpt-4o").with_params(temperature=0.5, max_tokens=500)
        
        response = await llm.send_message(UserMessage(text=prompt))
        return response.strip()
    except Exception as e:
        print(f"KI-Fehler: {e}")
        return None


def generate_listing_description(listing_data, language='ge'):
    session_id = f"listing_desc_{uuid.uuid4().hex[:8]}"
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(_generate_description_async(listing_data, language, session_id))
        finally:
            loop.close()
    except Exception as e:
        print(f"Fehler: {e}")
        return None


def generate_description_from_listing(listing, language='ge'):
    typ_map = {'House': 'Haus', 'Appartment': 'Wohnung', 'Villa': 'Villa', 'Property': 'Grundstueck', 'New Building': 'Neubau'}
    
    listing_data = {
        'typ': typ_map.get(listing.property_type, listing.property_type),
        'preis': listing.property_price or 0,
        'ort': listing.city or '',
        'region': listing.location or '',
        'wohnflaeche': listing.size or 0,
        'grundstueck': listing.area or 0,
        'schlafzimmer': listing.bedrooms or 0,
        'badezimmer': listing.bathrooms or 0,
    }
    
    return generate_listing_description(listing_data, language)
