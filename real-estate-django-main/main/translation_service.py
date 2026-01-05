"""
Translation Service für statische Texte
Verwendet Emergent LLM Integration für automatische Übersetzungen in 12 Sprachen
"""
import os
import sys
import asyncio
from asgiref.sync import sync_to_async

# Emergent LLM Key
EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"

# Alle unterstützten Sprachen
LANGUAGES = {
    'en': 'English',
    'ge': 'German', 
    'fr': 'French',
    'gr': 'Greek',
    'hr': 'Croatian',
    'pl': 'Polish',
    'cz': 'Czech',
    'ru': 'Russian',
    'sw': 'Swedish',
    'no': 'Norwegian',
    'sk': 'Slovak',
    'nl': 'Dutch'
}

async def translate_text(text, target_language):
    """Übersetzt einen Text in die Zielsprache mit Emergent Integration"""
    from emergentintegrations.llm.chat import LlmChat, UserMessage
    
    if not text or text.strip() == '':
        return text
    
    try:
        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"translate-{target_language}-{hash(text)}",
            system_message=f"You are a professional translator. Translate the following text to {target_language}. Return ONLY the translated text, nothing else. Keep the same tone and style. Do not add any explanations."
        ).with_model("openai", "gpt-4o-mini")
        
        user_message = UserMessage(text=text)
        response = await chat.send_message(user_message)
        return response.strip()
    except Exception as e:
        print(f"Fehler bei Übersetzung von '{text}' nach {target_language}: {e}")
        return text

async def translate_all_languages(german_text):
    """Übersetzt einen deutschen Text in alle 12 Sprachen"""
    translations = {'ge': german_text}
    
    for lang_code, lang_name in LANGUAGES.items():
        if lang_code == 'ge':
            continue
        result = await translate_text(german_text, lang_name)
        translations[lang_code] = result
        print(f"  {lang_code}: {result}")
    
    return translations

# Alle statischen Texte die übersetzt werden müssen (Deutsch als Basis)
STATIC_TEXTS = {
    # Navigation - navbar
    'nav_buy': {'page': 'navbar', 'german': 'Kaufen'},
    'nav_sell': {'page': 'navbar', 'german': 'Verkaufen'},
    'nav_contact': {'page': 'navbar', 'german': 'Kontakt'},
    'nav_about': {'page': 'navbar', 'german': 'Über uns'},
    'nav_faq': {'page': 'navbar', 'german': 'F.A.Q'},
    'nav_add_listing': {'page': 'navbar', 'german': 'Immobilie hinzufügen'},
    'nav_logout': {'page': 'navbar', 'german': 'Abmelden'},
    'nav_login': {'page': 'navbar', 'german': 'Anmelden'},
    'nav_register': {'page': 'navbar', 'german': 'Registrieren'},
    
    # Dropdown Kaufen
    'dropdown_house': {'page': 'navbar', 'german': 'Haus'},
    'dropdown_apartment': {'page': 'navbar', 'german': 'Wohnung'},
    'dropdown_new_building': {'page': 'navbar', 'german': 'Neubau'},
    'dropdown_land': {'page': 'navbar', 'german': 'Grundstück'},
    
    # Dropdown Benutzer
    'dropdown_realtor': {'page': 'navbar', 'german': 'Immobilienmakler'},
    'dropdown_contractor': {'page': 'navbar', 'german': 'Bauunternehmer'},
    'dropdown_owner': {'page': 'navbar', 'german': 'Eigentümer'},
    
    # Allgemeine Labels
    'label_for_sale': {'page': 'listings', 'german': 'Zu verkaufen'},
    'label_for_rent': {'page': 'listings', 'german': 'Zu vermieten'},
    'label_bedrooms': {'page': 'listings', 'german': 'Schlafzimmer'},
    'label_bathrooms': {'page': 'listings', 'german': 'Badezimmer'},
    'label_area': {'page': 'listings', 'german': 'Fläche'},
    'label_sqm': {'page': 'listings', 'german': 'qm'},
    'label_price': {'page': 'listings', 'german': 'Preis'},
    'label_description': {'page': 'property details', 'german': 'Beschreibung'},
    'label_features': {'page': 'property details', 'german': 'Ausstattung'},
    'label_location': {'page': 'property details', 'german': 'Standort'},
    'label_details': {'page': 'property details', 'german': 'Details'},
    'label_garage': {'page': 'property details', 'german': 'Garage'},
    'label_floors': {'page': 'property details', 'german': 'Etagen'},
    'label_deposit': {'page': 'property details', 'german': 'Anzahlung'},
    'label_property_id': {'page': 'property details', 'german': 'Immobilien-ID'},
    'label_property_type': {'page': 'property details', 'german': 'Immobilientyp'},
    'label_property_status': {'page': 'property details', 'german': 'Status'},
    
    # Buttons
    'btn_view_details': {'page': 'listings', 'german': 'Details anzeigen'},
    'btn_contact_agent': {'page': 'property details', 'german': 'Makler kontaktieren'},
    'btn_send_message': {'page': 'contact', 'german': 'Nachricht senden'},
    'btn_submit': {'page': 'contact', 'german': 'Absenden'},
    'btn_search': {'page': 'home', 'german': 'Suchen'},
    'btn_load_more': {'page': 'listings', 'german': 'Mehr laden'},
    
    # Homepage
    'home_title': {'page': 'home', 'german': 'Finden Sie Ihre Traumimmobilie in Kroatien'},
    'home_subtitle': {'page': 'home', 'german': 'Entdecken Sie die besten Immobilien an der kroatischen Küste'},
    'home_latest_listings': {'page': 'home', 'german': 'Neueste Immobilien'},
    'home_featured': {'page': 'home', 'german': 'Empfohlene Immobilien'},
    
    # Property Types
    'type_house': {'page': 'listings', 'german': 'Haus'},
    'type_apartment': {'page': 'listings', 'german': 'Wohnung'},
    'type_villa': {'page': 'listings', 'german': 'Villa'},
    'type_office': {'page': 'listings', 'german': 'Büro'},
    'type_land': {'page': 'listings', 'german': 'Grundstück'},
    'type_family_house': {'page': 'listings', 'german': 'Familienhaus'},
    'type_modern_villa': {'page': 'listings', 'german': 'Moderne Villa'},
    'type_town_house': {'page': 'listings', 'german': 'Stadthaus'},
    
    # Footer
    'footer_about': {'page': 'footer', 'german': 'Über uns'},
    'footer_contact': {'page': 'footer', 'german': 'Kontakt'},
    'footer_privacy': {'page': 'footer', 'german': 'Datenschutz'},
    'footer_imprint': {'page': 'footer', 'german': 'Impressum'},
    'footer_terms': {'page': 'footer', 'german': 'AGB'},
    'footer_sitemap': {'page': 'footer', 'german': 'Sitemap'},
    'footer_copyright': {'page': 'footer', 'german': 'Alle Rechte vorbehalten'},
    
    # Contact
    'contact_title': {'page': 'contact', 'german': 'Kontaktieren Sie uns'},
    'contact_name': {'page': 'contact', 'german': 'Name'},
    'contact_email': {'page': 'contact', 'german': 'E-Mail'},
    'contact_phone': {'page': 'contact', 'german': 'Telefon'},
    'contact_message': {'page': 'contact', 'german': 'Nachricht'},
    
    # About
    'about_title': {'page': 'about', 'german': 'Über 123-Kroatien'},
    'about_mission': {'page': 'about', 'german': 'Unsere Mission'},
    
    # Login/Register
    'login_title': {'page': 'login', 'german': 'Anmelden'},
    'login_email': {'page': 'login', 'german': 'E-Mail Adresse'},
    'login_password': {'page': 'login', 'german': 'Passwort'},
    'login_remember': {'page': 'login', 'german': 'Angemeldet bleiben'},
    'login_forgot': {'page': 'login', 'german': 'Passwort vergessen?'},
    'register_title': {'page': 'signup', 'german': 'Registrieren'},
    'register_firstname': {'page': 'signup', 'german': 'Vorname'},
    'register_lastname': {'page': 'signup', 'german': 'Nachname'},
    'register_confirm_password': {'page': 'signup', 'german': 'Passwort bestätigen'},
    
    # Filter/Search
    'filter_property_type': {'page': 'listings', 'german': 'Immobilientyp'},
    'filter_location': {'page': 'listings', 'german': 'Standort'},
    'filter_price_range': {'page': 'listings', 'german': 'Preisbereich'},
    'filter_bedrooms': {'page': 'listings', 'german': 'Schlafzimmer'},
    'filter_bathrooms': {'page': 'listings', 'german': 'Badezimmer'},
    'filter_min_area': {'page': 'listings', 'german': 'Min. Fläche'},
    'filter_max_area': {'page': 'listings', 'german': 'Max. Fläche'},
    'filter_all': {'page': 'listings', 'german': 'Alle'},
    
    # Messages
    'msg_no_listings': {'page': 'listings', 'german': 'Keine Immobilien gefunden'},
    'msg_loading': {'page': 'home', 'german': 'Laden...'},
    'msg_success': {'page': 'contact', 'german': 'Erfolgreich gesendet!'},
    'msg_error': {'page': 'contact', 'german': 'Ein Fehler ist aufgetreten'},
}

async def populate_translations():
    """Fügt alle Übersetzungen in die Datenbank ein"""
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
    sys.path.insert(0, '/app/real-estate-django-main')
    django.setup()
    
    from pages.models import Translation
    
    # Erste alle bestehenden löschen (sync)
    await sync_to_async(Translation.objects.all().delete)()
    print("Bestehende Übersetzungen gelöscht.")
    
    total = len(STATIC_TEXTS)
    current = 0
    
    for name, data in STATIC_TEXTS.items():
        current += 1
        print(f"\n[{current}/{total}] Übersetze: {name} ({data['german']})")
        
        # Übersetze in alle Sprachen
        translations = await translate_all_languages(data['german'])
        
        # In Datenbank speichern (sync)
        @sync_to_async
        def save_translation():
            translation = Translation(
                name=name,
                page=data['page'],
                german_content=translations.get('ge', data['german']),
                english_content=translations.get('en', ''),
                french_content=translations.get('fr', ''),
                greek_content=translations.get('gr', ''),
                croatian_content=translations.get('hr', ''),
                polish_content=translations.get('pl', ''),
                czech_content=translations.get('cz', ''),
                russian_content=translations.get('ru', ''),
                swedish_content=translations.get('sw', ''),
                norway_content=translations.get('no', ''),
                slovak_content=translations.get('sk', ''),
                dutch_content=translations.get('nl', '')
            )
            translation.save()
        
        await save_translation()
        print(f"  ✓ Gespeichert!")
    
    print(f"\n\n=== FERTIG! {total} Übersetzungen erstellt ===")

if __name__ == '__main__':
    asyncio.run(populate_translations())
