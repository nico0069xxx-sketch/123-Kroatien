from django.utils.translation import activate
from pages.models import Translation
from django.urls import reverse
import re
import json

# Alle unterstützten Sprachen
ALL_LANGUAGES = ['ge', 'en', 'hr', 'fr', 'nl', 'pl', 'cz', 'sk', 'ru', 'gr', 'sw', 'no']

# Glossar-Pfad je Sprache
GLOSSARY_URLS = {
    "ge": "glossar", "en": "glossary", "hr": "pojmovnik", "fr": "glossaire",
    "nl": "woordenlijst", "pl": "slownik", "cz": "glosar", "sk": "slovnik",
    "ru": "glossarij", "gr": "glossari", "sw": "ordlista", "no": "ordliste",
}

# URL-Pfade für Dienstleister in allen Sprachen
CATEGORY_URLS = {
    "real_estate_agent": {
        "ge": "immobilienmakler", "en": "real-estate-agents", "hr": "agencije-za-nekretnine",
        "fr": "agents-immobiliers", "nl": "makelaars", "pl": "agenci-nieruchomosci",
        "cz": "realitni-makleri", "sk": "realitni-makleri", "ru": "agenty-nedvizhimosti",
        "gr": "mesites-akiniton", "sw": "fastighetsmaklare", "no": "eiendomsmeglere",
    },
    "construction_company": {
        "ge": "bauunternehmen", "en": "construction-companies", "hr": "gradevinske-tvrtke",
        "fr": "entreprises-construction", "nl": "bouwbedrijven", "pl": "firmy-budowlane",
        "cz": "stavebni-firmy", "sk": "stavebne-firmy", "ru": "stroitelnye-kompanii",
        "gr": "kataskevestikes-etaireies", "sw": "byggforetag", "no": "byggefirmaer",
    },
    "lawyer": {
        "ge": "rechtsanwaelte", "en": "lawyers", "hr": "odvjetnici",
        "fr": "avocats", "nl": "advocaten", "pl": "prawnicy",
        "cz": "pravnici", "sk": "pravnici", "ru": "advokaty",
        "gr": "dikigoroi", "sw": "advokater", "no": "advokater",
    },
    "tax_advisor": {
        "ge": "steuerberater", "en": "tax-advisors", "hr": "porezni-savjetnici",
        "fr": "conseillers-fiscaux", "nl": "belastingadviseurs", "pl": "doradcy-podatkowi",
        "cz": "danovi-poradci", "sk": "danovi-poradcovia", "ru": "nalogovye-konsultanty",
        "gr": "forologikoi-symvouloi", "sw": "skatteradgivare", "no": "skatteradgivere",
    },
    "architect": {
        "ge": "architekten", "en": "architects", "hr": "arhitekti",
        "fr": "architectes", "nl": "architecten", "pl": "architekci",
        "cz": "architekti", "sk": "architekti", "ru": "arhitektory",
        "gr": "architektons", "sw": "arkitekter", "no": "arkitekter",
    },
}

COUNTRY_NAMES = {
    "ge": "kroatien", "en": "croatia", "hr": "hrvatska", "fr": "croatie",
    "nl": "kroatie", "pl": "chorwacja", "cz": "chorvatsko", "sk": "chorvatsko",
    "ru": "horvatiya", "gr": "kroatia", "sw": "kroatien", "no": "kroatia",
}

def set_language(request):
    """
    Bestimmt die aktuelle Sprache:
    1. Zuerst aus der URL (z.B. /en/about/ -> 'en')
    2. Dann aus der Session
    3. Fallback: 'ge' (Deutsch)
    """
    # Versuche Sprache aus URL zu extrahieren
    path = request.path
    url_lang = None
    
    # Pattern: /{lang}/... wobei lang ein 2-Buchstaben Code ist
    if len(path) >= 4 and path[0] == '/' and path[3] == '/':
        potential_lang = path[1:3]
        if potential_lang in ALL_LANGUAGES:
            url_lang = potential_lang
    
    # Sprache bestimmen: URL > Session > Default
    if url_lang:
        lang = url_lang
        # Session aktualisieren, damit sie konsistent bleibt
        request.session['site_language'] = lang
    else:
        lang = request.session.get('site_language', 'ge')
    
    activate(lang)
    return {'language': lang}


def get_my_translations(request):
    current_path = request.path
    
    # Sprachcode aus Pfad entfernen (z.B. /ge/about/ -> /about/)
    import re
    clean_path = re.sub(r'^/[a-z]{2}/', '/', current_path)
    if clean_path == '':
        clean_path = '/'
    
    page = 'home'
    if clean_path == '/': page = 'home'
    elif '/about/' in clean_path: page = 'about'
    elif '/listing/' in clean_path: page = 'listings'
    elif '/profile/' in clean_path: page = 'profile'
    elif '/blog-single' in clean_path: page = 'blog details'
    elif '/blog/' in clean_path: page = 'blog'
    elif '/contact/' in clean_path: page = 'contact'
    elif '/login' in clean_path: page = 'login'
    elif '/register' in clean_path: page = 'signup'
    elif '/property-details/' in clean_path: page = 'property details'
    elif '/add-property/' in clean_path: page = 'add-property'
    elif '/privacy/' in clean_path: page = 'privacy'
    elif '/forget-password/' in clean_path: page = 'forget-password'
    elif '/verify-otp/' in clean_path: page = 'reset-password'
    elif '/agent/' in clean_path: page = 'profile'
    elif '/edit-agent/' in clean_path: page = 'signup'
    elif '/faq/' in clean_path: page = 'faq'

    user_language = request.session.get('site_language', 'ge')

    context = {}
    # Lade alle Übersetzungen für die aktuelle Seite, navbar, footer und home
    translations = Translation.objects.filter(page=page) | Translation.objects.filter(page='navbar') | Translation.objects.filter(page='footer') | Translation.objects.filter(page='listings') | Translation.objects.filter(page='property details') | Translation.objects.filter(page='home') | Translation.objects.filter(page='contact')
    for t in translations:
        if user_language == 'en': context[t.name] = t.english_content
        elif user_language == 'ge': context[t.name] = t.german_content
        elif user_language == 'fr': context[t.name] = t.french_content
        elif user_language == 'gr': context[t.name] = t.greek_content
        elif user_language == 'hr': context[t.name] = t.croatian_content
        elif user_language == 'pl': context[t.name] = t.polish_content
        elif user_language == 'cz': context[t.name] = t.czech_content
        elif user_language == 'ru': context[t.name] = t.russian_content
        elif user_language == 'sw': context[t.name] = t.swedish_content
        elif user_language == 'no': context[t.name] = t.norway_content
        elif user_language == 'sk': context[t.name] = t.slovak_content
        elif user_language == 'nl': context[t.name] = t.dutch_content
        else: context[t.name] = t.german_content  # Fallback zu Deutsch

    # URL-Variablen für Dienstleister hinzufügen
    context['country_name'] = COUNTRY_NAMES.get(user_language, 'kroatien')
    context['url_realtor'] = CATEGORY_URLS['real_estate_agent'].get(user_language, 'immobilienmakler')
    context['url_contractor'] = CATEGORY_URLS['construction_company'].get(user_language, 'bauunternehmen')
    context['url_lawyer'] = CATEGORY_URLS['lawyer'].get(user_language, 'rechtsanwaelte')
    context['url_tax_advisor'] = CATEGORY_URLS['tax_advisor'].get(user_language, 'steuerberater')
    context['url_architect'] = CATEGORY_URLS['architect'].get(user_language, 'architekten')
    
    # === SPRACH-URLs für Sprachumschalter ===
    # Generiere für die aktuelle Seite die korrekten URLs in allen Sprachen
    context['language_urls_json'] = get_language_urls_for_path(current_path, user_language)

    return context


def get_language_urls_for_path(current_path: str, current_lang: str) -> str:
    """
    Generiert ein JSON-Objekt mit den korrekten URLs für alle Sprachen.
    
    Unterstützte Seiten-Typen:
    - Glossar-Index: /{lang}/{country}/{glossar}/
    - Glossar-Detail: /{lang}/{country}/{glossar}/{slug}/
    - Buyer-Guide: /{lang}/{country}/{glossar}/buyer-guide/
    - Disclaimer: /{lang}/{country}/{glossar}/disclaimer/
    - Investors: /{lang}/{country}/{glossar}/investors/
    - Holiday: /{lang}/{country}/{glossar}/holiday-properties/
    - Luxury: /{lang}/{country}/{glossar}/luxury-real-estate/
    - Sitemap: /sitemap/
    - Statische Seiten ohne Sprachpräfix: /contact/, /about/, etc.
    """
    urls = {}
    
    # Pattern für Glossar-Seiten erkennen
    # z.B. /ge/kroatien/glossar/buyer-guide/
    glossary_pattern = re.compile(
        r'^/([a-z]{2})/([^/]+)/(' + '|'.join(GLOSSARY_URLS.values()) + r')/?(.*)$'
    )
    
    match = glossary_pattern.match(current_path)
    
    if match:
        # Es ist eine Glossar-bezogene Seite
        source_lang = match.group(1)
        source_country = match.group(2)
        source_glossary_slug = match.group(3)
        remainder = match.group(4).strip('/')
        
        for lang in ALL_LANGUAGES:
            country = COUNTRY_NAMES.get(lang, 'kroatien')
            glossary = GLOSSARY_URLS.get(lang, 'glossar')
            
            if remainder:
                # Sub-Seite (buyer-guide, disclaimer, investors, etc.)
                # Diese haben feste Slugs die nicht übersetzt werden
                urls[lang] = f"/{lang}/{country}/{glossary}/{remainder}/"
            else:
                # Glossar-Index
                urls[lang] = f"/{lang}/{country}/{glossary}/"
    
    elif current_path == '/sitemap/' or current_path == '/sitemap':
        # Sitemap unterstützt jetzt Sprachpräfixe
        for lang in ALL_LANGUAGES:
            if lang == 'ge':
                urls[lang] = '/sitemap/'  # Default Sprache ohne Präfix
            else:
                urls[lang] = f'/{lang}/sitemap/'
    
    else:
        # Statische Seiten (/contact/, /about/, /faq/, etc.)
        # Entferne bestehendes Sprachpräfix falls vorhanden
        clean_path = re.sub(r'^/[a-z]{2}/', '/', current_path)
        if not clean_path or clean_path == '':
            clean_path = '/'
        
        for lang in ALL_LANGUAGES:
            if lang == 'ge':
                # Deutsche URLs ohne Präfix (Default)
                urls[lang] = clean_path
            else:
                # Andere Sprachen mit Präfix
                urls[lang] = f'/{lang}{clean_path}'
    
    return json.dumps(urls)


# ============================================
# HERO SECTION TRANSLATIONS (Homepage)
# ============================================

HERO_TRANSLATIONS = {
    "ge": {
        "hero_tagline": "Kroatien · Adria · Mittelmeer",
        "hero_title": "Exklusive Immobilien<br>an der kroatischen Küste",
        "hero_subtitle": "Verifizierte Makler und persönliche Beratung für Ihre Traumimmobilie.",
    },
    "en": {
        "hero_tagline": "Croatia · Adriatic · Mediterranean",
        "hero_title": "Exclusive Properties<br>on the Croatian Coast",
        "hero_subtitle": "Verified agents and personal consultation for your dream property.",
    },
    "hr": {
        "hero_tagline": "Hrvatska · Jadran · Mediteran",
        "hero_title": "Ekskluzivne nekretnine<br>na hrvatskoj obali",
        "hero_subtitle": "Verificirani agenti i osobno savjetovanje za Vašu nekretninu iz snova.",
    },
    "fr": {
        "hero_tagline": "Croatie · Adriatique · Méditerranée",
        "hero_title": "Propriétés exclusives<br>sur la côte croate",
        "hero_subtitle": "Agents vérifiés et conseil personnalisé pour votre propriété de rêve.",
    },
    "nl": {
        "hero_tagline": "Kroatië · Adriatische Zee · Middellandse Zee",
        "hero_title": "Exclusief vastgoed<br>aan de Kroatische kust",
        "hero_subtitle": "Geverifieerde makelaars en persoonlijk advies voor uw droomwoning.",
    },
    "pl": {
        "hero_tagline": "Chorwacja · Adriatyk · Morze Śródziemne",
        "hero_title": "Ekskluzywne nieruchomości<br>na chorwackim wybrzeżu",
        "hero_subtitle": "Zweryfikowani agenci i osobiste doradztwo dla Twojej wymarzonej nieruchomości.",
    },
    "cz": {
        "hero_tagline": "Chorvatsko · Jadran · Středomoří",
        "hero_title": "Exkluzivní nemovitosti<br>na chorvatském pobřeží",
        "hero_subtitle": "Ověření makléři a osobní poradenství pro Vaši vysněnou nemovitost.",
    },
    "sk": {
        "hero_tagline": "Chorvátsko · Jadran · Stredomorie",
        "hero_title": "Exkluzívne nehnuteľnosti<br>na chorvátskom pobreží",
        "hero_subtitle": "Overení makléri a osobné poradenstvo pre Vašu vysnívanú nehnuteľnosť.",
    },
    "ru": {
        "hero_tagline": "Хорватия · Адриатика · Средиземноморье",
        "hero_title": "Эксклюзивная недвижимость<br>на хорватском побережье",
        "hero_subtitle": "Проверенные агенты и персональные консультации для вашей мечты.",
    },
    "gr": {
        "hero_tagline": "Κροατία · Αδριατική · Μεσόγειος",
        "hero_title": "Αποκλειστικά ακίνητα<br>στην κροατική ακτή",
        "hero_subtitle": "Πιστοποιημένοι μεσίτες και προσωπική συμβουλευτική για το ακίνητο των ονείρων σας.",
    },
    "sw": {
        "hero_tagline": "Kroatien · Adriatiska havet · Medelhavet",
        "hero_title": "Exklusiva fastigheter<br>vid den kroatiska kusten",
        "hero_subtitle": "Verifierade mäklare och personlig rådgivning för din drömbostad.",
    },
    "no": {
        "hero_tagline": "Kroatia · Adriaterhavet · Middelhavet",
        "hero_title": "Eksklusive eiendommer<br>ved den kroatiske kysten",
        "hero_subtitle": "Verifiserte meglere og personlig rådgivning for din drømmebolig.",
    },
}


def hero_translations(request):
    """
    Liefert Hero-Übersetzungen für die Homepage.
    """
    user_language = request.session.get('site_language', 'ge')
    translations = HERO_TRANSLATIONS.get(user_language, HERO_TRANSLATIONS['ge'])
    return translations


# ============================================
# SITEMAP TRANSLATIONS
# ============================================

SITEMAP_TRANSLATIONS = {
    "ge": {
        # Page Title & Header
        "sm_page_title": "Sitemap",
        "sm_page_subtitle": "Vollständiger Überblick aller Seiten",
        "sm_meta_desc": "Vollständige Sitemap von 123-Kroatien.eu - Ihr Wegweiser zu kroatischen Immobilien",
        
        # Section Headers
        "sm_main_pages": "Hauptseiten",
        "sm_legal": "Rechtliches",
        "sm_providers": "Dienstleister Kroatien",
        "sm_user_area": "Benutzer-Bereich",
        "sm_services": "Service",
        "sm_ai": "KI",
        "sm_seo_links": "SEO & Technische Links",
        "sm_languages": "Verfügbare Sprachen",
        
        # Main Pages Links
        "sm_home": "Startseite",
        "sm_all_properties": "Alle Immobilien",
        "sm_about": "Über uns",
        "sm_contact": "Kontakt",
        "sm_faq": "FAQ",
        
        # Legal Links
        "sm_imprint": "Impressum",
        "sm_privacy": "Datenschutz",
        "sm_terms": "AGB",
        "sm_cancellation": "Widerrufsrecht",
        "sm_disclaimer": "Haftungsausschluss",
        
        # Service Providers
        "sm_realtor": "Immobilienmakler",
        "sm_contractor": "Bauunternehmer",
        "sm_lawyer": "Rechtsanwalt",
        "sm_tax_advisor": "Steuerberater",
        "sm_architect": "Architekt",
        
        # User Area
        "sm_become_partner": "Partner werden",
        "sm_register": "Registrieren",
        "sm_login": "Anmelden",
        "sm_agent_portal": "Makler-Portal",
        "sm_forgot_password": "Passwort vergessen",
        
        # Services
        "sm_glossary": "Immobilien-Glossar",
        "sm_buyer_guide": "Käufer Kurzleitfaden",
        "sm_market_reports": "Marktberichte",
        "sm_addresses": "Wichtige Adressen",
        "sm_news": "Nachrichten",
        
        # AI
        "sm_ai_search": "KI Immobilien Schnellsuche",
        "sm_expert_finder": "Expertenfinder",
    },
    "en": {
        "sm_page_title": "Sitemap",
        "sm_page_subtitle": "Complete overview of all pages",
        "sm_meta_desc": "Complete sitemap of 123-Kroatien.eu - Your guide to Croatian real estate",
        "sm_main_pages": "Main Pages",
        "sm_legal": "Legal",
        "sm_providers": "Service Providers",
        "sm_user_area": "User Area",
        "sm_services": "Services",
        "sm_ai": "Artificial Intelligence",
        "sm_seo_links": "SEO & Technical Links",
        "sm_languages": "Available Languages",
        "sm_home": "Home",
        "sm_all_properties": "All Properties",
        "sm_about": "About Us",
        "sm_contact": "Contact",
        "sm_faq": "FAQ",
        "sm_imprint": "Imprint",
        "sm_privacy": "Privacy Policy",
        "sm_terms": "Terms & Conditions",
        "sm_cancellation": "Cancellation Policy",
        "sm_disclaimer": "Disclaimer",
        "sm_realtor": "Real Estate Agent",
        "sm_contractor": "Building Contractor",
        "sm_lawyer": "Lawyer",
        "sm_tax_advisor": "Tax Advisor",
        "sm_architect": "Architect",
        "sm_become_partner": "Become a Partner",
        "sm_register": "Register",
        "sm_login": "Login",
        "sm_agent_portal": "Agent Portal",
        "sm_forgot_password": "Forgot Password",
        "sm_glossary": "Real Estate Glossary",
        "sm_buyer_guide": "Buyer Guide",
        "sm_market_reports": "Market Reports",
        "sm_addresses": "Important Addresses",
        "sm_news": "News",
        "sm_ai_search": "AI Property Quick Search",
        "sm_expert_finder": "Expert Finder",
    },
    "hr": {
        "sm_page_title": "Mapa stranica",
        "sm_page_subtitle": "Kompletan pregled svih stranica",
        "sm_meta_desc": "Kompletna mapa stranica 123-Kroatien.eu - Vaš vodič kroz hrvatske nekretnine",
        "sm_main_pages": "Glavne stranice",
        "sm_legal": "Pravne informacije",
        "sm_providers": "Pružatelji usluga",
        "sm_user_area": "Korisnički prostor",
        "sm_services": "Usluge",
        "sm_ai": "Umjetna inteligencija",
        "sm_seo_links": "SEO & Tehničke poveznice",
        "sm_languages": "Dostupni jezici",
        "sm_home": "Početna",
        "sm_all_properties": "Sve nekretnine",
        "sm_about": "O nama",
        "sm_contact": "Kontakt",
        "sm_faq": "Česta pitanja",
        "sm_imprint": "Impressum",
        "sm_privacy": "Zaštita podataka",
        "sm_terms": "Uvjeti korištenja",
        "sm_cancellation": "Pravo na odustanak",
        "sm_disclaimer": "Odricanje odgovornosti",
        "sm_realtor": "Agent za nekretnine",
        "sm_contractor": "Građevinar",
        "sm_lawyer": "Odvjetnik",
        "sm_tax_advisor": "Porezni savjetnik",
        "sm_architect": "Arhitekt",
        "sm_become_partner": "Postanite partner",
        "sm_register": "Registracija",
        "sm_login": "Prijava",
        "sm_agent_portal": "Portal za agente",
        "sm_forgot_password": "Zaboravljena lozinka",
        "sm_glossary": "Pojmovnik nekretnina",
        "sm_buyer_guide": "Vodič za kupce",
        "sm_market_reports": "Tržišni izvještaji",
        "sm_addresses": "Važne adrese",
        "sm_news": "Vijesti",
        "sm_ai_search": "AI brza pretraga nekretnina",
        "sm_expert_finder": "Tražilica stručnjaka",
    },
    "fr": {
        "sm_page_title": "Plan du site",
        "sm_page_subtitle": "Aperçu complet de toutes les pages",
        "sm_meta_desc": "Plan du site complet de 123-Kroatien.eu - Votre guide de l'immobilier croate",
        "sm_main_pages": "Pages principales",
        "sm_legal": "Mentions légales",
        "sm_providers": "Prestataires de services",
        "sm_user_area": "Espace utilisateur",
        "sm_services": "Services",
        "sm_ai": "Intelligence artificielle",
        "sm_seo_links": "SEO & Liens techniques",
        "sm_languages": "Langues disponibles",
        "sm_home": "Accueil",
        "sm_all_properties": "Toutes les propriétés",
        "sm_about": "À propos",
        "sm_contact": "Contact",
        "sm_faq": "FAQ",
        "sm_imprint": "Mentions légales",
        "sm_privacy": "Politique de confidentialité",
        "sm_terms": "Conditions générales",
        "sm_cancellation": "Droit de rétractation",
        "sm_disclaimer": "Avertissement",
        "sm_realtor": "Agent immobilier",
        "sm_contractor": "Entrepreneur",
        "sm_lawyer": "Avocat",
        "sm_tax_advisor": "Conseiller fiscal",
        "sm_architect": "Architecte",
        "sm_become_partner": "Devenir partenaire",
        "sm_register": "S'inscrire",
        "sm_login": "Connexion",
        "sm_agent_portal": "Portail agents",
        "sm_forgot_password": "Mot de passe oublié",
        "sm_glossary": "Glossaire immobilier",
        "sm_buyer_guide": "Guide de l'acheteur",
        "sm_market_reports": "Rapports de marché",
        "sm_addresses": "Adresses importantes",
        "sm_news": "Actualités",
        "sm_ai_search": "Recherche rapide IA",
        "sm_expert_finder": "Recherche d'experts",
    },
    "nl": {
        "sm_page_title": "Sitemap",
        "sm_page_subtitle": "Volledig overzicht van alle pagina's",
        "sm_meta_desc": "Volledige sitemap van 123-Kroatien.eu - Uw gids voor Kroatisch vastgoed",
        "sm_main_pages": "Hoofdpagina's",
        "sm_legal": "Juridisch",
        "sm_providers": "Dienstverleners",
        "sm_user_area": "Gebruikersgebied",
        "sm_services": "Diensten",
        "sm_ai": "Kunstmatige intelligentie",
        "sm_seo_links": "SEO & Technische links",
        "sm_languages": "Beschikbare talen",
        "sm_home": "Home",
        "sm_all_properties": "Alle vastgoed",
        "sm_about": "Over ons",
        "sm_contact": "Contact",
        "sm_faq": "FAQ",
        "sm_imprint": "Colofon",
        "sm_privacy": "Privacybeleid",
        "sm_terms": "Algemene voorwaarden",
        "sm_cancellation": "Herroepingsrecht",
        "sm_disclaimer": "Disclaimer",
        "sm_realtor": "Makelaar",
        "sm_contractor": "Aannemer",
        "sm_lawyer": "Advocaat",
        "sm_tax_advisor": "Belastingadviseur",
        "sm_architect": "Architect",
        "sm_become_partner": "Partner worden",
        "sm_register": "Registreren",
        "sm_login": "Inloggen",
        "sm_agent_portal": "Makelaarsportaal",
        "sm_forgot_password": "Wachtwoord vergeten",
        "sm_glossary": "Vastgoed woordenlijst",
        "sm_buyer_guide": "Koopgids",
        "sm_market_reports": "Marktverslagen",
        "sm_addresses": "Belangrijke adressen",
        "sm_news": "Nieuws",
        "sm_ai_search": "AI snel zoeken",
        "sm_expert_finder": "Expertzoeker",
    },
    "pl": {
        "sm_page_title": "Mapa strony",
        "sm_page_subtitle": "Pełny przegląd wszystkich stron",
        "sm_meta_desc": "Kompletna mapa strony 123-Kroatien.eu - Twój przewodnik po chorwackich nieruchomościach",
        "sm_main_pages": "Strony główne",
        "sm_legal": "Informacje prawne",
        "sm_providers": "Usługodawcy",
        "sm_user_area": "Strefa użytkownika",
        "sm_services": "Usługi",
        "sm_ai": "Sztuczna inteligencja",
        "sm_seo_links": "SEO & Linki techniczne",
        "sm_languages": "Dostępne języki",
        "sm_home": "Strona główna",
        "sm_all_properties": "Wszystkie nieruchomości",
        "sm_about": "O nas",
        "sm_contact": "Kontakt",
        "sm_faq": "FAQ",
        "sm_imprint": "Impressum",
        "sm_privacy": "Polityka prywatności",
        "sm_terms": "Regulamin",
        "sm_cancellation": "Prawo odstąpienia",
        "sm_disclaimer": "Zastrzeżenia",
        "sm_realtor": "Agent nieruchomości",
        "sm_contractor": "Wykonawca",
        "sm_lawyer": "Prawnik",
        "sm_tax_advisor": "Doradca podatkowy",
        "sm_architect": "Architekt",
        "sm_become_partner": "Zostań partnerem",
        "sm_register": "Rejestracja",
        "sm_login": "Logowanie",
        "sm_agent_portal": "Portal agenta",
        "sm_forgot_password": "Zapomniałeś hasła",
        "sm_glossary": "Słownik nieruchomości",
        "sm_buyer_guide": "Przewodnik kupującego",
        "sm_market_reports": "Raporty rynkowe",
        "sm_addresses": "Ważne adresy",
        "sm_news": "Wiadomości",
        "sm_ai_search": "Szybkie wyszukiwanie AI",
        "sm_expert_finder": "Wyszukiwarka ekspertów",
    },
    "cz": {
        "sm_page_title": "Mapa stránek",
        "sm_page_subtitle": "Kompletní přehled všech stránek",
        "sm_meta_desc": "Kompletní mapa stránek 123-Kroatien.eu - Váš průvodce chorvatskými nemovitostmi",
        "sm_main_pages": "Hlavní stránky",
        "sm_legal": "Právní informace",
        "sm_providers": "Poskytovatelé služeb",
        "sm_user_area": "Uživatelská zóna",
        "sm_services": "Služby",
        "sm_ai": "Umělá inteligence",
        "sm_seo_links": "SEO & Technické odkazy",
        "sm_languages": "Dostupné jazyky",
        "sm_home": "Domů",
        "sm_all_properties": "Všechny nemovitosti",
        "sm_about": "O nás",
        "sm_contact": "Kontakt",
        "sm_faq": "FAQ",
        "sm_imprint": "Impressum",
        "sm_privacy": "Ochrana údajů",
        "sm_terms": "Obchodní podmínky",
        "sm_cancellation": "Právo na odstoupení",
        "sm_disclaimer": "Prohlášení",
        "sm_realtor": "Realitní makléř",
        "sm_contractor": "Stavitel",
        "sm_lawyer": "Právník",
        "sm_tax_advisor": "Daňový poradce",
        "sm_architect": "Architekt",
        "sm_become_partner": "Staňte se partnerem",
        "sm_register": "Registrace",
        "sm_login": "Přihlášení",
        "sm_agent_portal": "Portál makléře",
        "sm_forgot_password": "Zapomenuté heslo",
        "sm_glossary": "Realitní glosář",
        "sm_buyer_guide": "Průvodce kupujícího",
        "sm_market_reports": "Tržní zprávy",
        "sm_addresses": "Důležité adresy",
        "sm_news": "Zprávy",
        "sm_ai_search": "AI rychlé vyhledávání",
        "sm_expert_finder": "Vyhledávač odborníků",
    },
    "sk": {
        "sm_page_title": "Mapa stránok",
        "sm_page_subtitle": "Kompletný prehľad všetkých stránok",
        "sm_meta_desc": "Kompletná mapa stránok 123-Kroatien.eu - Váš sprievodca chorvátskymi nehnuteľnosťami",
        "sm_main_pages": "Hlavné stránky",
        "sm_legal": "Právne informácie",
        "sm_providers": "Poskytovatelia služieb",
        "sm_user_area": "Používateľská zóna",
        "sm_services": "Služby",
        "sm_ai": "Umelá inteligencia",
        "sm_seo_links": "SEO & Technické odkazy",
        "sm_languages": "Dostupné jazyky",
        "sm_home": "Domov",
        "sm_all_properties": "Všetky nehnuteľnosti",
        "sm_about": "O nás",
        "sm_contact": "Kontakt",
        "sm_faq": "FAQ",
        "sm_imprint": "Impressum",
        "sm_privacy": "Ochrana údajov",
        "sm_terms": "Obchodné podmienky",
        "sm_cancellation": "Právo na odstúpenie",
        "sm_disclaimer": "Vyhlásenie",
        "sm_realtor": "Realitný maklér",
        "sm_contractor": "Staviteľ",
        "sm_lawyer": "Právnik",
        "sm_tax_advisor": "Daňový poradca",
        "sm_architect": "Architekt",
        "sm_become_partner": "Staňte sa partnerom",
        "sm_register": "Registrácia",
        "sm_login": "Prihlásenie",
        "sm_agent_portal": "Portál makléra",
        "sm_forgot_password": "Zabudnuté heslo",
        "sm_glossary": "Realitný slovník",
        "sm_buyer_guide": "Sprievodca kupujúceho",
        "sm_market_reports": "Trhové správy",
        "sm_addresses": "Dôležité adresy",
        "sm_news": "Správy",
        "sm_ai_search": "AI rýchle vyhľadávanie",
        "sm_expert_finder": "Vyhľadávač odborníkov",
    },
    "ru": {
        "sm_page_title": "Карта сайта",
        "sm_page_subtitle": "Полный обзор всех страниц",
        "sm_meta_desc": "Полная карта сайта 123-Kroatien.eu - Ваш путеводитель по хорватской недвижимости",
        "sm_main_pages": "Главные страницы",
        "sm_legal": "Юридическая информация",
        "sm_providers": "Поставщики услуг",
        "sm_user_area": "Личный кабинет",
        "sm_services": "Услуги",
        "sm_ai": "Искусственный интеллект",
        "sm_seo_links": "SEO & Технические ссылки",
        "sm_languages": "Доступные языки",
        "sm_home": "Главная",
        "sm_all_properties": "Вся недвижимость",
        "sm_about": "О нас",
        "sm_contact": "Контакт",
        "sm_faq": "FAQ",
        "sm_imprint": "Выходные данные",
        "sm_privacy": "Политика конфиденциальности",
        "sm_terms": "Условия использования",
        "sm_cancellation": "Право отмены",
        "sm_disclaimer": "Отказ от ответственности",
        "sm_realtor": "Риэлтор",
        "sm_contractor": "Подрядчик",
        "sm_lawyer": "Адвокат",
        "sm_tax_advisor": "Налоговый консультант",
        "sm_architect": "Архитектор",
        "sm_become_partner": "Стать партнером",
        "sm_register": "Регистрация",
        "sm_login": "Вход",
        "sm_agent_portal": "Портал агента",
        "sm_forgot_password": "Забыли пароль",
        "sm_glossary": "Глоссарий недвижимости",
        "sm_buyer_guide": "Руководство покупателя",
        "sm_market_reports": "Рыночные отчеты",
        "sm_addresses": "Важные адреса",
        "sm_news": "Новости",
        "sm_ai_search": "Быстрый поиск ИИ",
        "sm_expert_finder": "Поиск экспертов",
    },
    "gr": {
        "sm_page_title": "Χάρτης ιστοτόπου",
        "sm_page_subtitle": "Πλήρης επισκόπηση όλων των σελίδων",
        "sm_meta_desc": "Πλήρης χάρτης ιστοτόπου 123-Kroatien.eu - Ο οδηγός σας για κροατικά ακίνητα",
        "sm_main_pages": "Κύριες σελίδες",
        "sm_legal": "Νομικές πληροφορίες",
        "sm_providers": "Πάροχοι υπηρεσιών",
        "sm_user_area": "Περιοχή χρήστη",
        "sm_services": "Υπηρεσίες",
        "sm_ai": "Τεχνητή νοημοσύνη",
        "sm_seo_links": "SEO & Τεχνικοί σύνδεσμοι",
        "sm_languages": "Διαθέσιμες γλώσσες",
        "sm_home": "Αρχική",
        "sm_all_properties": "Όλα τα ακίνητα",
        "sm_about": "Σχετικά με εμάς",
        "sm_contact": "Επικοινωνία",
        "sm_faq": "FAQ",
        "sm_imprint": "Impressum",
        "sm_privacy": "Πολιτική απορρήτου",
        "sm_terms": "Όροι χρήσης",
        "sm_cancellation": "Πολιτική ακύρωσης",
        "sm_disclaimer": "Αποποίηση ευθύνης",
        "sm_realtor": "Μεσίτης",
        "sm_contractor": "Κατασκευαστής",
        "sm_lawyer": "Δικηγόρος",
        "sm_tax_advisor": "Φοροτεχνικός",
        "sm_architect": "Αρχιτέκτονας",
        "sm_become_partner": "Γίνετε συνεργάτης",
        "sm_register": "Εγγραφή",
        "sm_login": "Σύνδεση",
        "sm_agent_portal": "Πύλη μεσίτη",
        "sm_forgot_password": "Ξεχάσατε τον κωδικό",
        "sm_glossary": "Γλωσσάριο ακινήτων",
        "sm_buyer_guide": "Οδηγός αγοραστή",
        "sm_market_reports": "Αναφορές αγοράς",
        "sm_addresses": "Σημαντικές διευθύνσεις",
        "sm_news": "Νέα",
        "sm_ai_search": "AI γρήγορη αναζήτηση",
        "sm_expert_finder": "Εύρεση ειδικών",
    },
    "sw": {
        "sm_page_title": "Webbplatskarta",
        "sm_page_subtitle": "Fullständig översikt över alla sidor",
        "sm_meta_desc": "Komplett webbplatskarta för 123-Kroatien.eu - Din guide till kroatiska fastigheter",
        "sm_main_pages": "Huvudsidor",
        "sm_legal": "Juridisk information",
        "sm_providers": "Tjänsteleverantörer",
        "sm_user_area": "Användarområde",
        "sm_services": "Tjänster",
        "sm_ai": "Artificiell intelligens",
        "sm_seo_links": "SEO & Tekniska länkar",
        "sm_languages": "Tillgängliga språk",
        "sm_home": "Hem",
        "sm_all_properties": "Alla fastigheter",
        "sm_about": "Om oss",
        "sm_contact": "Kontakt",
        "sm_faq": "FAQ",
        "sm_imprint": "Impressum",
        "sm_privacy": "Integritetspolicy",
        "sm_terms": "Allmänna villkor",
        "sm_cancellation": "Ångerrätt",
        "sm_disclaimer": "Ansvarsfriskrivning",
        "sm_realtor": "Fastighetsmäklare",
        "sm_contractor": "Byggentreprenör",
        "sm_lawyer": "Advokat",
        "sm_tax_advisor": "Skatterådgivare",
        "sm_architect": "Arkitekt",
        "sm_become_partner": "Bli partner",
        "sm_register": "Registrera",
        "sm_login": "Logga in",
        "sm_agent_portal": "Mäklarportal",
        "sm_forgot_password": "Glömt lösenord",
        "sm_glossary": "Fastighetsordlista",
        "sm_buyer_guide": "Köparguide",
        "sm_market_reports": "Marknadsrapporter",
        "sm_addresses": "Viktiga adresser",
        "sm_news": "Nyheter",
        "sm_ai_search": "AI snabbsökning",
        "sm_expert_finder": "Expertsökare",
    },
    "no": {
        "sm_page_title": "Nettstedkart",
        "sm_page_subtitle": "Fullstendig oversikt over alle sider",
        "sm_meta_desc": "Komplett nettstedskart for 123-Kroatien.eu - Din guide til kroatisk eiendom",
        "sm_main_pages": "Hovedsider",
        "sm_legal": "Juridisk informasjon",
        "sm_providers": "Tjenesteleverandører",
        "sm_user_area": "Brukerområde",
        "sm_services": "Tjenester",
        "sm_ai": "Kunstig intelligens",
        "sm_seo_links": "SEO & Tekniske lenker",
        "sm_languages": "Tilgjengelige språk",
        "sm_home": "Hjem",
        "sm_all_properties": "Alle eiendommer",
        "sm_about": "Om oss",
        "sm_contact": "Kontakt",
        "sm_faq": "FAQ",
        "sm_imprint": "Impressum",
        "sm_privacy": "Personvernpolicy",
        "sm_terms": "Vilkår og betingelser",
        "sm_cancellation": "Angrerett",
        "sm_disclaimer": "Ansvarsfraskrivelse",
        "sm_realtor": "Eiendomsmegler",
        "sm_contractor": "Byggentreprenør",
        "sm_lawyer": "Advokat",
        "sm_tax_advisor": "Skatterådgiver",
        "sm_architect": "Arkitekt",
        "sm_become_partner": "Bli partner",
        "sm_register": "Registrer",
        "sm_login": "Logg inn",
        "sm_agent_portal": "Meglerportal",
        "sm_forgot_password": "Glemt passord",
        "sm_glossary": "Eiendomsordliste",
        "sm_buyer_guide": "Kjøperguide",
        "sm_market_reports": "Markedsrapporter",
        "sm_addresses": "Viktige adresser",
        "sm_news": "Nyheter",
        "sm_ai_search": "AI hurtigsøk",
        "sm_expert_finder": "Ekspertfinner",
    },
}

# URL-Segmente für Sitemap (mehrsprachige Pfade)
SITEMAP_URL_SEGMENTS = {
    "glossary": GLOSSARY_URLS,
    "partner": {
        "ge": "partner-werden", "en": "become-partner", "hr": "postanite-partner",
        "fr": "devenir-partenaire", "nl": "partner-worden", "pl": "zostan-partnerem",
        "cz": "stanat-se-partnerem", "sk": "stat-sa-partnerom", "ru": "stat-partnerom",
        "gr": "gineite-synergatis", "sw": "bli-partner", "no": "bli-partner",
    },
    "registration": {
        "ge": "registrierung", "en": "registration", "hr": "registracija",
        "fr": "inscription", "nl": "registratie", "pl": "rejestracja",
        "cz": "registrace", "sk": "registracia", "ru": "registratsiya",
        "gr": "eggraphi", "sw": "registrering", "no": "registrering",
    },
    "expert_finder": {
        "ge": "experten-finder", "en": "expert-finder", "hr": "pronalazac-strucnjaka",
        "fr": "recherche-experts", "nl": "expert-zoeker", "pl": "wyszukiwarka-ekspertow",
        "cz": "vyhledavac-odborniku", "sk": "vyhladavac-odbornikov", "ru": "poisk-ekspertov",
        "gr": "anazhthsh-eidikwn", "sw": "expert-sokare", "no": "ekspert-soker",
    },
    "market_reports": {
        "ge": "marktberichte", "en": "market-reports", "hr": "trzisni-izvjestaji",
        "fr": "rapports-marche", "nl": "marktverslagen", "pl": "raporty-rynkowe",
        "cz": "trzni-zpravy", "sk": "trhove-spravy", "ru": "rynochnye-otchety",
        "gr": "anafores-agoras", "sw": "marknadsrapporter", "no": "markedsrapporter",
    },
    "addresses": {
        "ge": "wichtige-adressen", "en": "important-addresses", "hr": "vazne-adrese",
        "fr": "adresses-importantes", "nl": "belangrijke-adressen", "pl": "wazne-adresy",
        "cz": "dulezite-adresy", "sk": "dolezite-adresy", "ru": "vazhnye-adresa",
        "gr": "simantikes-dieythynseis", "sw": "viktiga-adresser", "no": "viktige-adresser",
    },
    "news": {
        "ge": "nachrichten", "en": "news", "hr": "vijesti",
        "fr": "actualites", "nl": "nieuws", "pl": "wiadomosci",
        "cz": "zpravy", "sk": "spravy", "ru": "novosti",
        "gr": "nea", "sw": "nyheter", "no": "nyheter",
    },
}


def sitemap_translations(request):
    """
    Liefert alle Sitemap-Übersetzungen und dynamische URLs.
    """
    user_language = request.session.get('site_language', 'ge')
    
    # Text-Übersetzungen
    translations = SITEMAP_TRANSLATIONS.get(user_language, SITEMAP_TRANSLATIONS['ge'])
    
    # Dynamische URL-Segmente
    country = COUNTRY_NAMES.get(user_language, 'kroatien')
    glossary_segment = GLOSSARY_URLS.get(user_language, 'glossar')
    
    # URL-Segmente für die aktuelle Sprache
    url_segments = {
        'url_country': country,
        'url_glossary': glossary_segment,
        'url_partner': SITEMAP_URL_SEGMENTS['partner'].get(user_language, 'partner-werden'),
        'url_registration': SITEMAP_URL_SEGMENTS['registration'].get(user_language, 'registrierung'),
        'url_expert_finder': SITEMAP_URL_SEGMENTS['expert_finder'].get(user_language, 'experten-finder'),
        'url_market_reports': SITEMAP_URL_SEGMENTS['market_reports'].get(user_language, 'marktberichte'),
        'url_addresses': SITEMAP_URL_SEGMENTS['addresses'].get(user_language, 'wichtige-adressen'),
        'url_news': SITEMAP_URL_SEGMENTS['news'].get(user_language, 'nachrichten'),
    }
    
    # Kombiniere alles
    return {**translations, **url_segments}


# ============================================
# SEO META TAGS (Open Graph & Twitter Cards)
# ============================================

SEO_META_TRANSLATIONS = {
    "ge": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Immobilien Kroatien | Häuser, Wohnungen & Villen an der Adria",
        "meta_default_description": "Finden Sie Ihre Traumimmobilie in Kroatien. Verifizierte Makler, exklusive Villen, Häuser und Wohnungen an der Adriaküste. Persönliche Beratung in 12 Sprachen.",
        "meta_default_keywords": "Immobilien Kroatien, Haus kaufen Kroatien, Villa Kroatien, Wohnung Adria, Ferienhaus Kroatien, Makler Kroatien",
    },
    "en": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Croatia Real Estate | Houses, Apartments & Villas on the Adriatic",
        "meta_default_description": "Find your dream property in Croatia. Verified agents, exclusive villas, houses and apartments on the Adriatic coast. Personal consultation in 12 languages.",
        "meta_default_keywords": "Croatia real estate, buy house Croatia, villa Croatia, apartment Adriatic, holiday home Croatia, real estate agent Croatia",
    },
    "hr": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Nekretnine Hrvatska | Kuće, Stanovi i Vile na Jadranu",
        "meta_default_description": "Pronađite svoju nekretninu iz snova u Hrvatskoj. Verificirani agenti, ekskluzivne vile, kuće i stanovi na jadranskoj obali. Osobno savjetovanje na 12 jezika.",
        "meta_default_keywords": "nekretnine Hrvatska, kupiti kuću Hrvatska, vila Hrvatska, stan Jadran, kuća za odmor Hrvatska, agent za nekretnine Hrvatska",
    },
    "fr": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Immobilier Croatie | Maisons, Appartements & Villas sur l'Adriatique",
        "meta_default_description": "Trouvez votre propriété de rêve en Croatie. Agents vérifiés, villas exclusives, maisons et appartements sur la côte adriatique. Conseil personnalisé en 12 langues.",
        "meta_default_keywords": "immobilier Croatie, acheter maison Croatie, villa Croatie, appartement Adriatique, maison de vacances Croatie, agent immobilier Croatie",
    },
    "nl": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Vastgoed Kroatië | Huizen, Appartementen & Villa's aan de Adriatische Zee",
        "meta_default_description": "Vind uw droomwoning in Kroatië. Geverifieerde makelaars, exclusieve villa's, huizen en appartementen aan de Adriatische kust. Persoonlijk advies in 12 talen.",
        "meta_default_keywords": "vastgoed Kroatië, huis kopen Kroatië, villa Kroatië, appartement Adriatische Zee, vakantiehuis Kroatië, makelaar Kroatië",
    },
    "pl": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Nieruchomości Chorwacja | Domy, Mieszkania i Wille nad Adriatykiem",
        "meta_default_description": "Znajdź wymarzoną nieruchomość w Chorwacji. Zweryfikowani agenci, ekskluzywne wille, domy i mieszkania na wybrzeżu Adriatyku. Osobiste doradztwo w 12 językach.",
        "meta_default_keywords": "nieruchomości Chorwacja, kupić dom Chorwacja, willa Chorwacja, mieszkanie Adriatyk, dom wakacyjny Chorwacja, agent nieruchomości Chorwacja",
    },
    "cz": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Nemovitosti Chorvatsko | Domy, Byty a Vily na Jadranu",
        "meta_default_description": "Najděte svou vysněnou nemovitost v Chorvatsku. Ověření makléři, exkluzivní vily, domy a byty na jadranském pobřeží. Osobní poradenství ve 12 jazycích.",
        "meta_default_keywords": "nemovitosti Chorvatsko, koupit dům Chorvatsko, vila Chorvatsko, byt Jadran, rekreační dům Chorvatsko, realitní makléř Chorvatsko",
    },
    "sk": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Nehnuteľnosti Chorvátsko | Domy, Byty a Vily na Jadrane",
        "meta_default_description": "Nájdite svoju vysnívanú nehnuteľnosť v Chorvátsku. Overení makléri, exkluzívne vily, domy a byty na jadranskom pobreží. Osobné poradenstvo v 12 jazykoch.",
        "meta_default_keywords": "nehnuteľnosti Chorvátsko, kúpiť dom Chorvátsko, vila Chorvátsko, byt Jadran, rekreačný dom Chorvátsko, realitný maklér Chorvátsko",
    },
    "ru": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Недвижимость Хорватия | Дома, Квартиры и Виллы на Адриатике",
        "meta_default_description": "Найдите недвижимость своей мечты в Хорватии. Проверенные агенты, эксклюзивные виллы, дома и квартиры на побережье Адриатики. Персональные консультации на 12 языках.",
        "meta_default_keywords": "недвижимость Хорватия, купить дом Хорватия, вилла Хорватия, квартира Адриатика, дом для отдыха Хорватия, агент недвижимости Хорватия",
    },
    "gr": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Ακίνητα Κροατία | Σπίτια, Διαμερίσματα & Βίλες στην Αδριατική",
        "meta_default_description": "Βρείτε το ακίνητο των ονείρων σας στην Κροατία. Πιστοποιημένοι μεσίτες, αποκλειστικές βίλες, σπίτια και διαμερίσματα στην ακτή της Αδριατικής. Προσωπική συμβουλευτική σε 12 γλώσσες.",
        "meta_default_keywords": "ακίνητα Κροατία, αγορά σπιτιού Κροατία, βίλα Κροατία, διαμέρισμα Αδριατική, εξοχικό Κροατία, μεσίτης Κροατία",
    },
    "sw": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Fastigheter Kroatien | Hus, Lägenheter & Villor vid Adriatiska havet",
        "meta_default_description": "Hitta din drömfastighet i Kroatien. Verifierade mäklare, exklusiva villor, hus och lägenheter vid Adriatiska kusten. Personlig rådgivning på 12 språk.",
        "meta_default_keywords": "fastigheter Kroatien, köpa hus Kroatien, villa Kroatien, lägenhet Adriatiska havet, semesterhus Kroatien, fastighetsmäklare Kroatien",
    },
    "no": {
        "meta_site_name": "123-Kroatien.eu",
        "meta_default_title": "Eiendom Kroatia | Hus, Leiligheter & Villaer ved Adriaterhavet",
        "meta_default_description": "Finn drømmeeiendommen din i Kroatia. Verifiserte meglere, eksklusive villaer, hus og leiligheter ved Adriaterhavskysten. Personlig rådgivning på 12 språk.",
        "meta_default_keywords": "eiendom Kroatia, kjøpe hus Kroatia, villa Kroatia, leilighet Adriaterhavet, feriehus Kroatia, eiendomsmegler Kroatia",
    },
}


def seo_meta_tags(request):
    """
    Liefert SEO Meta-Tags (Open Graph, Twitter Cards) für alle Seiten.
    Einzelne Seiten können diese überschreiben via Template-Blocks.
    """
    user_language = request.session.get('site_language', 'ge')
    meta = SEO_META_TRANSLATIONS.get(user_language, SEO_META_TRANSLATIONS['ge'])
    
    # Aktuelle URL für og:url
    current_url = request.build_absolute_uri()
    
    return {
        'meta_site_name': meta['meta_site_name'],
        'meta_title': meta['meta_default_title'],
        'meta_description': meta['meta_default_description'],
        'meta_keywords': meta['meta_default_keywords'],
        'meta_url': current_url,
        'meta_image': 'https://123-kroatien.eu/static/images/logo-full.png',
        'meta_type': 'website',
        'meta_twitter_card': 'summary_large_image',
    }


# ============================================
# BREADCRUMB TRANSLATIONS
# ============================================

BREADCRUMB_LABELS = {
    "ge": {
        "home": "Startseite",
        "listing": "Immobilien",
        "listings": "Immobilien",
        "about": "Über uns",
        "contact": "Kontakt",
        "faq": "FAQ",
        "blog": "Blog",
        "imprint": "Impressum",
        "data-protection": "Datenschutz",
        "agb": "AGB",
        "cancellation-policy": "Widerrufsrecht",
        "sitemap": "Sitemap",
        "service": "Service",
        "makler-dashboard": "Makler-Portal",
        "glossar": "Glossar",
        "glossary": "Glossar",
        "disclaimer": "Haftungsausschluss",
        "buyer-guide": "Käuferleitfaden",
        "immobilienmakler": "Immobilienmakler",
        "bauunternehmen": "Bauunternehmen",
        "rechtsanwaelte": "Rechtsanwälte",
        "steuerberater": "Steuerberater",
        "architekten": "Architekten",
        "partner-werden": "Partner werden",
        "registrierung": "Registrierung",
        "experten-finder": "Expertenfinder",
        "marktberichte": "Marktberichte",
        "wichtige-adressen": "Wichtige Adressen",
        "nachrichten": "Nachrichten",
        "kroatien": "Kroatien",
    },
    "en": {
        "home": "Home",
        "listing": "Properties",
        "listings": "Properties",
        "about": "About Us",
        "contact": "Contact",
        "faq": "FAQ",
        "blog": "Blog",
        "imprint": "Imprint",
        "data-protection": "Privacy Policy",
        "agb": "Terms & Conditions",
        "cancellation-policy": "Cancellation Policy",
        "sitemap": "Sitemap",
        "service": "Service",
        "makler-dashboard": "Agent Portal",
        "glossar": "Glossary",
        "glossary": "Glossary",
        "disclaimer": "Disclaimer",
        "buyer-guide": "Buyer Guide",
        "real-estate-agents": "Real Estate Agents",
        "construction-companies": "Construction Companies",
        "lawyers": "Lawyers",
        "tax-advisors": "Tax Advisors",
        "architects": "Architects",
        "become-partner": "Become Partner",
        "registration": "Registration",
        "expert-finder": "Expert Finder",
        "market-reports": "Market Reports",
        "important-addresses": "Important Addresses",
        "news": "News",
        "croatia": "Croatia",
    },
    "hr": {
        "home": "Početna",
        "listing": "Nekretnine",
        "listings": "Nekretnine",
        "about": "O nama",
        "contact": "Kontakt",
        "faq": "Česta pitanja",
        "blog": "Blog",
        "imprint": "Impressum",
        "data-protection": "Zaštita podataka",
        "agb": "Uvjeti korištenja",
        "cancellation-policy": "Pravo na odustanak",
        "sitemap": "Mapa stranica",
        "service": "Usluge",
        "makler-dashboard": "Portal za agente",
        "glossar": "Pojmovnik",
        "pojmovnik": "Pojmovnik",
        "disclaimer": "Odricanje odgovornosti",
        "buyer-guide": "Vodič za kupce",
        "agencije-za-nekretnine": "Agencije za nekretnine",
        "gradevinske-tvrtke": "Građevinske tvrtke",
        "odvjetnici": "Odvjetnici",
        "porezni-savjetnici": "Porezni savjetnici",
        "arhitekti": "Arhitekti",
        "postanite-partner": "Postanite partner",
        "registracija": "Registracija",
        "pronalazac-strucnjaka": "Tražilica stručnjaka",
        "trzisni-izvjestaji": "Tržišni izvještaji",
        "vazne-adrese": "Važne adrese",
        "vijesti": "Vijesti",
        "hrvatska": "Hrvatska",
    },
    "fr": {
        "home": "Accueil",
        "listing": "Propriétés",
        "listings": "Propriétés",
        "about": "À propos",
        "contact": "Contact",
        "faq": "FAQ",
        "blog": "Blog",
        "imprint": "Mentions légales",
        "data-protection": "Politique de confidentialité",
        "agb": "Conditions générales",
        "cancellation-policy": "Droit de rétractation",
        "sitemap": "Plan du site",
        "service": "Services",
        "makler-dashboard": "Portail agents",
        "glossar": "Glossaire",
        "glossaire": "Glossaire",
        "disclaimer": "Avertissement",
        "buyer-guide": "Guide de l'acheteur",
        "agents-immobiliers": "Agents immobiliers",
        "entreprises-construction": "Entreprises de construction",
        "avocats": "Avocats",
        "conseillers-fiscaux": "Conseillers fiscaux",
        "architectes": "Architectes",
        "devenir-partenaire": "Devenir partenaire",
        "inscription": "Inscription",
        "recherche-experts": "Recherche d'experts",
        "rapports-marche": "Rapports de marché",
        "adresses-importantes": "Adresses importantes",
        "actualites": "Actualités",
        "croatie": "Croatie",
    },
    "nl": {
        "home": "Home",
        "listing": "Vastgoed",
        "listings": "Vastgoed",
        "about": "Over ons",
        "contact": "Contact",
        "faq": "FAQ",
        "sitemap": "Sitemap",
        "makler-dashboard": "Makelaarsportaal",
        "woordenlijst": "Woordenlijst",
        "disclaimer": "Disclaimer",
        "buyer-guide": "Koopgids",
        "makelaars": "Makelaars",
        "bouwbedrijven": "Bouwbedrijven",
        "advocaten": "Advocaten",
        "belastingadviseurs": "Belastingadviseurs",
        "architecten": "Architecten",
        "partner-worden": "Partner worden",
        "registratie": "Registratie",
        "expert-zoeker": "Expertzoeker",
        "marktverslagen": "Marktverslagen",
        "belangrijke-adressen": "Belangrijke adressen",
        "nieuws": "Nieuws",
        "kroatie": "Kroatië",
    },
    "pl": {
        "home": "Strona główna",
        "listing": "Nieruchomości",
        "sitemap": "Mapa strony",
        "slownik": "Słownik",
        "agenci-nieruchomosci": "Agenci nieruchomości",
        "firmy-budowlane": "Firmy budowlane",
        "prawnicy": "Prawnicy",
        "doradcy-podatkowi": "Doradcy podatkowi",
        "architekci": "Architekci",
        "zostan-partnerem": "Zostań partnerem",
        "rejestracja": "Rejestracja",
        "chorwacja": "Chorwacja",
    },
    "cz": {
        "home": "Domů",
        "listing": "Nemovitosti",
        "sitemap": "Mapa stránek",
        "glosar": "Glosář",
        "realitni-makleri": "Realitní makléři",
        "stavebni-firmy": "Stavební firmy",
        "pravnici": "Právníci",
        "danovi-poradci": "Daňoví poradci",
        "architekti": "Architekti",
        "stanat-se-partnerem": "Staňte se partnerem",
        "registrace": "Registrace",
        "chorvatsko": "Chorvatsko",
    },
    "sk": {
        "home": "Domov",
        "listing": "Nehnuteľnosti",
        "sitemap": "Mapa stránok",
        "slovnik": "Slovník",
        "realitni-makleri": "Realitní makléri",
        "stavebne-firmy": "Stavebné firmy",
        "pravnici": "Právnici",
        "danovi-poradcovia": "Daňoví poradcovia",
        "architekti": "Architekti",
        "stat-sa-partnerom": "Staňte sa partnerom",
        "registracia": "Registrácia",
        "chorvatsko": "Chorvátsko",
    },
    "ru": {
        "home": "Главная",
        "listing": "Недвижимость",
        "sitemap": "Карта сайта",
        "glossarij": "Глоссарий",
        "agenty-nedvizhimosti": "Агенты недвижимости",
        "stroitelnye-kompanii": "Строительные компании",
        "advokaty": "Адвокаты",
        "nalogovye-konsultanty": "Налоговые консультанты",
        "arhitektory": "Архитекторы",
        "stat-partnerom": "Стать партнером",
        "registratsiya": "Регистрация",
        "horvatiya": "Хорватия",
    },
    "gr": {
        "home": "Αρχική",
        "listing": "Ακίνητα",
        "sitemap": "Χάρτης ιστοτόπου",
        "glossari": "Γλωσσάριο",
        "mesites-akiniton": "Μεσίτες ακινήτων",
        "kataskevestikes-etaireies": "Κατασκευαστικές εταιρείες",
        "dikigoroi": "Δικηγόροι",
        "forologikoi-symvouloi": "Φορολογικοί σύμβουλοι",
        "architektons": "Αρχιτέκτονες",
        "gineite-synergatis": "Γίνετε συνεργάτης",
        "eggraphi": "Εγγραφή",
        "kroatia": "Κροατία",
    },
    "sw": {
        "home": "Hem",
        "listing": "Fastigheter",
        "sitemap": "Webbplatskarta",
        "ordlista": "Ordlista",
        "fastighetsmaklare": "Fastighetsmäklare",
        "byggforetag": "Byggföretag",
        "advokater": "Advokater",
        "skatteradgivare": "Skatterådgivare",
        "arkitekter": "Arkitekter",
        "bli-partner": "Bli partner",
        "registrering": "Registrering",
        "kroatien": "Kroatien",
    },
    "no": {
        "home": "Hjem",
        "listing": "Eiendommer",
        "sitemap": "Nettstedkart",
        "ordliste": "Ordliste",
        "eiendomsmeglere": "Eiendomsmeglere",
        "byggefirmaer": "Byggefirmaer",
        "advokater": "Advokater",
        "skatteradgivere": "Skatterådgivere",
        "arkitekter": "Arkitekter",
        "bli-partner": "Bli partner",
        "registrering": "Registrering",
        "kroatia": "Kroatia",
    },
}


def breadcrumbs(request):
    """
    Generiert Breadcrumbs basierend auf dem aktuellen URL-Pfad.
    Liefert sowohl die Breadcrumb-Liste als auch JSON-LD Schema für SEO.
    """
    user_language = request.session.get('site_language', 'ge')
    labels = BREADCRUMB_LABELS.get(user_language, BREADCRUMB_LABELS['ge'])
    
    path = request.path.strip('/')
    parts = path.split('/') if path else []
    
    # Breadcrumb-Liste aufbauen
    breadcrumb_items = []
    current_url = ''
    
    # Startseite immer als erstes
    breadcrumb_items.append({
        'name': labels.get('home', 'Home'),
        'url': f'/{user_language}/' if user_language != 'ge' else '/',
        'position': 1,
    })
    
    position = 2
    for i, part in enumerate(parts):
        if not part:
            continue
            
        # Sprachcode überspringen (ge, en, hr, etc.)
        if part in ALL_LANGUAGES:
            continue
        
        current_url += f'/{part}'
        
        # Label finden (aus Dict oder kapitalisieren)
        label = labels.get(part, part.replace('-', ' ').title())
        
        breadcrumb_items.append({
            'name': label,
            'url': current_url + '/',
            'position': position,
        })
        position += 1
    
    # JSON-LD Schema für Breadcrumbs generieren
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": item['position'],
                "name": item['name'],
                "item": f"https://123-kroatien.eu{item['url']}"
            }
            for item in breadcrumb_items
        ]
    }
    
    return {
        'breadcrumbs': breadcrumb_items,
        'breadcrumb_schema_json': json.dumps(breadcrumb_schema, ensure_ascii=False),
    }


# ============================================
# HREFLANG TAGS (Internationalisierung)
# ============================================

# ISO-639-1 Sprachcodes für hreflang
HREFLANG_CODES = {
    'ge': 'de',      # Deutsch
    'en': 'en',      # English
    'hr': 'hr',      # Hrvatski
    'fr': 'fr',      # Français
    'nl': 'nl',      # Nederlands
    'pl': 'pl',      # Polski
    'cz': 'cs',      # Čeština
    'sk': 'sk',      # Slovenčina
    'ru': 'ru',      # Русский
    'gr': 'el',      # Ελληνικά
    'sw': 'sv',      # Svenska
    'no': 'no',      # Norsk
}


def hreflang_tags(request):
    """
    Generiert hreflang-Tags für alle 12 Sprachen.
    Wichtig für internationale SEO - zeigt Google welche Sprachversionen existieren.
    """
    path = request.path
    
    # Aktuelle Sprache aus Pfad ermitteln
    path_parts = path.strip('/').split('/')
    current_lang = path_parts[0] if path_parts and path_parts[0] in ALL_LANGUAGES else 'ge'
    
    # Pfad ohne Sprachpräfix
    if current_lang in ALL_LANGUAGES and path_parts and path_parts[0] == current_lang:
        path_without_lang = '/' + '/'.join(path_parts[1:])
    else:
        path_without_lang = path
    
    # Sicherstellen dass der Pfad mit / endet
    if path_without_lang and not path_without_lang.endswith('/'):
        path_without_lang += '/'
    if path_without_lang == '':
        path_without_lang = '/'
    
    # Hreflang-Links generieren
    hreflang_links = []
    
    for site_lang, iso_code in HREFLANG_CODES.items():
        if site_lang == 'ge':
            # Deutsch ist default, kein Präfix
            url = f"https://123-kroatien.eu{path_without_lang}"
        else:
            url = f"https://123-kroatien.eu/{site_lang}{path_without_lang}"
        
        hreflang_links.append({
            'lang': iso_code,
            'url': url,
        })
    
    # x-default (für Nutzer ohne passende Sprache)
    hreflang_links.append({
        'lang': 'x-default',
        'url': f"https://123-kroatien.eu{path_without_lang}",
    })
    
    return {
        'hreflang_links': hreflang_links,
    }