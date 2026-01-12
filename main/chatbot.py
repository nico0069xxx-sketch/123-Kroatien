import os
import json
import hashlib
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# =============================================================================
# KOSTEN-OPTIMIERUNG: Antwort-Cache
# =============================================================================
RESPONSE_CACHE = {}
CACHE_MAX_SIZE = 100

def get_cache_key(message, language):
    """Erstellt einen eindeutigen Cache-Key"""
    return hashlib.md5(f"{message.lower().strip()}_{language}".encode()).hexdigest()

def get_cached_response(message, language):
    """Prüft ob eine Antwort im Cache ist"""
    key = get_cache_key(message, language)
    return RESPONSE_CACHE.get(key)

def cache_response(message, language, response):
    """Speichert eine Antwort im Cache"""
    if len(RESPONSE_CACHE) >= CACHE_MAX_SIZE:
        oldest_key = next(iter(RESPONSE_CACHE))
        del RESPONSE_CACHE[oldest_key]
    key = get_cache_key(message, language)
    RESPONSE_CACHE[key] = response

# =============================================================================
# SPRACHSPEZIFISCHE FAQ-DATEN LADEN (BUG-FIX: ge -> faq_data.json)
# =============================================================================
FAQ_DATA_CACHE = {}

# Mapping: Sprachcode -> Dateiname
LANGUAGE_FILE_MAP = {
    'ge': 'faq_data.json',      # Deutsch = Hauptdatei (BUGFIX!)
    'en': 'faq_data_en.json',
    'fr': 'faq_data_fr.json',
    'hr': 'faq_data_hr.json',
    'gr': 'faq_data_gr.json',
    'pl': 'faq_data_pl.json',
    'cz': 'faq_data_cz.json',
    'ru': 'faq_data_ru.json',
    'sw': 'faq_data_sw.json',
    'no': 'faq_data_no.json',
    'sk': 'faq_data_sk.json',
    'nl': 'faq_data_nl.json',
}

def load_faq_data(language='ge'):
    """Lädt die FAQ-Daten für eine bestimmte Sprache"""
    if language in FAQ_DATA_CACHE:
        return FAQ_DATA_CACHE[language]
    
    # Korrekten Dateinamen aus Mapping holen
    faq_filename = LANGUAGE_FILE_MAP.get(language, 'faq_data.json')
    faq_path = os.path.join(os.path.dirname(__file__), faq_filename)
    
    # Fallback auf deutsche Hauptdatei
    if not os.path.exists(faq_path):
        faq_path = os.path.join(os.path.dirname(__file__), 'faq_data.json')
    
    try:
        with open(faq_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            FAQ_DATA_CACHE[language] = data
            return data
    except Exception as e:
        print(f"FAQ laden fehlgeschlagen: {e}")
        return []

# =============================================================================
# KOSTEN-OPTIMIERUNG: Relevante FAQs finden (ohne API-Call)
# =============================================================================
def find_relevant_faqs(message, faq_data, max_results=5):
    """
    Findet relevante FAQs basierend auf Keyword-Matching.
    KOSTENLOS - kein API-Call nötig!
    """
    message_lower = message.lower()
    scored_faqs = []
    
    for faq in faq_data:
        score = 0
        question = faq.get('q', '').lower()
        answer = faq.get('a', '').lower()
        
        words = message_lower.split()
        for word in words:
            if len(word) > 3:
                if word in question:
                    score += 3
                if word in answer:
                    score += 1
        
        if score > 0:
            scored_faqs.append((score, faq))
    
    scored_faqs.sort(key=lambda x: x[0], reverse=True)
    return [faq for score, faq in scored_faqs[:max_results]]

def check_direct_faq_match(message, faq_data):
    """
    Prüft ob die Frage direkt in den FAQs beantwortet werden kann.
    Gibt None zurück - wir wollen IMMER durch GPT für Königsklasse-Qualität!
    """
    # Deaktiviert für Königsklasse-Qualität
    # Alle Antworten gehen durch den Master-Prompt
    return None

# =============================================================================
# MASTER-PROMPT: KÖNIGSKLASSE CONTENT ENGINE
# =============================================================================
MASTER_SYSTEM_PROMPT = """Du bist ein Experte für Immobilien in Kroatien und Content-Ersteller für 123-Kroatien.eu.

DEINE AUFGABE:
Generiere hochwertige, faktenbasierte, SEO-optimierte und KI-zitierbare Antworten.

SPRACHE: {lang_instruction}

ANTWORT-STRUKTUR (WICHTIG - HALTE DICH STRIKT DARAN):
1. **Direkte Antwort** (2-3 Sätze): Klar, faktisch, neutral - für Featured Snippets geeignet
2. **Details** (wenn nötig): Rechtlicher Kontext, regionale Besonderheiten in Kroatien
3. **Wichtige Fakten**: Zahlen, Preise, Prozentsätze als Stichpunkte (mit • Aufzählungszeichen)
4. **Praktischer Rat**: Was der Nutzer beachten sollte

REGELN (NICHT VERHANDELBAR):
- Keine Marketing-Sprache oder Werbefloskeln
- Keine übertriebenen Behauptungen ("unvergleichlich", "einzigartig", "traumhaft")
- Keine Spekulation
- Keine Füllwörter
- Keine Handlungsaufforderungen (CTAs)
- Nicht erwähnen, dass du eine KI bist
- Faktenbasiert und neutral
- Leicht von KI-Systemen zitierbar
- Von Menschen lesbar

KROATIEN-SPEZIFISCH:
- Gehe davon aus, dass der Leser an Kroatien interessiert ist
- Erwähne Kroatien explizit wenn relevant
- Bei regionalen Unterschieden (Gesetze, Steuern) klar darauf hinweisen

CHATBOT-KOMPATIBILITÄT:
- Antworten müssen eigenständig sein
- Keine externen Websites referenzieren (außer 123-kroatien.eu)
- Keinen vorherigen Kontext voraussetzen

FAQ-WISSEN (nutze diese Informationen):
{faq_context}

Beantworte die Frage des Nutzers basierend auf diesem Wissen. Halte dich STRIKT an die Antwort-Struktur."""

def get_chatbot_response(message, language='ge'):
    """
    KI-Chatbot für Immobilien-Plattform - KÖNIGSKLASSE Edition
    Mit Kosten-Optimierung durch Caching und Smart FAQ-Matching
    """
    
    # SCHRITT 1: Cache prüfen (KOSTENLOS)
    cached = get_cached_response(message, language)
    if cached:
        return cached
    
    # SCHRITT 2: FAQ-Daten laden (mit Bug-Fix)
    faq_data = load_faq_data(language)
    
    # SCHRITT 3: Relevante FAQs finden (KOSTENLOS)
    relevant_faqs = find_relevant_faqs(message, faq_data, max_results=5)
    
    # SCHRITT 4: GPT aufrufen mit Master-Prompt
    try:
        lang_instructions = {
            'ge': 'Antworte auf Deutsch.',
            'en': 'Respond in English.',
            'fr': 'Réponds en français.',
            'hr': 'Odgovori na hrvatskom.',
            'gr': 'Απάντησε στα ελληνικά.',
            'pl': 'Odpowiedz po polsku.',
            'cz': 'Odpověz česky.',
            'ru': 'Ответь по-русски.',
            'sw': 'Svara på svenska.',
            'no': 'Svar på norsk.',
            'sk': 'Odpovedz po slovensky.',
            'nl': 'Antwoord in het Nederlands.',
        }
        
        lang_instruction = lang_instructions.get(language, 'Antworte auf Deutsch.')
        
        # Nur relevante FAQs als Kontext senden (KOSTEN-OPTIMIERUNG)
        if relevant_faqs:
            faq_context = "RELEVANTE FAQ-INFORMATIONEN:\n\n"
            for faq in relevant_faqs:
                faq_context += f"FRAGE: {faq.get('q', '')}\nANTWORT: {faq.get('a', '')}\n\n"
        else:
            faq_context = "Keine direkt relevanten FAQs gefunden. Nutze dein allgemeines Wissen über Immobilien in Kroatien."
        
        system_prompt = MASTER_SYSTEM_PROMPT.format(
            lang_instruction=lang_instruction,
            faq_context=faq_context
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=600,
            temperature=0.3  # Niedriger = konsistenter und faktenbasierter
        )
        
        result = response.choices[0].message.content
        
        # Antwort cachen
        cache_response(message, language, result)
        
        return result
        
    except Exception as e:
        print(f"OpenAI Error: {e}")
        
        if relevant_faqs:
            return relevant_faqs[0].get('a', 'Entschuldigung, es gab ein technisches Problem.')
        
        return "Entschuldigung, es gab ein technisches Problem. Bitte versuchen Sie es später erneut."


def get_cache_stats():
    """Gibt Cache-Statistiken zurück"""
    return {
        "cached_responses": len(RESPONSE_CACHE),
        "max_cache_size": CACHE_MAX_SIZE,
        "faq_languages_loaded": list(FAQ_DATA_CACHE.keys())
    }


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


# =============================================================================
# CHATBOT + SMART-SEARCH INTEGRATION
# =============================================================================

def get_chatbot_response_with_search(message, language='ge', listings_callback=None):
    """
    Erweiterter Chatbot: Erkennt Suchanfragen und gibt Immobilien zurück.
    
    Args:
        message: Benutzer-Nachricht
        language: Sprachcode
        listings_callback: Funktion die Listings aus DB holt (optional)
    
    Returns:
        dict mit 'response', 'is_search', 'search_results'
    """
    
    # Prüfen ob es eine Suchanfrage ist
    if is_property_search(message):
        # Suchkriterien extrahieren
        criteria = extract_search_criteria(message, language)
        
        search_response = {
            'is_search': True,
            'criteria': criteria,
            'search_results': [],
            'response': ''
        }
        
        # Antwort generieren
        lang_responses = {
            'ge': "Ich suche passende Immobilien für dich...",
            'en': "I'm searching for matching properties for you...",
            'hr': "Tražim odgovarajuće nekretnine za vas...",
            'fr': "Je recherche des propriétés correspondantes pour vous...",
            'nl': "Ik zoek passende woningen voor u...",
            'pl': "Szukam pasujących nieruchomości dla Ciebie...",
            'cz': "Hledám pro vás odpovídající nemovitosti...",
            'sk': "Hľadám pre vás zodpovedajúce nehnuteľnosti...",
            'ru': "Ищу подходящие объекты для вас...",
            'gr': "Ψάχνω κατάλληλα ακίνητα για εσάς...",
            'sw': "Jag söker matchande fastigheter åt dig...",
            'no': "Jeg søker etter matchende eiendommer for deg...",
        }
        
        search_response['response'] = lang_responses.get(language, lang_responses['ge'])
        
        return search_response
    
    # Normale Chatbot-Antwort
    response = get_chatbot_response(message, language)
    
    return {
        'is_search': False,
        'criteria': None,
        'search_results': [],
        'response': response
    }
