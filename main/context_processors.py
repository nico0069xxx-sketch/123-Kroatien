from django.utils.translation import activate
from pages.models import Translation

# Cookie Banner Übersetzungen (alle 12 Sprachen)
COOKIE_TRANSLATIONS = {"ge": {"cookie_title": "Cookie-Einstellungen", "cookie_text": "Wir verwenden Cookies, um Ihnen die bestmögliche Erfahrung zu bieten.", "cookie_necessary": "Notwendige Cookies", "cookie_necessary_desc": "Für die Grundfunktionen erforderlich.", "cookie_analytics": "Analyse-Cookies", "cookie_analytics_desc": "Helfen uns zu verstehen, wie Besucher unsere Website nutzen.", "cookie_marketing": "Marketing-Cookies", "cookie_marketing_desc": "Werden für relevante Werbung verwendet.", "cookie_settings": "Einstellungen", "cookie_reject": "Ablehnen", "cookie_accept": "Alle akzeptieren", "cookie_save": "Speichern", "cookie_privacy": "Datenschutz"}, "en": {"cookie_title": "Cookie Settings", "cookie_text": "We use cookies to provide you with the best experience.", "cookie_necessary": "Necessary Cookies", "cookie_necessary_desc": "Required for basic functionality.", "cookie_analytics": "Analytics Cookies", "cookie_analytics_desc": "Help us understand how visitors use our website.", "cookie_marketing": "Marketing Cookies", "cookie_marketing_desc": "Used for relevant advertising.", "cookie_settings": "Settings", "cookie_reject": "Reject", "cookie_accept": "Accept All", "cookie_save": "Save", "cookie_privacy": "Privacy"}, "hr": {"cookie_title": "Postavke kolacica", "cookie_text": "Koristimo kolacice za najbolje iskustvo.", "cookie_necessary": "Neophodni kolacici", "cookie_necessary_desc": "Potrebni za osnovne funkcije.", "cookie_analytics": "Analiticni kolacici", "cookie_analytics_desc": "Pomazu razumjeti koristenje.", "cookie_marketing": "Marketinski kolacici", "cookie_marketing_desc": "Za relevantne oglase.", "cookie_settings": "Postavke", "cookie_reject": "Odbij", "cookie_accept": "Prihvati sve", "cookie_save": "Spremi", "cookie_privacy": "Privatnost"}, "fr": {"cookie_title": "Parametres cookies", "cookie_text": "Nous utilisons des cookies.", "cookie_necessary": "Cookies necessaires", "cookie_necessary_desc": "Requis.", "cookie_analytics": "Cookies analytiques", "cookie_analytics_desc": "Comprendre utilisation.", "cookie_marketing": "Cookies marketing", "cookie_marketing_desc": "Publicites.", "cookie_settings": "Parametres", "cookie_reject": "Refuser", "cookie_accept": "Accepter", "cookie_save": "Enregistrer", "cookie_privacy": "Confidentialite"}, "nl": {"cookie_title": "Cookie-instellingen", "cookie_text": "Wij gebruiken cookies.", "cookie_necessary": "Noodzakelijk", "cookie_necessary_desc": "Vereist.", "cookie_analytics": "Analytisch", "cookie_analytics_desc": "Begrip gebruik.", "cookie_marketing": "Marketing", "cookie_marketing_desc": "Advertenties.", "cookie_settings": "Instellingen", "cookie_reject": "Weigeren", "cookie_accept": "Accepteren", "cookie_save": "Opslaan", "cookie_privacy": "Privacy"}, "pl": {"cookie_title": "Ustawienia cookies", "cookie_text": "Uzywamy cookies.", "cookie_necessary": "Niezbedne", "cookie_necessary_desc": "Wymagane.", "cookie_analytics": "Analityczne", "cookie_analytics_desc": "Zrozumienie.", "cookie_marketing": "Marketingowe", "cookie_marketing_desc": "Reklamy.", "cookie_settings": "Ustawienia", "cookie_reject": "Odrzuc", "cookie_accept": "Akceptuj", "cookie_save": "Zapisz", "cookie_privacy": "Prywatnosc"}, "cz": {"cookie_title": "Nastaveni cookies", "cookie_text": "Pouzivame cookies.", "cookie_necessary": "Nezbytne", "cookie_necessary_desc": "Nutne.", "cookie_analytics": "Analyticke", "cookie_analytics_desc": "Pochopeni.", "cookie_marketing": "Marketingove", "cookie_marketing_desc": "Reklamy.", "cookie_settings": "Nastaveni", "cookie_reject": "Odmitnout", "cookie_accept": "Prijmout", "cookie_save": "Ulozit", "cookie_privacy": "Soukromi"}, "sk": {"cookie_title": "Nastavenia cookies", "cookie_text": "Pouzivame cookies.", "cookie_necessary": "Nevyhnutne", "cookie_necessary_desc": "Potrebne.", "cookie_analytics": "Analyticke", "cookie_analytics_desc": "Pochopenie.", "cookie_marketing": "Marketingove", "cookie_marketing_desc": "Reklamy.", "cookie_settings": "Nastavenia", "cookie_reject": "Odmietnut", "cookie_accept": "Prijat", "cookie_save": "Ulozit", "cookie_privacy": "Sukromie"}, "ru": {"cookie_title": "Nastroiki cookie", "cookie_text": "My ispolzuem cookie.", "cookie_necessary": "Neobhodimye", "cookie_necessary_desc": "Trebuetsja.", "cookie_analytics": "Analiticheskie", "cookie_analytics_desc": "Ponimanie.", "cookie_marketing": "Marketingovye", "cookie_marketing_desc": "Reklama.", "cookie_settings": "Nastroiki", "cookie_reject": "Otklonjit", "cookie_accept": "Prinjat", "cookie_save": "Sohranit", "cookie_privacy": "Konfidencialnost"}, "gr": {"cookie_title": "Rythmiseis cookies", "cookie_text": "Chrisimopoioume cookies.", "cookie_necessary": "Aparaitita", "cookie_necessary_desc": "Apaitountai.", "cookie_analytics": "Analytika", "cookie_analytics_desc": "Katanoisi.", "cookie_marketing": "Marketing", "cookie_marketing_desc": "Diafimisi.", "cookie_settings": "Rythmiseis", "cookie_reject": "Aporripsi", "cookie_accept": "Apodoxi", "cookie_save": "Apothikeusi", "cookie_privacy": "Aporrito"}, "sw": {"cookie_title": "Cookie-installningar", "cookie_text": "Vi anvander cookies.", "cookie_necessary": "Nodvandiga", "cookie_necessary_desc": "Kravs.", "cookie_analytics": "Analytiska", "cookie_analytics_desc": "Forstaelse.", "cookie_marketing": "Marknadsforing", "cookie_marketing_desc": "Annonser.", "cookie_settings": "Installningar", "cookie_reject": "Avvisa", "cookie_accept": "Acceptera", "cookie_save": "Spara", "cookie_privacy": "Integritet"}, "no": {"cookie_title": "Cookie-innstillinger", "cookie_text": "Vi bruker cookies.", "cookie_necessary": "Nodvendige", "cookie_necessary_desc": "Pakreves.", "cookie_analytics": "Analytiske", "cookie_analytics_desc": "Forstaelse.", "cookie_marketing": "Markedsforing", "cookie_marketing_desc": "Annonser.", "cookie_settings": "Innstillinger", "cookie_reject": "Avvis", "cookie_accept": "Godta", "cookie_save": "Lagre", "cookie_privacy": "Personvern"}}



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

    # Sprache aus URL oder Session
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in ["ge", "en", "hr", "fr", "nl", "pl", "cz", "sk", "ru", "gr", "sw", "no"] else None
    user_language = url_lang or request.session.get("site_language", "ge")

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
    
    # URL für Experten-Finder (12 Sprachen)
    EXPERTEN_FINDER_URLS = {
        'ge': 'experten-finder', 'en': 'expert-finder', 'hr': 'pronalazac-strucnjaka',
        'fr': 'recherche-experts', 'nl': 'expert-zoeken', 'pl': 'wyszukiwarka-ekspertow',
        'cz': 'vyhledavac-expertu', 'sk': 'vyhladavac-expertov', 'ru': 'poisk-ekspertov',
        'gr': 'anazhthsh-eidikwn', 'sw': 'expertsokare', 'no': 'ekspertsoker'
    }
    context['url_experten_finder'] = EXPERTEN_FINDER_URLS.get(user_language, 'experten-finder')
    
    # Label für Experten-Finder (12 Sprachen)
    EXPERTEN_FINDER_LABELS = {
        'ge': 'Experten-Finder', 'en': 'Expert Finder', 'hr': 'Pronalazac strucnjaka',
        'fr': 'Recherche experts', 'nl': 'Expert zoeken', 'pl': 'Wyszukiwarka ekspertow',
        'cz': 'Vyhledavac expertu', 'sk': 'Vyhladavac expertov', 'ru': 'Poisk ekspertov',
        'gr': 'Anazhthsh eidikwn', 'sw': 'Expertsokare', 'no': 'Ekspertsoker'
    }
    context['experten_finder_label'] = EXPERTEN_FINDER_LABELS.get(user_language, 'Experten-Finder')
    
    # URL für Marktberichte
    MARKET_URLS = {
        'ge': 'marktberichte', 'en': 'market-reports', 'hr': 'trzisna-izvjesca',
        'fr': 'rapports-immobiliers', 'nl': 'marktrapporten', 'pl': 'raporty-rynkowe',
        'cz': 'trzni-zpravy', 'sk': 'trhove-spravy', 'ru': 'rynochnye-otchety',
        'gr': 'anafores-agoras', 'sw': 'marknadsrapporter', 'no': 'markedsrapporter'
    }
    context['url_market_reports'] = MARKET_URLS.get(user_language, 'marktberichte')
    
    # URL für Wichtige Adressen
    ADDRESS_URLS = {
        'ge': 'wichtige-adressen', 'en': 'important-addresses', 'hr': 'vazne-adrese',
        'fr': 'adresses-importantes', 'nl': 'belangrijke-adressen', 'pl': 'wazne-adresy',
        'cz': 'dulezite-adresy', 'sk': 'dolezite-adresy', 'ru': 'vazhnye-adresa',
        'gr': 'simantikes-diefthinseis', 'sw': 'viktiga-adresser', 'no': 'viktige-adresser'
    }
    context['url_addresses'] = ADDRESS_URLS.get(user_language, 'wichtige-adressen')
    
    # URL für Glossar
    GLOSSARY_URLS = {
        'ge': 'glossar', 'en': 'glossary', 'hr': 'pojmovnik',
        'fr': 'glossaire', 'nl': 'woordenlijst', 'pl': 'slownik',
        'cz': 'glosar', 'sk': 'slovnik', 'ru': 'glossarij',
        'gr': 'glossari', 'sw': 'ordlista', 'no': 'ordliste'
    }
    context['url_glossary'] = GLOSSARY_URLS.get(user_language, 'glossar')
    
    # URL für News
    NEWS_URLS = {
        'ge': 'nachrichten', 'en': 'news', 'hr': 'vijesti',
        'fr': 'actualites', 'nl': 'nieuws', 'pl': 'wiadomosci',
        'cz': 'zpravy', 'sk': 'spravy', 'ru': 'novosti',
        'gr': 'nea', 'sw': 'nyheter', 'no': 'nyheter'
    }
    context['url_news'] = NEWS_URLS.get(user_language, 'nachrichten')

    # Chatbot-Übersetzungen immer laden (für alle Seiten)
    chatbot_translations = Translation.objects.filter(page='chatbot')
    for t in chatbot_translations:
        if user_language == 'en': context[t.name] = t.english_content
        elif user_language == 'hr': context[t.name] = t.croatian_content
        elif user_language == 'fr': context[t.name] = t.french_content
        elif user_language == 'gr': context[t.name] = t.greek_content
        elif user_language == 'pl': context[t.name] = t.polish_content
        elif user_language == 'cz': context[t.name] = t.czech_content
        elif user_language == 'ru': context[t.name] = t.russian_content
        elif user_language == 'sw': context[t.name] = t.swedish_content
        elif user_language == 'no': context[t.name] = t.norway_content
        elif user_language == 'sk': context[t.name] = t.slovak_content
        elif user_language == 'nl': context[t.name] = t.dutch_content
        else: context[t.name] = t.german_content


    # News URLs
    news_urls = {
        'ge': '/ge/kroatien/nachrichten/',
        'en': '/en/croatia/news/',
        'hr': '/hr/hrvatska/vijesti/',
        'fr': '/fr/croatie/actualites/',
        'nl': '/nl/kroatie/nieuws/',
        'pl': '/pl/chorwacja/wiadomosci/',
        'cz': '/cz/chorvatsko/zpravy/',
        'sk': '/sk/chorvatsko/spravy/',
        'ru': '/ru/horvatiya/novosti/',
        'gr': '/gr/kroatia/nea/',
        'sw': '/sw/kroatien/nyheter/',
        'no': '/no/kroatia/nyheter/',
    }
    context['news_url'] = news_urls.get(user_language, '/ge/kroatien/nachrichten/')
    
    # News Label
    news_labels = {
        'ge': 'Nachrichten',
        'en': 'News',
        'hr': 'Vijesti',
        'fr': 'Actualités',
        'nl': 'Nieuws',
        'pl': 'Wiadomości',
        'cz': 'Zprávy',
        'sk': 'Správy',
        'ru': 'Новости',
        'gr': 'Νέα',
        'sw': 'Nyheter',
        'no': 'Nyheter',
    }
    context['news_label'] = news_labels.get(user_language, 'Nachrichten')

    # Partner Section Labels
    partner_labels = {
        'ge': 'Unsere Partner',
        'en': 'Our Partners',
        'hr': 'Naši partneri',
        'fr': 'Nos partenaires',
        'nl': 'Onze partners',
        'pl': 'Nasi partnerzy',
        'cz': 'Naši partneři',
        'sk': 'Naši partneri',
        'ru': 'Наши партнеры',
        'gr': 'Οι συνεργάτες μας',
        'sw': 'Våra partners',
        'no': 'Våre partnere',
    }
    context['our_partners'] = partner_labels.get(user_language, 'Unsere Partner')
    
    # Partner Subtitle Labels
    partner_subtitle = {
        'ge': 'Verifizierte Partner aus Kroatien',
        'en': 'Verified partners from Croatia',
        'hr': 'Verificirani partneri iz Hrvatske',
        'fr': 'Partenaires vérifiés de Croatie',
        'nl': 'Geverifieerde partners uit Kroatië',
        'pl': 'Zweryfikowani partnerzy z Chorwacji',
        'cz': 'Ověření partneři z Chorvatska',
        'sk': 'Overení partneri z Chorvátska',
        'ru': 'Проверенные партнеры из Хорватии',
        'gr': 'Επαληθευμένοι συνεργάτες από την Κροατία',
        'sw': 'Verifierade partners från Kroatien',
        'no': 'Verifiserte partnere fra Kroatia',
    }
    context['partner_subtitle'] = partner_subtitle.get(user_language, 'Verifizierte Partner aus Kroatien')

    # Hero Section - Tagline
    hero_tagline = {
        'ge': 'KROATIEN - ADRIA - MITTELMEER',
        'en': 'CROATIA - ADRIATIC - MEDITERRANEAN',
        'hr': 'HRVATSKA - JADRAN - MEDITERAN',
        'fr': 'CROATIE - ADRIATIQUE - MÉDITERRANÉE',
        'nl': 'KROATIË - ADRIATISCHE ZEE - MIDDELLANDSE ZEE',
        'pl': 'CHORWACJA - ADRIATYK - MORZE ŚRÓDZIEMNE',
        'cz': 'CHORVATSKO - JADRAN - STŘEDOMOŘÍ',
        'sk': 'CHORVÁTSKO - JADRAN - STREDOMORIE',
        'ru': 'ХОРВАТИЯ - АДРИАТИКА - СРЕДИЗЕМНОМОРЬЕ',
        'gr': 'ΚΡΟΑΤΊΑ - ΑΔΡΙΑΤΙΚΉ - ΜΕΣΌΓΕΙΟΣ',
        'sw': 'KROATIEN - ADRIATISKA HAVET - MEDELHAVET',
        'no': 'KROATIA - ADRIATERHAVET - MIDDELHAVET',
    }
    context['hero_tagline'] = hero_tagline.get(user_language, 'KROATIEN - ADRIA - MITTELMEER')

    # Hero Section - Title
    hero_title = {
        'ge': 'Exklusive Immobilien<br>an der kroatischen Küste',
        'en': 'Exclusive Properties<br>on the Croatian Coast',
        'hr': 'Ekskluzivne nekretnine<br>na hrvatskoj obali',
        'fr': 'Propriétés exclusives<br>sur la côte croate',
        'nl': 'Exclusief vastgoed<br>aan de Kroatische kust',
        'pl': 'Ekskluzywne nieruchomości<br>na chorwackim wybrzeżu',
        'cz': 'Exkluzivní nemovitosti<br>na chorvatském pobřeží',
        'sk': 'Exkluzívne nehnuteľnosti<br>na chorvátskom pobreží',
        'ru': 'Эксклюзивная недвижимость<br>на хорватском побережье',
        'gr': 'Αποκλειστικά ακίνητα<br>στην κροατική ακτή',
        'sw': 'Exklusiva fastigheter<br>vid den kroatiska kusten',
        'no': 'Eksklusive eiendommer<br>ved den kroatiske kysten',
    }
    context['hero_title'] = hero_title.get(user_language, 'Exklusive Immobilien<br>an der kroatischen Küste')

    # Hero Section - Subtitle
    hero_subtitle = {
        'ge': 'Verifizierte Immobilienmakler und persönliche Beratung für Ihre Traumimmobilie.',
        'en': 'Verified real estate agents and personal advice for your dream property.',
        'hr': 'Verificirani agenti za nekretnine i osobno savjetovanje za vašu nekretninu iz snova.',
        'fr': 'Agents immobiliers vérifiés et conseils personnalisés pour votre propriété de rêve.',
        'nl': 'Geverifieerde makelaars en persoonlijk advies voor uw droomwoning.',
        'pl': 'Zweryfikowani agenci nieruchomości i osobiste doradztwo dla wymarzonej nieruchomości.',
        'cz': 'Ověření realitní makléři a osobní poradenství pro vaši vysněnou nemovitost.',
        'sk': 'Overení realitní makléri a osobné poradenstvo pre vašu vysnívanú nehnuteľnosť.',
        'ru': 'Проверенные агенты по недвижимости и персональные консультации для вашей мечты.',
        'gr': 'Επαληθευμένοι μεσίτες και προσωπικές συμβουλές για το ακίνητο των ονείρων σας.',
        'sw': 'Verifierade fastighetsmäklare och personlig rådgivning för din drömbostad.',
        'no': 'Verifiserte eiendomsmeglere og personlig rådgivning for drømmeeiendommen din.',
    }
    context['hero_subtitle'] = hero_subtitle.get(user_language, 'Verifizierte Immobilienmakler und persönliche Beratung für Ihre Traumimmobilie.')

    # Cookie Banner
    cookie_trans = COOKIE_TRANSLATIONS.get(user_language, COOKIE_TRANSLATIONS["ge"])
    context.update(cookie_trans)
    return context

# Sitemap Übersetzungen (alle 12 Sprachen)
SITEMAP_TRANSLATIONS = {
    "ge": {
        "sitemap_meta_desc": "Vollständige Sitemap von 123-Kroatien.eu - Ihr Wegweiser zu kroatischen Immobilien",
        "sitemap_title": "Sitemap",
        "sitemap_desc": "Vollständige Website-Struktur von 123-Kroatien.eu",
        "sitemap_portal_desc": "Führendes Immobilienportal in Kroatien",
        "sitemap_categories": "Seitenkategorien",
        "sitemap_heading": "Sitemap",
        "sitemap_subheading": "Kompletter Überblick aller Seiten und Funktionen unseres Immobilienportals",
        "main_pages": "Hauptseiten",
        "home": "Startseite",
        "all_properties": "Alle Immobilien",
        "about_us": "Über uns",
        "contact": "Kontakt",
        "faq": "FAQ",
        "legal_info": "Rechtliche Informationen",
        "imprint": "Impressum",
        "privacy": "Datenschutz",
        "terms": "AGB",
        "cancellation": "Widerrufsrecht",
        "disclaimer": "Haftungsausschluss",
        "service_providers": "Dienstleister Kroatien",
        "real_estate_agent": "Immobilienmakler",
        "contractor": "Bauunternehmer",
        "lawyer": "Rechtsanwalt",
        "tax_advisor": "Steuerberater",
        "architect": "Architekt",
        "user_area": "Benutzer-Bereich",
        "become_partner": "Partner werden",
        "register": "Registrieren",
        "login": "Anmelden",
        "agent_portal": "Makler-Portal",
        "forgot_password": "Passwort vergessen",
        "content_info": "Inhalte & Informationen",
        "news": "Nachrichten",
        "market_reports": "Marktberichte",
        "important_addresses": "Wichtige Adressen",
        "glossary": "Glossar",
        "tools": "Tools & Services",
        "expert_finder": "Experten-Finder",
        "ai_search": "KI Immobilien Schnellsuche",
        "property_search": "Immobiliensuche",
    },
    "en": {
        "sitemap_meta_desc": "Complete sitemap of 123-Kroatien.eu - Your guide to Croatian real estate",
        "sitemap_title": "Sitemap",
        "sitemap_desc": "Complete website structure of 123-Kroatien.eu",
        "sitemap_portal_desc": "Leading real estate portal in Croatia",
        "sitemap_categories": "Page Categories",
        "sitemap_heading": "Sitemap",
        "sitemap_subheading": "Complete overview of all pages and features of our real estate portal",
        "main_pages": "Main Pages",
        "home": "Home",
        "all_properties": "All Properties",
        "about_us": "About Us",
        "contact": "Contact",
        "faq": "FAQ",
        "legal_info": "Legal Information",
        "imprint": "Imprint",
        "privacy": "Privacy Policy",
        "terms": "Terms & Conditions",
        "cancellation": "Cancellation Policy",
        "disclaimer": "Disclaimer",
        "service_providers": "Service Providers Croatia",
        "real_estate_agent": "Real Estate Agent",
        "contractor": "Building Contractor",
        "lawyer": "Lawyer",
        "tax_advisor": "Tax Advisor",
        "architect": "Architect",
        "user_area": "User Area",
        "become_partner": "Become a Partner",
        "register": "Register",
        "login": "Login",
        "agent_portal": "Agent Portal",
        "forgot_password": "Forgot Password",
        "content_info": "Content & Information",
        "news": "News",
        "market_reports": "Market Reports",
        "important_addresses": "Important Addresses",
        "glossary": "Glossary",
        "tools": "Tools & Services",
        "expert_finder": "Expert Finder",
        "ai_search": "AI Property Quick Search",
        "property_search": "Property Search",
    },
    "hr": {
        "sitemap_meta_desc": "Kompletna mapa stranica 123-Kroatien.eu - Vaš vodič kroz hrvatske nekretnine",
        "sitemap_title": "Mapa stranica",
        "sitemap_desc": "Kompletna struktura web stranice 123-Kroatien.eu",
        "sitemap_portal_desc": "Vodeći portal za nekretnine u Hrvatskoj",
        "sitemap_categories": "Kategorije stranica",
        "sitemap_heading": "Mapa stranica",
        "sitemap_subheading": "Kompletan pregled svih stranica i funkcija našeg portala za nekretnine",
        "main_pages": "Glavne stranice",
        "home": "Početna",
        "all_properties": "Sve nekretnine",
        "about_us": "O nama",
        "contact": "Kontakt",
        "faq": "Česta pitanja",
        "legal_info": "Pravne informacije",
        "imprint": "Impressum",
        "privacy": "Zaštita podataka",
        "terms": "Uvjeti korištenja",
        "cancellation": "Pravo na odustanak",
        "disclaimer": "Odricanje odgovornosti",
        "service_providers": "Pružatelji usluga",
        "real_estate_agent": "Agent za nekretnine",
        "contractor": "Građevinar",
        "lawyer": "Odvjetnik",
        "tax_advisor": "Porezni savjetnik",
        "architect": "Arhitekt",
        "user_area": "Korisnički prostor",
        "become_partner": "Postanite partner",
        "register": "Registracija",
        "login": "Prijava",
        "agent_portal": "Portal za agente",
        "forgot_password": "Zaboravljena lozinka",
        "content_info": "Sadržaj i informacije",
        "news": "Vijesti",
        "market_reports": "Tržišna izvješća",
        "important_addresses": "Važne adrese",
        "glossary": "Pojmovnik",
        "tools": "Alati i usluge",
        "expert_finder": "Pronalazač stručnjaka",
        "ai_search": "AI brza pretraga nekretnina",
        "property_search": "Pretraživanje nekretnina",
    },
    "fr": {
        "sitemap_meta_desc": "Plan du site complet de 123-Kroatien.eu - Votre guide de l'immobilier croate",
        "sitemap_title": "Plan du site",
        "sitemap_desc": "Structure complète du site 123-Kroatien.eu",
        "sitemap_portal_desc": "Portail immobilier leader en Croatie",
        "sitemap_categories": "Catégories de pages",
        "sitemap_heading": "Plan du site",
        "sitemap_subheading": "Aperçu complet de toutes les pages et fonctionnalités de notre portail immobilier",
        "main_pages": "Pages principales",
        "home": "Accueil",
        "all_properties": "Toutes les propriétés",
        "about_us": "À propos",
        "contact": "Contact",
        "faq": "FAQ",
        "legal_info": "Informations légales",
        "imprint": "Mentions légales",
        "privacy": "Politique de confidentialité",
        "terms": "Conditions générales",
        "cancellation": "Droit de rétractation",
        "disclaimer": "Avertissement",
        "service_providers": "Prestataires de services",
        "real_estate_agent": "Agent immobilier",
        "contractor": "Entrepreneur",
        "lawyer": "Avocat",
        "tax_advisor": "Conseiller fiscal",
        "architect": "Architecte",
        "user_area": "Espace utilisateur",
        "become_partner": "Devenir partenaire",
        "register": "S'inscrire",
        "login": "Connexion",
        "agent_portal": "Portail agents",
        "forgot_password": "Mot de passe oublié",
        "content_info": "Contenu et informations",
        "news": "Actualités",
        "market_reports": "Rapports de marché",
        "important_addresses": "Adresses importantes",
        "glossary": "Glossaire",
        "tools": "Outils et services",
        "expert_finder": "Recherche d'experts",
        "ai_search": "Recherche rapide IA",
        "property_search": "Recherche immobilière",
    },
    "nl": {
        "sitemap_meta_desc": "Volledige sitemap van 123-Kroatien.eu - Uw gids voor Kroatisch vastgoed",
        "sitemap_title": "Sitemap",
        "sitemap_desc": "Volledige websitestructuur van 123-Kroatien.eu",
        "sitemap_portal_desc": "Toonaangevend vastgoedportaal in Kroatië",
        "sitemap_categories": "Paginacategorieën",
        "sitemap_heading": "Sitemap",
        "sitemap_subheading": "Volledig overzicht van alle pagina's en functies van ons vastgoedportaal",
        "main_pages": "Hoofdpagina's",
        "home": "Home",
        "all_properties": "Alle vastgoed",
        "about_us": "Over ons",
        "contact": "Contact",
        "faq": "FAQ",
        "legal_info": "Juridische informatie",
        "imprint": "Colofon",
        "privacy": "Privacybeleid",
        "terms": "Algemene voorwaarden",
        "cancellation": "Herroepingsrecht",
        "disclaimer": "Disclaimer",
        "service_providers": "Dienstverleners",
        "real_estate_agent": "Makelaar",
        "contractor": "Aannemer",
        "lawyer": "Advocaat",
        "tax_advisor": "Belastingadviseur",
        "architect": "Architect",
        "user_area": "Gebruikersgebied",
        "become_partner": "Partner worden",
        "register": "Registreren",
        "login": "Inloggen",
        "agent_portal": "Makelaarsportaal",
        "forgot_password": "Wachtwoord vergeten",
        "content_info": "Inhoud en informatie",
        "news": "Nieuws",
        "market_reports": "Marktrapporten",
        "important_addresses": "Belangrijke adressen",
        "glossary": "Woordenlijst",
        "tools": "Tools en diensten",
        "expert_finder": "Expert zoeken",
        "ai_search": "AI snel zoeken",
        "property_search": "Vastgoed zoeken",
    },
    "pl": {
        "sitemap_meta_desc": "Kompletna mapa strony 123-Kroatien.eu - Twój przewodnik po chorwackich nieruchomościach",
        "sitemap_title": "Mapa strony",
        "sitemap_desc": "Kompletna struktura strony 123-Kroatien.eu",
        "sitemap_portal_desc": "Wiodący portal nieruchomości w Chorwacji",
        "sitemap_categories": "Kategorie stron",
        "sitemap_heading": "Mapa strony",
        "sitemap_subheading": "Pełny przegląd wszystkich stron i funkcji naszego portalu nieruchomości",
        "main_pages": "Strony główne",
        "home": "Strona główna",
        "all_properties": "Wszystkie nieruchomości",
        "about_us": "O nas",
        "contact": "Kontakt",
        "faq": "FAQ",
        "legal_info": "Informacje prawne",
        "imprint": "Impressum",
        "privacy": "Polityka prywatności",
        "terms": "Regulamin",
        "cancellation": "Prawo odstąpienia",
        "disclaimer": "Zastrzeżenia",
        "service_providers": "Usługodawcy",
        "real_estate_agent": "Agent nieruchomości",
        "contractor": "Wykonawca",
        "lawyer": "Prawnik",
        "tax_advisor": "Doradca podatkowy",
        "architect": "Architekt",
        "user_area": "Strefa użytkownika",
        "become_partner": "Zostań partnerem",
        "register": "Rejestracja",
        "login": "Logowanie",
        "agent_portal": "Portal agenta",
        "forgot_password": "Zapomniałeś hasła",
        "content_info": "Treści i informacje",
        "news": "Wiadomości",
        "market_reports": "Raporty rynkowe",
        "important_addresses": "Ważne adresy",
        "glossary": "Słownik",
        "tools": "Narzędzia i usługi",
        "expert_finder": "Wyszukiwarka ekspertów",
        "ai_search": "Szybkie wyszukiwanie AI",
        "property_search": "Szukaj nieruchomości",
    },
    "cz": {
        "sitemap_meta_desc": "Kompletní mapa stránek 123-Kroatien.eu - Váš průvodce chorvatskými nemovitostmi",
        "sitemap_title": "Mapa stránek",
        "sitemap_desc": "Kompletní struktura webu 123-Kroatien.eu",
        "sitemap_portal_desc": "Přední realitní portál v Chorvatsku",
        "sitemap_categories": "Kategorie stránek",
        "sitemap_heading": "Mapa stránek",
        "sitemap_subheading": "Kompletní přehled všech stránek a funkcí našeho realitního portálu",
        "main_pages": "Hlavní stránky",
        "home": "Domů",
        "all_properties": "Všechny nemovitosti",
        "about_us": "O nás",
        "contact": "Kontakt",
        "faq": "FAQ",
        "legal_info": "Právní informace",
        "imprint": "Impressum",
        "privacy": "Ochrana údajů",
        "terms": "Obchodní podmínky",
        "cancellation": "Právo na odstoupení",
        "disclaimer": "Prohlášení",
        "service_providers": "Poskytovatelé služeb",
        "real_estate_agent": "Realitní makléř",
        "contractor": "Stavitel",
        "lawyer": "Právník",
        "tax_advisor": "Daňový poradce",
        "architect": "Architekt",
        "user_area": "Uživatelská zóna",
        "become_partner": "Staňte se partnerem",
        "register": "Registrace",
        "login": "Přihlášení",
        "agent_portal": "Portál makléře",
        "forgot_password": "Zapomenuté heslo",
        "content_info": "Obsah a informace",
        "news": "Zprávy",
        "market_reports": "Tržní zprávy",
        "important_addresses": "Důležité adresy",
        "glossary": "Glosář",
        "tools": "Nástroje a služby",
        "expert_finder": "Vyhledávač odborníků",
        "ai_search": "AI rychlé vyhledávání",
        "property_search": "Vyhledávání nemovitostí",
    },
    "sk": {
        "sitemap_meta_desc": "Kompletná mapa stránok 123-Kroatien.eu - Váš sprievodca chorvátskymi nehnuteľnosťami",
        "sitemap_title": "Mapa stránok",
        "sitemap_desc": "Kompletná štruktúra webu 123-Kroatien.eu",
        "sitemap_portal_desc": "Popredný realitný portál v Chorvátsku",
        "sitemap_categories": "Kategórie stránok",
        "sitemap_heading": "Mapa stránok",
        "sitemap_subheading": "Kompletný prehľad všetkých stránok a funkcií nášho realitného portálu",
        "main_pages": "Hlavné stránky",
        "home": "Domov",
        "all_properties": "Všetky nehnuteľnosti",
        "about_us": "O nás",
        "contact": "Kontakt",
        "faq": "FAQ",
        "legal_info": "Právne informácie",
        "imprint": "Impressum",
        "privacy": "Ochrana údajov",
        "terms": "Obchodné podmienky",
        "cancellation": "Právo na odstúpenie",
        "disclaimer": "Vyhlásenie",
        "service_providers": "Poskytovatelia služieb",
        "real_estate_agent": "Realitný maklér",
        "contractor": "Staviteľ",
        "lawyer": "Právnik",
        "tax_advisor": "Daňový poradca",
        "architect": "Architekt",
        "user_area": "Používateľská zóna",
        "become_partner": "Staňte sa partnerom",
        "register": "Registrácia",
        "login": "Prihlásenie",
        "agent_portal": "Portál makléra",
        "forgot_password": "Zabudnuté heslo",
        "content_info": "Obsah a informácie",
        "news": "Správy",
        "market_reports": "Trhové správy",
        "important_addresses": "Dôležité adresy",
        "glossary": "Slovník",
        "tools": "Nástroje a služby",
        "expert_finder": "Vyhľadávač odborníkov",
        "ai_search": "AI rýchle vyhľadávanie",
        "property_search": "Vyhľadávanie nehnuteľností",
    },
    "ru": {
        "sitemap_meta_desc": "Полная карта сайта 123-Kroatien.eu - Ваш путеводитель по хорватской недвижимости",
        "sitemap_title": "Карта сайта",
        "sitemap_desc": "Полная структура сайта 123-Kroatien.eu",
        "sitemap_portal_desc": "Ведущий портал недвижимости в Хорватии",
        "sitemap_categories": "Категории страниц",
        "sitemap_heading": "Карта сайта",
        "sitemap_subheading": "Полный обзор всех страниц и функций нашего портала недвижимости",
        "main_pages": "Основные страницы",
        "home": "Главная",
        "all_properties": "Вся недвижимость",
        "about_us": "О нас",
        "contact": "Контакт",
        "faq": "FAQ",
        "legal_info": "Юридическая информация",
        "imprint": "Выходные данные",
        "privacy": "Политика конфиденциальности",
        "terms": "Условия использования",
        "cancellation": "Право отмены",
        "disclaimer": "Отказ от ответственности",
        "service_providers": "Поставщики услуг",
        "real_estate_agent": "Риэлтор",
        "contractor": "Подрядчик",
        "lawyer": "Адвокат",
        "tax_advisor": "Налоговый консультант",
        "architect": "Архитектор",
        "user_area": "Личный кабинет",
        "become_partner": "Стать партнером",
        "register": "Регистрация",
        "login": "Вход",
        "agent_portal": "Портал агента",
        "forgot_password": "Забыли пароль",
        "content_info": "Контент и информация",
        "news": "Новости",
        "market_reports": "Рыночные отчеты",
        "important_addresses": "Важные адреса",
        "glossary": "Глоссарий",
        "tools": "Инструменты и услуги",
        "expert_finder": "Поиск экспертов",
        "ai_search": "Быстрый поиск ИИ",
        "property_search": "Поиск недвижимости",
    },
    "gr": {
        "sitemap_meta_desc": "Πλήρης χάρτης ιστοτόπου 123-Kroatien.eu - Ο οδηγός σας για κροατικά ακίνητα",
        "sitemap_title": "Χάρτης ιστοτόπου",
        "sitemap_desc": "Πλήρης δομή ιστοτόπου 123-Kroatien.eu",
        "sitemap_portal_desc": "Κορυφαία πύλη ακινήτων στην Κροατία",
        "sitemap_categories": "Κατηγορίες σελίδων",
        "sitemap_heading": "Χάρτης ιστοτόπου",
        "sitemap_subheading": "Πλήρης επισκόπηση όλων των σελίδων και λειτουργιών της πύλης ακινήτων μας",
        "main_pages": "Κύριες σελίδες",
        "home": "Αρχική",
        "all_properties": "Όλα τα ακίνητα",
        "about_us": "Σχετικά με εμάς",
        "contact": "Επικοινωνία",
        "faq": "FAQ",
        "legal_info": "Νομικές πληροφορίες",
        "imprint": "Impressum",
        "privacy": "Πολιτική απορρήτου",
        "terms": "Όροι χρήσης",
        "cancellation": "Πολιτική ακύρωσης",
        "disclaimer": "Αποποίηση ευθύνης",
        "service_providers": "Πάροχοι υπηρεσιών",
        "real_estate_agent": "Μεσίτης",
        "contractor": "Κατασκευαστής",
        "lawyer": "Δικηγόρος",
        "tax_advisor": "Φοροτεχνικός",
        "architect": "Αρχιτέκτονας",
        "user_area": "Περιοχή χρήστη",
        "become_partner": "Γίνετε συνεργάτης",
        "register": "Εγγραφή",
        "login": "Σύνδεση",
        "agent_portal": "Πύλη μεσίτη",
        "forgot_password": "Ξεχάσατε τον κωδικό",
        "content_info": "Περιεχόμενο και πληροφορίες",
        "news": "Νέα",
        "market_reports": "Αναφορές αγοράς",
        "important_addresses": "Σημαντικές διευθύνσεις",
        "glossary": "Γλωσσάριο",
        "tools": "Εργαλεία και υπηρεσίες",
        "expert_finder": "Αναζήτηση ειδικών",
        "ai_search": "AI γρήγορη αναζήτηση",
        "property_search": "Αναζήτηση ακινήτων",
    },
    "sw": {
        "sitemap_meta_desc": "Komplett webbplatskarta för 123-Kroatien.eu - Din guide till kroatiska fastigheter",
        "sitemap_title": "Webbplatskarta",
        "sitemap_desc": "Komplett webbplatsstruktur för 123-Kroatien.eu",
        "sitemap_portal_desc": "Ledande fastighetsportal i Kroatien",
        "sitemap_categories": "Sidkategorier",
        "sitemap_heading": "Webbplatskarta",
        "sitemap_subheading": "Komplett översikt över alla sidor och funktioner på vår fastighetsportal",
        "main_pages": "Huvudsidor",
        "home": "Hem",
        "all_properties": "Alla fastigheter",
        "about_us": "Om oss",
        "contact": "Kontakt",
        "faq": "FAQ",
        "legal_info": "Juridisk information",
        "imprint": "Impressum",
        "privacy": "Integritetspolicy",
        "terms": "Allmänna villkor",
        "cancellation": "Ångerrätt",
        "disclaimer": "Ansvarsfriskrivning",
        "service_providers": "Tjänsteleverantörer",
        "real_estate_agent": "Fastighetsmäklare",
        "contractor": "Byggentreprenör",
        "lawyer": "Advokat",
        "tax_advisor": "Skatterådgivare",
        "architect": "Arkitekt",
        "user_area": "Användarområde",
        "become_partner": "Bli partner",
        "register": "Registrera",
        "login": "Logga in",
        "agent_portal": "Mäklarportal",
        "forgot_password": "Glömt lösenord",
        "content_info": "Innehåll och information",
        "news": "Nyheter",
        "market_reports": "Marknadsrapporter",
        "important_addresses": "Viktiga adresser",
        "glossary": "Ordlista",
        "tools": "Verktyg och tjänster",
        "expert_finder": "Expertsökare",
        "ai_search": "AI snabbsökning",
        "property_search": "Fastighetssökning",
    },
    "no": {
        "sitemap_meta_desc": "Komplett nettstedskart for 123-Kroatien.eu - Din guide til kroatisk eiendom",
        "sitemap_title": "Nettstedkart",
        "sitemap_desc": "Komplett nettstedstruktur for 123-Kroatien.eu",
        "sitemap_portal_desc": "Ledende eiendomsportal i Kroatia",
        "sitemap_categories": "Sidekategorier",
        "sitemap_heading": "Nettstedkart",
        "sitemap_subheading": "Komplett oversikt over alle sider og funksjoner på vår eiendomsportal",
        "main_pages": "Hovedsider",
        "home": "Hjem",
        "all_properties": "Alle eiendommer",
        "about_us": "Om oss",
        "contact": "Kontakt",
        "faq": "FAQ",
        "legal_info": "Juridisk informasjon",
        "imprint": "Impressum",
        "privacy": "Personvernpolicy",
        "terms": "Vilkår og betingelser",
        "cancellation": "Angrerett",
        "disclaimer": "Ansvarsfraskrivelse",
        "service_providers": "Tjenesteleverandører",
        "real_estate_agent": "Eiendomsmegler",
        "contractor": "Byggentreprenør",
        "lawyer": "Advokat",
        "tax_advisor": "Skatterådgiver",
        "architect": "Arkitekt",
        "user_area": "Brukerområde",
        "become_partner": "Bli partner",
        "register": "Registrer",
        "login": "Logg inn",
        "agent_portal": "Meglerportal",
        "forgot_password": "Glemt passord",
        "content_info": "Innhold og informasjon",
        "news": "Nyheter",
        "market_reports": "Markedsrapporter",
        "important_addresses": "Viktige adresser",
        "glossary": "Ordliste",
        "tools": "Verktøy og tjenester",
        "expert_finder": "Ekspertsøker",
        "ai_search": "AI hurtigsøk",
        "property_search": "Eiendomssøk",
    },
}


def get_sitemap_translations(request):
    """Stellt Sitemap-Übersetzungen für Templates bereit"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in SITEMAP_TRANSLATIONS else None
    user_language = url_lang or request.session.get("site_language", "ge")
    
    sitemap_trans = SITEMAP_TRANSLATIONS.get(user_language, SITEMAP_TRANSLATIONS["ge"])
    return {f"sm_{k}": v for k, v in sitemap_trans.items()}

# Suchfilter Übersetzungen
SEARCH_FILTER_TRANSLATIONS = {
    "ge": {
        "filter_area_from": "Wohnfläche ab",
        "filter_location": "Standort",
        "filter_rooms": "Zimmer",
        "filter_bathrooms": "Bäder",
        "filter_price_from": "Preis von",
        "filter_price_to": "Preis bis",
    },
    "en": {
        "filter_area_from": "Area from",
        "filter_location": "Location",
        "filter_rooms": "Rooms",
        "filter_bathrooms": "Bathrooms",
        "filter_price_from": "Price from",
        "filter_price_to": "Price to",
    },
    "hr": {
        "filter_area_from": "Površina od",
        "filter_location": "Lokacija",
        "filter_rooms": "Sobe",
        "filter_bathrooms": "Kupaonice",
        "filter_price_from": "Cijena od",
        "filter_price_to": "Cijena do",
    },
    "fr": {
        "filter_area_from": "Surface dès",
        "filter_location": "Emplacement",
        "filter_rooms": "Pièces",
        "filter_bathrooms": "Salles de bain",
        "filter_price_from": "Prix dès",
        "filter_price_to": "Prix jusqu'à",
    },
    "nl": {
        "filter_area_from": "Oppervlakte vanaf",
        "filter_location": "Locatie",
        "filter_rooms": "Kamers",
        "filter_bathrooms": "Badkamers",
        "filter_price_from": "Prijs vanaf",
        "filter_price_to": "Prijs tot",
    },
    "pl": {
        "filter_area_from": "Powierzchnia od",
        "filter_location": "Lokalizacja",
        "filter_rooms": "Pokoje",
        "filter_bathrooms": "Łazienki",
        "filter_price_from": "Cena od",
        "filter_price_to": "Cena do",
    },
    "cz": {
        "filter_area_from": "Plocha od",
        "filter_location": "Lokalita",
        "filter_rooms": "Pokoje",
        "filter_bathrooms": "Koupelny",
        "filter_price_from": "Cena od",
        "filter_price_to": "Cena do",
    },
    "sk": {
        "filter_area_from": "Plocha od",
        "filter_location": "Lokalita",
        "filter_rooms": "Izby",
        "filter_bathrooms": "Kúpeľne",
        "filter_price_from": "Cena od",
        "filter_price_to": "Cena do",
    },
    "ru": {
        "filter_area_from": "Площадь от",
        "filter_location": "Расположение",
        "filter_rooms": "Комнаты",
        "filter_bathrooms": "Ванные",
        "filter_price_from": "Цена от",
        "filter_price_to": "Цена до",
    },
    "gr": {
        "filter_area_from": "Εμβαδόν από",
        "filter_location": "Τοποθεσία",
        "filter_rooms": "Δωμάτια",
        "filter_bathrooms": "Μπάνια",
        "filter_price_from": "Τιμή από",
        "filter_price_to": "Τιμή έως",
    },
    "sw": {
        "filter_area_from": "Yta från",
        "filter_location": "Plats",
        "filter_rooms": "Rum",
        "filter_bathrooms": "Badrum",
        "filter_price_from": "Pris från",
        "filter_price_to": "Pris till",
    },
    "no": {
        "filter_area_from": "Areal fra",
        "filter_location": "Sted",
        "filter_rooms": "Rom",
        "filter_bathrooms": "Bad",
        "filter_price_from": "Pris fra",
        "filter_price_to": "Pris til",
    },
}


def get_search_filter_translations(request):
    """Stellt Suchfilter-Übersetzungen für Templates bereit"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in SEARCH_FILTER_TRANSLATIONS else None
    user_language = url_lang or request.session.get("site_language", "ge")
    
    filter_trans = SEARCH_FILTER_TRANSLATIONS.get(user_language, SEARCH_FILTER_TRANSLATIONS["ge"])
    return filter_trans


# 2FA Setup Übersetzungen
TWO_FA_TRANSLATIONS = {
    "ge": {
        "2fa_title": "Sichere Anmeldung - Schützen Sie Ihr Konto",
        "2fa_instruction": "Scannen Sie diesen QR-Code mit einer Authenticator-App (z.B. Google Authenticator). Danach geben Sie bei jeder Anmeldung einen 6-stelligen Code aus der App ein.",
        "2fa_manual": "Oder geben Sie diesen Code manuell ein:",
        "2fa_activate": "Aktivieren",
        "2fa_placeholder": "6-stelliger Code",
    },
    "en": {
        "2fa_title": "Secure Login - Protect Your Account",
        "2fa_instruction": "Scan this QR code with an authenticator app (e.g. Google Authenticator). After that, you will enter a 6-digit code from the app each time you log in.",
        "2fa_manual": "Or enter this code manually:",
        "2fa_activate": "Activate",
        "2fa_placeholder": "6-digit code",
    },
    "hr": {
        "2fa_title": "Sigurna prijava - Zaštitite svoj račun",
        "2fa_instruction": "Skenirajte ovaj QR kod s aplikacijom za autentifikaciju (npr. Google Authenticator). Nakon toga ćete pri svakoj prijavi unijeti 6-znamenkasti kod iz aplikacije.",
        "2fa_manual": "Ili ručno unesite ovaj kod:",
        "2fa_activate": "Aktiviraj",
        "2fa_placeholder": "6-znamenkasti kod",
    },
    "fr": {
        "2fa_title": "Connexion sécurisée - Protégez votre compte",
        "2fa_instruction": "Scannez ce code QR avec une application d'authentification (ex. Google Authenticator). Ensuite, vous entrerez un code à 6 chiffres à chaque connexion.",
        "2fa_manual": "Ou entrez ce code manuellement:",
        "2fa_activate": "Activer",
        "2fa_placeholder": "Code à 6 chiffres",
    },
    "nl": {
        "2fa_title": "Veilig inloggen - Bescherm uw account",
        "2fa_instruction": "Scan deze QR-code met een authenticator-app (bijv. Google Authenticator). Daarna voert u bij elke login een 6-cijferige code in.",
        "2fa_manual": "Of voer deze code handmatig in:",
        "2fa_activate": "Activeren",
        "2fa_placeholder": "6-cijferige code",
    },
    "pl": {
        "2fa_title": "Bezpieczne logowanie - Chroń swoje konto",
        "2fa_instruction": "Zeskanuj ten kod QR aplikacją uwierzytelniającą (np. Google Authenticator). Następnie przy każdym logowaniu wprowadzisz 6-cyfrowy kod.",
        "2fa_manual": "Lub wprowadź ten kod ręcznie:",
        "2fa_activate": "Aktywuj",
        "2fa_placeholder": "6-cyfrowy kod",
    },
    "cz": {
        "2fa_title": "Bezpečné přihlášení - Chraňte svůj účet",
        "2fa_instruction": "Naskenujte tento QR kód pomocí ověřovací aplikace (např. Google Authenticator). Poté při každém přihlášení zadáte 6místný kód.",
        "2fa_manual": "Nebo zadejte tento kód ručně:",
        "2fa_activate": "Aktivovat",
        "2fa_placeholder": "6místný kód",
    },
    "sk": {
        "2fa_title": "Bezpečné prihlásenie - Chráňte svoj účet",
        "2fa_instruction": "Naskenujte tento QR kód pomocou overovacej aplikácie (napr. Google Authenticator). Potom pri každom prihlásení zadáte 6-miestny kód.",
        "2fa_manual": "Alebo zadajte tento kód ručne:",
        "2fa_activate": "Aktivovať",
        "2fa_placeholder": "6-miestny kód",
    },
    "ru": {
        "2fa_title": "Безопасный вход - Защитите свой аккаунт",
        "2fa_instruction": "Отсканируйте этот QR-код приложением для аутентификации (например, Google Authenticator). После этого при каждом входе вы будете вводить 6-значный код.",
        "2fa_manual": "Или введите этот код вручную:",
        "2fa_activate": "Активировать",
        "2fa_placeholder": "6-значный код",
    },
    "gr": {
        "2fa_title": "Ασφαλής σύνδεση - Προστατέψτε τον λογαριασμό σας",
        "2fa_instruction": "Σαρώστε αυτόν τον κωδικό QR με μια εφαρμογή ελέγχου ταυτότητας (π.χ. Google Authenticator). Μετά θα εισάγετε έναν 6ψήφιο κωδικό σε κάθε σύνδεση.",
        "2fa_manual": "Ή εισάγετε αυτόν τον κωδικό χειροκίνητα:",
        "2fa_activate": "Ενεργοποίηση",
        "2fa_placeholder": "6ψήφιος κωδικός",
    },
    "sw": {
        "2fa_title": "Säker inloggning - Skydda ditt konto",
        "2fa_instruction": "Skanna denna QR-kod med en autentiseringsapp (t.ex. Google Authenticator). Därefter anger du en 6-siffrig kod vid varje inloggning.",
        "2fa_manual": "Eller ange denna kod manuellt:",
        "2fa_activate": "Aktivera",
        "2fa_placeholder": "6-siffrig kod",
    },
    "no": {
        "2fa_title": "Sikker pålogging - Beskytt kontoen din",
        "2fa_instruction": "Skann denne QR-koden med en autentiseringsapp (f.eks. Google Authenticator). Deretter skriver du inn en 6-sifret kode ved hver pålogging.",
        "2fa_manual": "Eller skriv inn denne koden manuelt:",
        "2fa_activate": "Aktiver",
        "2fa_placeholder": "6-sifret kode",
    },
}


def get_2fa_translations(request):
    """Stellt 2FA-Übersetzungen für Templates bereit"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in TWO_FA_TRANSLATIONS else None
    user_language = url_lang or request.session.get("site_language", "ge")
    
    twofa_trans = TWO_FA_TRANSLATIONS.get(user_language, TWO_FA_TRANSLATIONS["ge"])
    return twofa_trans
