#!/usr/bin/env python3
"""
Erweitert den Chatbot um Smart-Search Erkennung
"""

chatbot_extension = '''

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
'''

with open("main/chatbot.py", "r", encoding="utf-8") as f:
    content = f.read()

if "get_chatbot_response_with_search" not in content:
    content += chatbot_extension
    with open("main/chatbot.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Chatbot-Integration hinzugefügt!")
else:
    print("⚠️  Chatbot-Integration existiert bereits")
