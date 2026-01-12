#!/usr/bin/env python3
"""
Fügt AI Smart-Search Funktion zum Chatbot hinzu
"""

# Code der am Ende von chatbot.py eingefügt wird
smart_search_code = '''

# =============================================================================
# AI SMART-SEARCH: Natürliche Sprache -> Suchfilter
# =============================================================================

SEARCH_EXTRACT_PROMPT = """Extrahiere Suchkriterien aus dieser Immobilienanfrage.

Anfrage: "{query}"

Antworte NUR mit JSON (keine Erklärung):
{{
    "property_type": "House|Appartment|New Building|Property|null",
    "property_status": "Sale|Rent|null",
    "price_min": <Zahl oder null>,
    "price_max": <Zahl oder null>,
    "bedrooms_min": <Zahl oder null>,
    "bathrooms_min": <Zahl oder null>,
    "area_min": <Zahl in m² oder null>,
    "location": "<Region oder null>",
    "features": ["pool", "meerblick", "garage", ...]
}}

Regeln:
- Nur explizit genannte Kriterien extrahieren
- Preise in Euro (ohne Währungszeichen)
- "Haus am Meer" = location könnte Küstenregion sein
- "günstig" = ignorieren (zu vage)
- "Pool", "Meerblick", "Garten" = in features Array"""

def extract_search_criteria(query, language='ge'):
    """
    Extrahiert Suchkriterien aus natürlicher Sprache.
    Kostengünstig: Nur 1 API-Call mit kurzem Prompt.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SEARCH_EXTRACT_PROMPT.format(query=query)},
                {"role": "user", "content": query}
            ],
            max_tokens=200,
            temperature=0.1  # Sehr niedrig für konsistentes JSON
        )
        
        result = response.choices[0].message.content.strip()
        
        # JSON parsen
        if result.startswith("```"):
            result = result.split("```")[1]
            if result.startswith("json"):
                result = result[4:]
        
        criteria = json.loads(result)
        return criteria
        
    except Exception as e:
        print(f"Smart-Search Fehler: {e}")
        return {}


def smart_search_response(query, results_count, language='ge'):
    """
    Generiert eine freundliche Antwort für Suchergebnisse.
    """
    lang_responses = {
        'ge': {
            'found': f"Ich habe {results_count} passende Immobilien für dich gefunden!",
            'none': "Leider habe ich keine passenden Immobilien gefunden. Versuche es mit anderen Kriterien.",
            'error': "Bei der Suche ist ein Fehler aufgetreten."
        },
        'en': {
            'found': f"I found {results_count} matching properties for you!",
            'none': "Unfortunately, I couldn't find any matching properties. Try different criteria.",
            'error': "An error occurred during the search."
        },
        'hr': {
            'found': f"Pronašao sam {results_count} odgovarajućih nekretnina za vas!",
            'none': "Nažalost, nisam pronašao odgovarajuće nekretnine. Pokušajte s drugim kriterijima.",
            'error': "Došlo je do pogreške prilikom pretrage."
        }
    }
    
    responses = lang_responses.get(language, lang_responses['ge'])
    
    if results_count > 0:
        return responses['found']
    else:
        return responses['none']


def is_property_search(message):
    """
    Erkennt ob eine Nachricht eine Immobiliensuche ist.
    KOSTENLOS - kein API-Call!
    """
    search_keywords = [
        # Deutsch
        'suche', 'finde', 'zeig', 'haus', 'wohnung', 'apartment', 'immobilie',
        'kaufen', 'mieten', 'grundstück', 'villa', 'neubau',
        'schlafzimmer', 'bad', 'pool', 'meerblick', 'garten',
        'euro', '€', 'preis', 'bis', 'unter', 'max',
        # Englisch
        'search', 'find', 'show', 'house', 'property', 'buy', 'rent',
        'bedroom', 'bathroom', 'sea view', 'garden',
        # Kroatisch
        'tražim', 'kuća', 'stan', 'nekretnina', 'kupiti', 'najam'
    ]
    
    message_lower = message.lower()
    matches = sum(1 for kw in search_keywords if kw in message_lower)
    
    return matches >= 2  # Mindestens 2 Keywords = wahrscheinlich Suche
'''

# Datei lesen und erweitern
with open("main/chatbot.py", "r", encoding="utf-8") as f:
    content = f.read()

# Prüfen ob Smart-Search schon existiert
if "extract_search_criteria" not in content:
    content += smart_search_code
    with open("main/chatbot.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Smart-Search Funktionen zu chatbot.py hinzugefügt!")
else:
    print("⚠️  Smart-Search existiert bereits in chatbot.py")
