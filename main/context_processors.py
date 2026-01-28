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
# CTA Professional Banner (Home)
    cta_professional_title = {
        'ge': 'Sind Sie Immobilienexperte?',
        'en': 'Are you a real estate expert?',
        'hr': 'Jeste li stručnjak za nekretnine?',
        'fr': 'Êtes-vous un expert immobilier?',
        'nl': 'Bent u een vastgoedexpert?',
        'pl': 'Czy jesteś ekspertem od nieruchomości?',
        'cz': 'Jste realitní expert?',
        'sk': 'Ste realitný expert?',
        'ru': 'Вы эксперт по недвижимости?',
        'gr': 'Είστε ειδικός ακινήτων;',
        'sw': 'Är du fastighetsexpert?',
        'no': 'Er du eiendomsekspert?',
    }
    context['cta_professional_title'] = cta_professional_title.get(user_language, 'Sind Sie Immobilienexperte?')

    cta_professional_text = {
        'ge': 'Makler, Architekt, Anwalt oder Steuerberater? Registrieren Sie sich KOSTENLOS und erreichen Sie tausende Kunden!',
        'en': 'Agent, architect, lawyer or tax advisor? Register for FREE and reach thousands of clients!',
        'hr': 'Agent, arhitekt, odvjetnik ili porezni savjetnik? Registrirajte se BESPLATNO i dosegnite tisuće klijenata!',
        'fr': 'Agent, architecte, avocat ou conseiller fiscal? Inscrivez-vous GRATUITEMENT et atteignez des milliers de clients!',
        'nl': 'Makelaar, architect, advocaat of belastingadviseur? Registreer GRATIS en bereik duizenden klanten!',
        'pl': 'Agent, architekt, prawnik lub doradca podatkowy? Zarejestruj się ZA DARMO i dotrzyj do tysięcy klientów!',
        'cz': 'Agent, architekt, právník nebo daňový poradce? Zaregistrujte se ZDARMA a oslovte tisíce klientů!',
        'sk': 'Agent, architekt, právnik alebo daňový poradca? Zaregistrujte sa ZADARMO a oslovte tisíce klientov!',
        'ru': 'Агент, архитектор, юрист или налоговый консультант? Зарегистрируйтесь БЕСПЛАТНО и привлеките тысячи клиентов!',
        'gr': 'Πράκτορας, αρχιτέκτονας, δικηγόρος ή φοροτεχνικός; Εγγραφείτε ΔΩΡΕΑΝ και προσεγγίστε χιλιάδες πελάτες!',
        'sw': 'Mäklare, arkitekt, advokat eller skatterådgivare? Registrera dig GRATIS och nå tusentals kunder!',
        'no': 'Megler, arkitekt, advokat eller skatterådgiver? Registrer deg GRATIS og nå tusenvis av kunder!',
    }
    context['cta_professional_text'] = cta_professional_text.get(user_language, 'Makler, Architekt, Anwalt oder Steuerberater? Registrieren Sie sich KOSTENLOS und erreichen Sie tausende Kunden!')

    cta_professional_button = {
        'ge': 'Kostenlos registrieren',
        'en': 'Register for free',
        'hr': 'Uvodni pristup',
        'fr': 'Inscription gratuite',
        'nl': 'Gratis registreren',
        'pl': 'Zarejestruj się za darmo',
        'cz': 'Registrovat zdarma',
        'sk': 'Registrovať zadarmo',
        'ru': 'Зарегистрироваться бесплатно',
        'gr': 'Εγγραφή δωρεάν',
        'sw': 'Registrera gratis',
        'no': 'Registrer gratis',
    }
    context['cta_professional_button'] = cta_professional_button.get(user_language, 'Kostenlos registrieren')

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
        "filter_property_status": "Kaufen/Mieten",
        "filter_for_sale": "Kaufen",
        "filter_For_Rent": "Mieten",
    },
    "en": {
        "filter_area_from": "Area from",
        "filter_location": "Location",
        "filter_rooms": "Rooms",
        "filter_bathrooms": "Bathrooms",
        "filter_price_from": "Price from",
        "filter_price_to": "Price to",
        "filter_property_status": "Buy/Rent",
        "filter_for_sale": "Buy",
        "filter_For_Rent": "Rent",
    },
    "hr": {
        "filter_area_from": "Površina od",
        "filter_location": "Lokacija",
        "filter_rooms": "Sobe",
        "filter_bathrooms": "Kupaonice",
        "filter_price_from": "Cijena od",
        "filter_price_to": "Cijena do",
        "filter_property_status": "Kupi/Najam",
        "filter_for_sale": "Kupi",
        "filter_For_Rent": "Najam",
    },
    "fr": {
        "filter_area_from": "Surface dès",
        "filter_location": "Emplacement",
        "filter_rooms": "Pièces",
        "filter_bathrooms": "Salles de bain",
        "filter_price_from": "Prix dès",
        "filter_price_to": "Prix jusqu'à",
        "filter_property_status": "Acheter/Louer",
        "filter_for_sale": "Acheter",
        "filter_For_Rent": "Louer",
    },
    "nl": {
        "filter_area_from": "Oppervlakte vanaf",
        "filter_location": "Locatie",
        "filter_rooms": "Kamers",
        "filter_bathrooms": "Badkamers",
        "filter_price_from": "Prijs vanaf",
        "filter_price_to": "Prijs tot",
        "filter_property_status": "Kopen/Huren",
        "filter_for_sale": "Kopen",
        "filter_For_Rent": "Huren",
    },
    "pl": {
        "filter_area_from": "Powierzchnia od",
        "filter_location": "Lokalizacja",
        "filter_rooms": "Pokoje",
        "filter_bathrooms": "Łazienki",
        "filter_price_from": "Cena od",
        "filter_price_to": "Cena do",
        "filter_property_status": "Kupno/Wynajem",
        "filter_for_sale": "Kupno",
        "filter_For_Rent": "Wynajem",
    },
    "cz": {
        "filter_area_from": "Plocha od",
        "filter_location": "Lokalita",
        "filter_rooms": "Pokoje",
        "filter_bathrooms": "Koupelny",
        "filter_price_from": "Cena od",
        "filter_price_to": "Cena do",
        "filter_property_status": "Koupit/Pronájem",
        "filter_for_sale": "Koupit",
        "filter_For_Rent": "Pronájem",
    },
    "sk": {
        "filter_area_from": "Plocha od",
        "filter_location": "Lokalita",
        "filter_rooms": "Izby",
        "filter_bathrooms": "Kúpeľne",
        "filter_price_from": "Cena od",
        "filter_price_to": "Cena do",
        "filter_property_status": "Kúpiť/Prenájom",
        "filter_for_sale": "Kúpiť",
        "filter_For_Rent": "Prenájom",
    },
    "ru": {
        "filter_area_from": "Площадь от",
        "filter_location": "Расположение",
        "filter_rooms": "Комнаты",
        "filter_bathrooms": "Ванные",
        "filter_price_from": "Цена от",
        "filter_price_to": "Цена до",
        "filter_property_status": "Купить/Аренда",
        "filter_for_sale": "Купить",
        "filter_For_Rent": "Аренда",
    },
    "gr": {
        "filter_area_from": "Εμβαδόν από",
        "filter_location": "Τοποθεσία",
        "filter_rooms": "Δωμάτια",
        "filter_bathrooms": "Μπάνια",
        "filter_price_from": "Τιμή από",
        "filter_price_to": "Τιμή έως",
        "filter_property_status": "Αγορά/Ενοικίαση",
        "filter_for_sale": "Αγορά",
        "filter_For_Rent": "Ενοικίαση",
    },
    "sw": {
        "filter_area_from": "Yta från",
        "filter_location": "Plats",
        "filter_rooms": "Rum",
        "filter_bathrooms": "Badrum",
        "filter_price_from": "Pris från",
        "filter_price_to": "Pris till",
        "filter_property_status": "Köpa/Hyra",
        "filter_for_sale": "Köpa",
        "filter_For_Rent": "Hyra",
    },
    "no": {
        "filter_area_from": "Areal fra",
        "filter_location": "Sted",
        "filter_rooms": "Rom",
        "filter_bathrooms": "Bad",
        "filter_price_from": "Pris fra",
        "filter_price_to": "Pris til",
        "filter_property_status": "Kjøpe/Leie",
        "filter_for_sale": "Kjøpe",
        "filter_For_Rent": "Leie",
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


# Buyer Guide Übersetzungen
BUYER_GUIDE_TRANSLATIONS = {
    "ge": {
        "bg_title": "Käuferleitfaden",
        "bg_subtitle": "Immobilienkauf in Kroatien - Schritt für Schritt",
        "bg_step1_title": "OIB-Nummer beantragen",
        "bg_step1_text": "Die OIB (Osobni identifikacijski broj) ist Ihre persönliche Identifikationsnummer in Kroatien. Sie benötigen diese für alle offiziellen Transaktionen.",
        "bg_step1_li1": "Beantragung beim Finanzamt (Porezna uprava)",
        "bg_step1_li2": "Benötigte Dokumente: Reisepass oder Personalausweis",
        "bg_step1_li3": "Bearbeitungszeit: meist sofort oder wenige Tage",
        "bg_step2_title": "Immobilie finden & prüfen",
        "bg_step2_text": "Nehmen Sie sich Zeit für die Suche und prüfen Sie die Immobilie sorgfältig.",
        "bg_step2_li1": "Grundbuchauszug anfordern",
        "bg_step2_li2": "Baugenehmigungen prüfen",
        "bg_step2_li3": "Energieausweis verlangen",
        "bg_tip": "Tipp:",
        "bg_tip_text": "Beauftragen Sie einen unabhängigen Anwalt mit der Due-Diligence-Prüfung.",
        "bg_step3_title": "Vorvertrag & Anzahlung",
        "bg_step3_text": "Der Vorvertrag sichert beide Parteien ab. Die übliche Anzahlung beträgt 10% des Kaufpreises.",
        "bg_step4_title": "Notartermin & Kaufvertrag",
        "bg_step4_text": "Der Kaufvertrag wird vom Notar beurkundet. Grunderwerbsteuer beträgt 3%.",
        "bg_step5_title": "Grundbucheintragung",
        "bg_step5_text": "Erst mit Eintragung sind Sie offiziell Eigentümer. Bearbeitungszeit: 2-4 Wochen.",
        "bg_cta_title": "Fragen zum Immobilienkauf?",
        "bg_cta_text": "Unsere Experten helfen Ihnen gerne",
        "bg_cta_button": "Kontakt aufnehmen",
        "bg_lang_select": "Sprache wählen",
    },
    "en": {
        "bg_title": "Property Buyer Guide",
        "bg_subtitle": "Buying property in Croatia - step by step",
        "bg_step1_title": "Apply for OIB Number",
        "bg_step1_text": "The OIB (Osobni identifikacijski broj) is your personal identification number in Croatia. You need this for all official transactions.",
        "bg_step1_li1": "Apply at the Tax Office (Porezna uprava)",
        "bg_step1_li2": "Required documents: Passport or ID card",
        "bg_step1_li3": "Processing time: usually immediate or a few days",
        "bg_step2_title": "Find & Inspect Property",
        "bg_step2_text": "Take your time searching and carefully inspect the property.",
        "bg_step2_li1": "Request land registry extract",
        "bg_step2_li2": "Check building permits",
        "bg_step2_li3": "Request energy certificate",
        "bg_tip": "Tip:",
        "bg_tip_text": "Hire an independent lawyer for due diligence.",
        "bg_step3_title": "Pre-contract & Deposit",
        "bg_step3_text": "The pre-contract secures both parties. The usual deposit is 10% of the purchase price.",
        "bg_step4_title": "Notary Appointment",
        "bg_step4_text": "The purchase contract is notarized. Property transfer tax is 3%.",
        "bg_step5_title": "Land Registry Entry",
        "bg_step5_text": "Only with entry are you officially the owner. Processing time: 2-4 weeks.",
        "bg_cta_title": "Questions about buying?",
        "bg_cta_text": "Our experts are happy to help",
        "bg_cta_button": "Contact us",
        "bg_lang_select": "Select language",
    },
    "hr": {
        "bg_title": "Vodič za kupce nekretnina",
        "bg_subtitle": "Kupnja nekretnine u Hrvatskoj - korak po korak",
        "bg_step1_title": "Zatražite OIB broj",
        "bg_step1_text": "OIB (Osobni identifikacijski broj) je vaš osobni identifikacijski broj u Hrvatskoj. Potreban vam je za sve službene transakcije.",
        "bg_step1_li1": "Zahtjev u Poreznoj upravi",
        "bg_step1_li2": "Potrebni dokumenti: Putovnica ili osobna iskaznica",
        "bg_step1_li3": "Vrijeme obrade: obično odmah ili nekoliko dana",
        "bg_step2_title": "Pronađite i pregledajte nekretninu",
        "bg_step2_text": "Uzmite si vremena za pretragu i pažljivo pregledajte nekretninu.",
        "bg_step2_li1": "Zatražite izvadak iz zemljišne knjige",
        "bg_step2_li2": "Provjerite građevinske dozvole",
        "bg_step2_li3": "Zatražite energetski certifikat",
        "bg_tip": "Savjet:",
        "bg_tip_text": "Angažirajte neovisnog odvjetnika za dubinsku analizu.",
        "bg_step3_title": "Predugovor i kapara",
        "bg_step3_text": "Predugovor osigurava obje strane. Uobičajena kapara iznosi 10% kupoprodajne cijene.",
        "bg_step4_title": "Javnobilježnički termin",
        "bg_step4_text": "Kupoprodajni ugovor ovjerava javni bilježnik. Porez na promet nekretnina iznosi 3%.",
        "bg_step5_title": "Upis u zemljišnu knjigu",
        "bg_step5_text": "Tek s upisom ste službeno vlasnik. Vrijeme obrade: 2-4 tjedna.",
        "bg_cta_title": "Pitanja o kupnji?",
        "bg_cta_text": "Naši stručnjaci rado pomažu",
        "bg_cta_button": "Kontaktirajte nas",
        "bg_lang_select": "Odaberite jezik",
    },
    "fr": {
        "bg_title": "Guide de l'acheteur",
        "bg_subtitle": "Acheter en Croatie - étape par étape",
        "bg_step1_title": "Demander un numéro OIB",
        "bg_step1_text": "L'OIB est votre numéro d'identification personnel en Croatie. Vous en avez besoin pour toutes les transactions officielles.",
        "bg_step1_li1": "Demande au bureau des impôts",
        "bg_step1_li2": "Documents requis: Passeport ou carte d'identité",
        "bg_step1_li3": "Délai de traitement: généralement immédiat ou quelques jours",
        "bg_step2_title": "Trouver et inspecter le bien",
        "bg_step2_text": "Prenez votre temps pour chercher et inspectez soigneusement le bien.",
        "bg_step2_li1": "Demander un extrait du registre foncier",
        "bg_step2_li2": "Vérifier les permis de construire",
        "bg_step2_li3": "Demander le certificat énergétique",
        "bg_tip": "Conseil:",
        "bg_tip_text": "Engagez un avocat indépendant pour la vérification.",
        "bg_step3_title": "Pré-contrat et acompte",
        "bg_step3_text": "Le pré-contrat sécurise les deux parties. L'acompte habituel est de 10% du prix.",
        "bg_step4_title": "Rendez-vous notaire",
        "bg_step4_text": "Le contrat d'achat est notarié. La taxe de transfert est de 3%.",
        "bg_step5_title": "Inscription au registre foncier",
        "bg_step5_text": "C'est seulement avec l'inscription que vous êtes officiellement propriétaire. Délai: 2-4 semaines.",
        "bg_cta_title": "Questions sur l'achat?",
        "bg_cta_text": "Nos experts sont là pour vous",
        "bg_cta_button": "Contactez-nous",
        "bg_lang_select": "Choisir la langue",
    },
    "nl": {
        "bg_title": "Koopgids",
        "bg_subtitle": "Vastgoed kopen in Kroatië - stap voor stap",
        "bg_step1_title": "OIB-nummer aanvragen",
        "bg_step1_text": "De OIB is uw persoonlijk identificatienummer in Kroatië. U heeft dit nodig voor alle officiële transacties.",
        "bg_step1_li1": "Aanvraag bij de belastingdienst",
        "bg_step1_li2": "Vereiste documenten: Paspoort of ID-kaart",
        "bg_step1_li3": "Verwerkingstijd: meestal direct of enkele dagen",
        "bg_step2_title": "Vind en inspecteer eigendom",
        "bg_step2_text": "Neem de tijd om te zoeken en inspecteer het pand zorgvuldig.",
        "bg_step2_li1": "Vraag kadasteruittreksel aan",
        "bg_step2_li2": "Controleer bouwvergunningen",
        "bg_step2_li3": "Vraag energiecertificaat aan",
        "bg_tip": "Tip:",
        "bg_tip_text": "Huur een onafhankelijke advocaat in voor due diligence.",
        "bg_step3_title": "Voorcontract en aanbetaling",
        "bg_step3_text": "Het voorcontract beveiligt beide partijen. De gebruikelijke aanbetaling is 10%.",
        "bg_step4_title": "Notarisafspraak",
        "bg_step4_text": "Het koopcontract wordt notarieel vastgelegd. Overdrachtsbelasting is 3%.",
        "bg_step5_title": "Kadasterinschrijving",
        "bg_step5_text": "Pas met inschrijving bent u officieel eigenaar. Verwerkingstijd: 2-4 weken.",
        "bg_cta_title": "Vragen over kopen?",
        "bg_cta_text": "Onze experts helpen graag",
        "bg_cta_button": "Neem contact op",
        "bg_lang_select": "Taal kiezen",
    },
    "pl": {
        "bg_title": "Poradnik kupującego",
        "bg_subtitle": "Kupno nieruchomości w Chorwacji - krok po kroku",
        "bg_step1_title": "Złóż wniosek o numer OIB",
        "bg_step1_text": "OIB to Twój osobisty numer identyfikacyjny w Chorwacji. Potrzebujesz go do wszystkich oficjalnych transakcji.",
        "bg_step1_li1": "Wniosek w urzędzie skarbowym",
        "bg_step1_li2": "Wymagane dokumenty: Paszport lub dowód osobisty",
        "bg_step1_li3": "Czas realizacji: zwykle natychmiast lub kilka dni",
        "bg_step2_title": "Znajdź i sprawdź nieruchomość",
        "bg_step2_text": "Poświęć czas na poszukiwania i dokładnie sprawdź nieruchomość.",
        "bg_step2_li1": "Poproś o wypis z księgi wieczystej",
        "bg_step2_li2": "Sprawdź pozwolenia na budowę",
        "bg_step2_li3": "Poproś o świadectwo energetyczne",
        "bg_tip": "Wskazówka:",
        "bg_tip_text": "Zatrudnij niezależnego prawnika do analizy.",
        "bg_step3_title": "Umowa przedwstępna i zaliczka",
        "bg_step3_text": "Umowa przedwstępna zabezpiecza obie strony. Zwykła zaliczka to 10%.",
        "bg_step4_title": "Wizyta u notariusza",
        "bg_step4_text": "Umowa kupna jest poświadczona notarialnie. Podatek od przeniesienia wynosi 3%.",
        "bg_step5_title": "Wpis do księgi wieczystej",
        "bg_step5_text": "Dopiero z wpisem jesteś oficjalnie właścicielem. Czas: 2-4 tygodnie.",
        "bg_cta_title": "Pytania o zakup?",
        "bg_cta_text": "Nasi eksperci chętnie pomogą",
        "bg_cta_button": "Skontaktuj się",
        "bg_lang_select": "Wybierz język",
    },
    "cz": {
        "bg_title": "Průvodce kupujícího",
        "bg_subtitle": "Koupě nemovitosti v Chorvatsku - krok za krokem",
        "bg_step1_title": "Požádejte o číslo OIB",
        "bg_step1_text": "OIB je vaše osobní identifikační číslo v Chorvatsku. Potřebujete ho pro všechny oficiální transakce.",
        "bg_step1_li1": "Žádost na finančním úřadě",
        "bg_step1_li2": "Požadované dokumenty: Pas nebo občanský průkaz",
        "bg_step1_li3": "Doba zpracování: obvykle ihned nebo několik dní",
        "bg_step2_title": "Najděte a prohlédněte nemovitost",
        "bg_step2_text": "Věnujte čas hledání a pečlivě si nemovitost prohlédněte.",
        "bg_step2_li1": "Vyžádejte si výpis z katastru",
        "bg_step2_li2": "Zkontrolujte stavební povolení",
        "bg_step2_li3": "Vyžádejte si energetický průkaz",
        "bg_tip": "Tip:",
        "bg_tip_text": "Najměte si nezávislého právníka na prověrku.",
        "bg_step3_title": "Předběžná smlouva a záloha",
        "bg_step3_text": "Předběžná smlouva zajišťuje obě strany. Obvyklá záloha je 10%.",
        "bg_step4_title": "Schůzka u notáře",
        "bg_step4_text": "Kupní smlouva je notářsky ověřena. Daň z převodu je 3%.",
        "bg_step5_title": "Zápis do katastru",
        "bg_step5_text": "Teprve zápisem jste oficiálně vlastníkem. Doba: 2-4 týdny.",
        "bg_cta_title": "Otázky ke koupi?",
        "bg_cta_text": "Naši odborníci rádi pomohou",
        "bg_cta_button": "Kontaktujte nás",
        "bg_lang_select": "Vybrat jazyk",
    },
    "sk": {
        "bg_title": "Sprievodca kupujúceho",
        "bg_subtitle": "Kúpa nehnuteľnosti v Chorvátsku - krok za krokom",
        "bg_step1_title": "Požiadajte o číslo OIB",
        "bg_step1_text": "OIB je vaše osobné identifikačné číslo v Chorvátsku. Potrebujete ho pre všetky oficiálne transakcie.",
        "bg_step1_li1": "Žiadosť na daňovom úrade",
        "bg_step1_li2": "Požadované dokumenty: Pas alebo občiansky preukaz",
        "bg_step1_li3": "Čas spracovania: zvyčajne ihneď alebo niekoľko dní",
        "bg_step2_title": "Nájdite a prezrite nehnuteľnosť",
        "bg_step2_text": "Venujte čas hľadaniu a dôkladne si nehnuteľnosť prezrite.",
        "bg_step2_li1": "Vyžiadajte si výpis z katastra",
        "bg_step2_li2": "Skontrolujte stavebné povolenia",
        "bg_step2_li3": "Vyžiadajte si energetický certifikát",
        "bg_tip": "Tip:",
        "bg_tip_text": "Najnite si nezávislého právnika na previerku.",
        "bg_step3_title": "Predbežná zmluva a záloha",
        "bg_step3_text": "Predbežná zmluva zabezpečuje obe strany. Obvyklá záloha je 10%.",
        "bg_step4_title": "Stretnutie u notára",
        "bg_step4_text": "Kúpna zmluva je notársky overená. Daň z prevodu je 3%.",
        "bg_step5_title": "Zápis do katastra",
        "bg_step5_text": "Až zápisom ste oficiálne vlastníkom. Čas: 2-4 týždne.",
        "bg_cta_title": "Otázky ku kúpe?",
        "bg_cta_text": "Naši odborníci radi pomôžu",
        "bg_cta_button": "Kontaktujte nás",
        "bg_lang_select": "Vybrať jazyk",
    },
    "ru": {
        "bg_title": "Руководство покупателя",
        "bg_subtitle": "Покупка недвижимости в Хорватии - шаг за шагом",
        "bg_step1_title": "Подайте заявку на номер OIB",
        "bg_step1_text": "OIB - это ваш личный идентификационный номер в Хорватии. Он нужен для всех официальных транзакций.",
        "bg_step1_li1": "Заявление в налоговой",
        "bg_step1_li2": "Необходимые документы: Паспорт или удостоверение личности",
        "bg_step1_li3": "Время обработки: обычно сразу или несколько дней",
        "bg_step2_title": "Найдите и осмотрите недвижимость",
        "bg_step2_text": "Не торопитесь с поиском и тщательно осмотрите недвижимость.",
        "bg_step2_li1": "Запросите выписку из земельного реестра",
        "bg_step2_li2": "Проверьте разрешения на строительство",
        "bg_step2_li3": "Запросите энергетический сертификат",
        "bg_tip": "Совет:",
        "bg_tip_text": "Наймите независимого юриста для проверки.",
        "bg_step3_title": "Предварительный договор и задаток",
        "bg_step3_text": "Предварительный договор защищает обе стороны. Обычный задаток - 10%.",
        "bg_step4_title": "Встреча с нотариусом",
        "bg_step4_text": "Договор купли-продажи заверяется нотариусом. Налог на передачу - 3%.",
        "bg_step5_title": "Регистрация в реестре",
        "bg_step5_text": "Только после регистрации вы официально владелец. Срок: 2-4 недели.",
        "bg_cta_title": "Вопросы о покупке?",
        "bg_cta_text": "Наши эксперты рады помочь",
        "bg_cta_button": "Связаться",
        "bg_lang_select": "Выбрать язык",
    },
    "gr": {
        "bg_title": "Οδηγός αγοραστή",
        "bg_subtitle": "Αγορά ακινήτου στην Κροατία - βήμα προς βήμα",
        "bg_step1_title": "Υποβολή αίτησης για αριθμό OIB",
        "bg_step1_text": "Το OIB είναι ο προσωπικός σας αριθμός ταυτότητας στην Κροατία. Το χρειάζεστε για όλες τις επίσημες συναλλαγές.",
        "bg_step1_li1": "Αίτηση στην εφορία",
        "bg_step1_li2": "Απαιτούμενα έγγραφα: Διαβατήριο ή ταυτότητα",
        "bg_step1_li3": "Χρόνος επεξεργασίας: συνήθως άμεσα ή λίγες μέρες",
        "bg_step2_title": "Βρείτε και επιθεωρήστε το ακίνητο",
        "bg_step2_text": "Αφιερώστε χρόνο στην αναζήτηση και επιθεωρήστε προσεκτικά το ακίνητο.",
        "bg_step2_li1": "Ζητήστε απόσπασμα κτηματολογίου",
        "bg_step2_li2": "Ελέγξτε τις οικοδομικές άδειες",
        "bg_step2_li3": "Ζητήστε ενεργειακό πιστοποιητικό",
        "bg_tip": "Συμβουλή:",
        "bg_tip_text": "Προσλάβετε ανεξάρτητο δικηγόρο για έλεγχο.",
        "bg_step3_title": "Προσύμφωνο και προκαταβολή",
        "bg_step3_text": "Το προσύμφωνο εξασφαλίζει και τα δύο μέρη. Η συνήθης προκαταβολή είναι 10%.",
        "bg_step4_title": "Ραντεβού συμβολαιογράφου",
        "bg_step4_text": "Το συμβόλαιο αγοράς συντάσσεται από συμβολαιογράφο. Ο φόρος μεταβίβασης είναι 3%.",
        "bg_step5_title": "Εγγραφή στο κτηματολόγιο",
        "bg_step5_text": "Μόνο με την εγγραφή είστε επίσημα ιδιοκτήτης. Χρόνος: 2-4 εβδομάδες.",
        "bg_cta_title": "Ερωτήσεις για αγορά?",
        "bg_cta_text": "Οι ειδικοί μας είναι στη διάθεσή σας",
        "bg_cta_button": "Επικοινωνήστε",
        "bg_lang_select": "Επιλέξτε γλώσσα",
    },
    "sw": {
        "bg_title": "Köpguide",
        "bg_subtitle": "Köpa fastighet i Kroatien - steg för steg",
        "bg_step1_title": "Ansök om OIB-nummer",
        "bg_step1_text": "OIB är ditt personliga identifikationsnummer i Kroatien. Du behöver det för alla officiella transaktioner.",
        "bg_step1_li1": "Ansökan på skattekontoret",
        "bg_step1_li2": "Nödvändiga dokument: Pass eller ID-kort",
        "bg_step1_li3": "Handläggningstid: vanligtvis omedelbart eller några dagar",
        "bg_step2_title": "Hitta och inspektera fastighet",
        "bg_step2_text": "Ta dig tid att söka och inspektera fastigheten noggrant.",
        "bg_step2_li1": "Begär fastighetsregisterutdrag",
        "bg_step2_li2": "Kontrollera bygglov",
        "bg_step2_li3": "Begär energicertifikat",
        "bg_tip": "Tips:",
        "bg_tip_text": "Anlita en oberoende advokat för due diligence.",
        "bg_step3_title": "Förkontrakt och handpenning",
        "bg_step3_text": "Förkontraktet säkrar båda parter. Den vanliga handpenningen är 10%.",
        "bg_step4_title": "Notariemöte",
        "bg_step4_text": "Köpekontraktet notariseras. Överlåtelseskatten är 3%.",
        "bg_step5_title": "Fastighetsregistrering",
        "bg_step5_text": "Först med registrering är du officiellt ägare. Tid: 2-4 veckor.",
        "bg_cta_title": "Frågor om köp?",
        "bg_cta_text": "Våra experter hjälper gärna",
        "bg_cta_button": "Kontakta oss",
        "bg_lang_select": "Välj språk",
    },
    "no": {
        "bg_title": "Kjøperguide",
        "bg_subtitle": "Kjøp av eiendom i Kroatia - steg for steg",
        "bg_step1_title": "Søk om OIB-nummer",
        "bg_step1_text": "OIB er ditt personlige identifikasjonsnummer i Kroatia. Du trenger det for alle offisielle transaksjoner.",
        "bg_step1_li1": "Søknad på skattekontoret",
        "bg_step1_li2": "Nødvendige dokumenter: Pass eller ID-kort",
        "bg_step1_li3": "Behandlingstid: vanligvis umiddelbart eller noen dager",
        "bg_step2_title": "Finn og inspiser eiendom",
        "bg_step2_text": "Ta deg tid til å søke og inspiser eiendommen nøye.",
        "bg_step2_li1": "Be om utdrag fra grunnboken",
        "bg_step2_li2": "Sjekk byggetillatelser",
        "bg_step2_li3": "Be om energisertifikat",
        "bg_tip": "Tips:",
        "bg_tip_text": "Ansett en uavhengig advokat for due diligence.",
        "bg_step3_title": "Forhåndskontrakt og depositum",
        "bg_step3_text": "Forhåndskontrakten sikrer begge parter. Det vanlige depositumet er 10%.",
        "bg_step4_title": "Notarmøte",
        "bg_step4_text": "Kjøpekontrakten notariseres. Overføringsskatten er 3%.",
        "bg_step5_title": "Grunnbokregistrering",
        "bg_step5_text": "Først med registrering er du offisielt eier. Tid: 2-4 uker.",
        "bg_cta_title": "Spørsmål om kjøp?",
        "bg_cta_text": "Våre eksperter hjelper gjerne",
        "bg_cta_button": "Kontakt oss",
        "bg_lang_select": "Velg språk",
    },
}


def get_buyer_guide_translations(request):
    """Stellt Buyer Guide Übersetzungen für Templates bereit"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in BUYER_GUIDE_TRANSLATIONS else None
    user_language = url_lang or request.session.get("site_language", "ge")
    
    bg_trans = BUYER_GUIDE_TRANSLATIONS.get(user_language, BUYER_GUIDE_TRANSLATIONS["ge"])
    return bg_trans


# Professional Detail Übersetzungen
PROFESSIONAL_DETAIL_TRANSLATIONS = {
    "ge": {
        "pd_about_us": "Über uns",
        "pd_no_description": "Keine Beschreibung vorhanden.",
        "pd_specializations": "Spezialgebiete",
        "pd_contact": "Kontakt",
        "pd_verified_provider": "Verifizierter Anbieter",
        "pd_send_message": "Nachricht senden",
        "pd_your_name": "Ihr Name",
        "pd_your_email": "Ihre E-Mail",
        "pd_your_phone": "Ihre Telefonnummer",
        "pd_your_message": "Ihre Nachricht",
        "pd_send": "Absenden",
        "pd_message_sent": "Nachricht gesendet!",
        "pd_languages": "Sprachen",
        "pd_regions": "Regionen",
        "pd_references": "Referenzprojekte",
        "pd_properties": "Immobilien",
        "pd_opening_hours": "Öffnungszeiten",
        "pd_closed": "Geschlossen",
        "pd_verified": "Verifiziert",
        "pd_back_to_list": "Zurück zur Liste",
    },
    "en": {
        "pd_about_us": "About Us",
        "pd_no_description": "No description available.",
        "pd_specializations": "Specializations",
        "pd_contact": "Contact",
        "pd_verified_provider": "Verified Provider",
        "pd_send_message": "Send Message",
        "pd_your_name": "Your Name",
        "pd_your_email": "Your Email",
        "pd_your_phone": "Your Phone",
        "pd_your_message": "Your Message",
        "pd_send": "Send",
        "pd_message_sent": "Message sent!",
        "pd_languages": "Languages",
        "pd_regions": "Regions",
        "pd_references": "Reference Projects",
        "pd_properties": "Properties",
        "pd_opening_hours": "Opening Hours",
        "pd_closed": "Closed",
        "pd_verified": "Verified",
        "pd_back_to_list": "Back to List",
    },
    "hr": {
        "pd_about_us": "O nama",
        "pd_no_description": "Nema opisa.",
        "pd_specializations": "Specijalizacije",
        "pd_contact": "Kontakt",
        "pd_verified_provider": "Verificirani pružatelj",
        "pd_send_message": "Pošalji poruku",
        "pd_your_name": "Vaše ime",
        "pd_your_email": "Vaš email",
        "pd_your_phone": "Vaš telefon",
        "pd_your_message": "Vaša poruka",
        "pd_send": "Pošalji",
        "pd_message_sent": "Poruka poslana!",
        "pd_languages": "Jezici",
        "pd_regions": "Regije",
        "pd_references": "Referentni projekti",
        "pd_properties": "Nekretnine",
        "pd_opening_hours": "Radno vrijeme",
        "pd_closed": "Zatvoreno",
        "pd_verified": "Verificirano",
        "pd_back_to_list": "Natrag na popis",
    },
    "fr": {
        "pd_about_us": "À propos",
        "pd_no_description": "Aucune description disponible.",
        "pd_specializations": "Spécialisations",
        "pd_contact": "Contact",
        "pd_verified_provider": "Prestataire vérifié",
        "pd_send_message": "Envoyer un message",
        "pd_your_name": "Votre nom",
        "pd_your_email": "Votre email",
        "pd_your_phone": "Votre téléphone",
        "pd_your_message": "Votre message",
        "pd_send": "Envoyer",
        "pd_message_sent": "Message envoyé!",
        "pd_languages": "Langues",
        "pd_regions": "Régions",
        "pd_references": "Projets de référence",
        "pd_properties": "Propriétés",
        "pd_opening_hours": "Horaires",
        "pd_closed": "Fermé",
        "pd_verified": "Vérifié",
        "pd_back_to_list": "Retour à la liste",
    },
    "nl": {
        "pd_about_us": "Over ons",
        "pd_no_description": "Geen beschrijving beschikbaar.",
        "pd_specializations": "Specialisaties",
        "pd_contact": "Contact",
        "pd_verified_provider": "Geverifieerde aanbieder",
        "pd_send_message": "Bericht sturen",
        "pd_your_name": "Uw naam",
        "pd_your_email": "Uw email",
        "pd_your_phone": "Uw telefoon",
        "pd_your_message": "Uw bericht",
        "pd_send": "Versturen",
        "pd_message_sent": "Bericht verzonden!",
        "pd_languages": "Talen",
        "pd_regions": "Regio's",
        "pd_references": "Referentieprojecten",
        "pd_properties": "Vastgoed",
        "pd_opening_hours": "Openingstijden",
        "pd_closed": "Gesloten",
        "pd_verified": "Geverifieerd",
        "pd_back_to_list": "Terug naar lijst",
    },
    "pl": {
        "pd_about_us": "O nas",
        "pd_no_description": "Brak opisu.",
        "pd_specializations": "Specjalizacje",
        "pd_contact": "Kontakt",
        "pd_verified_provider": "Zweryfikowany dostawca",
        "pd_send_message": "Wyślij wiadomość",
        "pd_your_name": "Twoje imię",
        "pd_your_email": "Twój email",
        "pd_your_phone": "Twój telefon",
        "pd_your_message": "Twoja wiadomość",
        "pd_send": "Wyślij",
        "pd_message_sent": "Wiadomość wysłana!",
        "pd_languages": "Języki",
        "pd_regions": "Regiony",
        "pd_references": "Projekty referencyjne",
        "pd_properties": "Nieruchomości",
        "pd_opening_hours": "Godziny otwarcia",
        "pd_closed": "Zamknięte",
        "pd_verified": "Zweryfikowany",
        "pd_back_to_list": "Powrót do listy",
    },
    "cz": {
        "pd_about_us": "O nás",
        "pd_no_description": "Žádný popis.",
        "pd_specializations": "Specializace",
        "pd_contact": "Kontakt",
        "pd_verified_provider": "Ověřený poskytovatel",
        "pd_send_message": "Odeslat zprávu",
        "pd_your_name": "Vaše jméno",
        "pd_your_email": "Váš email",
        "pd_your_phone": "Váš telefon",
        "pd_your_message": "Vaše zpráva",
        "pd_send": "Odeslat",
        "pd_message_sent": "Zpráva odeslána!",
        "pd_languages": "Jazyky",
        "pd_regions": "Regiony",
        "pd_references": "Referenční projekty",
        "pd_properties": "Nemovitosti",
        "pd_opening_hours": "Otevírací doba",
        "pd_closed": "Zavřeno",
        "pd_verified": "Ověřeno",
        "pd_back_to_list": "Zpět na seznam",
    },
    "sk": {
        "pd_about_us": "O nás",
        "pd_no_description": "Žiadny popis.",
        "pd_specializations": "Špecializácie",
        "pd_contact": "Kontakt",
        "pd_verified_provider": "Overený poskytovateľ",
        "pd_send_message": "Odoslať správu",
        "pd_your_name": "Vaše meno",
        "pd_your_email": "Váš email",
        "pd_your_phone": "Váš telefón",
        "pd_your_message": "Vaša správa",
        "pd_send": "Odoslať",
        "pd_message_sent": "Správa odoslaná!",
        "pd_languages": "Jazyky",
        "pd_regions": "Regióny",
        "pd_references": "Referenčné projekty",
        "pd_properties": "Nehnuteľnosti",
        "pd_opening_hours": "Otváracie hodiny",
        "pd_closed": "Zatvorené",
        "pd_verified": "Overené",
        "pd_back_to_list": "Späť na zoznam",
    },
    "ru": {
        "pd_about_us": "О нас",
        "pd_no_description": "Описание отсутствует.",
        "pd_specializations": "Специализации",
        "pd_contact": "Контакт",
        "pd_verified_provider": "Проверенный поставщик",
        "pd_send_message": "Отправить сообщение",
        "pd_your_name": "Ваше имя",
        "pd_your_email": "Ваш email",
        "pd_your_phone": "Ваш телефон",
        "pd_your_message": "Ваше сообщение",
        "pd_send": "Отправить",
        "pd_message_sent": "Сообщение отправлено!",
        "pd_languages": "Языки",
        "pd_regions": "Регионы",
        "pd_references": "Референсные проекты",
        "pd_properties": "Недвижимость",
        "pd_opening_hours": "Часы работы",
        "pd_closed": "Закрыто",
        "pd_verified": "Проверено",
        "pd_back_to_list": "Назад к списку",
    },
    "gr": {
        "pd_about_us": "Σχετικά με εμάς",
        "pd_no_description": "Δεν υπάρχει περιγραφή.",
        "pd_specializations": "Εξειδικεύσεις",
        "pd_contact": "Επικοινωνία",
        "pd_verified_provider": "Επαληθευμένος πάροχος",
        "pd_send_message": "Αποστολή μηνύματος",
        "pd_your_name": "Το όνομά σας",
        "pd_your_email": "Το email σας",
        "pd_your_phone": "Το τηλέφωνό σας",
        "pd_your_message": "Το μήνυμά σας",
        "pd_send": "Αποστολή",
        "pd_message_sent": "Το μήνυμα στάλθηκε!",
        "pd_languages": "Γλώσσες",
        "pd_regions": "Περιοχές",
        "pd_references": "Έργα αναφοράς",
        "pd_properties": "Ακίνητα",
        "pd_opening_hours": "Ώρες λειτουργίας",
        "pd_closed": "Κλειστό",
        "pd_verified": "Επαληθευμένο",
        "pd_back_to_list": "Επιστροφή στη λίστα",
    },
    "sw": {
        "pd_about_us": "Om oss",
        "pd_no_description": "Ingen beskrivning tillgänglig.",
        "pd_specializations": "Specialiseringar",
        "pd_contact": "Kontakt",
        "pd_verified_provider": "Verifierad leverantör",
        "pd_send_message": "Skicka meddelande",
        "pd_your_name": "Ditt namn",
        "pd_your_email": "Din email",
        "pd_your_phone": "Ditt telefon",
        "pd_your_message": "Ditt meddelande",
        "pd_send": "Skicka",
        "pd_message_sent": "Meddelande skickat!",
        "pd_languages": "Språk",
        "pd_regions": "Regioner",
        "pd_references": "Referensprojekt",
        "pd_properties": "Fastigheter",
        "pd_opening_hours": "Öppettider",
        "pd_closed": "Stängt",
        "pd_verified": "Verifierad",
        "pd_back_to_list": "Tillbaka till listan",
    },
    "no": {
        "pd_about_us": "Om oss",
        "pd_no_description": "Ingen beskrivelse tilgjengelig.",
        "pd_specializations": "Spesialiseringer",
        "pd_contact": "Kontakt",
        "pd_verified_provider": "Verifisert leverandør",
        "pd_send_message": "Send melding",
        "pd_your_name": "Ditt navn",
        "pd_your_email": "Din email",
        "pd_your_phone": "Din telefon",
        "pd_your_message": "Din melding",
        "pd_send": "Send",
        "pd_message_sent": "Melding sendt!",
        "pd_languages": "Språk",
        "pd_regions": "Regioner",
        "pd_references": "Referanseprosjekter",
        "pd_properties": "Eiendommer",
        "pd_opening_hours": "Åpningstider",
        "pd_closed": "Stengt",
        "pd_verified": "Verifisert",
        "pd_back_to_list": "Tilbake til listen",
    },
}


def get_professional_detail_translations(request):
    """Stellt Professional Detail Übersetzungen für Templates bereit"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in PROFESSIONAL_DETAIL_TRANSLATIONS else None
    user_language = url_lang or request.session.get("site_language", "ge")
    
    pd_trans = PROFESSIONAL_DETAIL_TRANSLATIONS.get(user_language, PROFESSIONAL_DETAIL_TRANSLATIONS["ge"])
    return pd_trans


# Navigation Mega Menu Übersetzungen
NAV_MENU_TRANSLATIONS = {
    "ge": {
        "nav_property_types": "Immobilienarten",
        "nav_popular_regions": "Beliebte Regionen",
        "nav_price": "Preis",
        "nav_real_estate": "Immobilien",
        "nav_planning_law": "Planung und Recht",
        "nav_find_expert": "Finden Sie den passenden Experten",
        "nav_search_now": "Jetzt suchen",
    },
    "en": {
        "nav_property_types": "Property Types",
        "nav_popular_regions": "Popular Regions",
        "nav_price": "Price",
        "nav_real_estate": "Real Estate",
        "nav_planning_law": "Planning and Law",
        "nav_find_expert": "Find the right expert",
        "nav_search_now": "Search now",
    },
    "hr": {
        "nav_property_types": "Vrste nekretnina",
        "nav_popular_regions": "Popularne regije",
        "nav_price": "Cijena",
        "nav_real_estate": "Nekretnine",
        "nav_planning_law": "Planiranje i pravo",
        "nav_find_expert": "Pronadite pravog strucnjaka",
        "nav_search_now": "Trazi sada",
    },
    "fr": {
        "nav_property_types": "Types de biens",
        "nav_popular_regions": "Regions populaires",
        "nav_price": "Prix",
        "nav_real_estate": "Immobilier",
        "nav_planning_law": "Planification et droit",
        "nav_find_expert": "Trouvez le bon expert",
        "nav_search_now": "Rechercher",
    },
    "nl": {
        "nav_property_types": "Soorten vastgoed",
        "nav_popular_regions": "Populaire regios",
        "nav_price": "Prijs",
        "nav_real_estate": "Vastgoed",
        "nav_planning_law": "Planning en recht",
        "nav_find_expert": "Vind de juiste expert",
        "nav_search_now": "Zoek nu",
    },
    "pl": {
        "nav_property_types": "Rodzaje nieruchomosci",
        "nav_popular_regions": "Popularne regiony",
        "nav_price": "Cena",
        "nav_real_estate": "Nieruchomosci",
        "nav_planning_law": "Planowanie i prawo",
        "nav_find_expert": "Znajdz odpowiedniego eksperta",
        "nav_search_now": "Szukaj teraz",
    },
    "cz": {
        "nav_property_types": "Typy nemovitosti",
        "nav_popular_regions": "Popularni regiony",
        "nav_price": "Cena",
        "nav_real_estate": "Nemovitosti",
        "nav_planning_law": "Planovani a pravo",
        "nav_find_expert": "Najdete spravneho experta",
        "nav_search_now": "Hledat",
    },
    "sk": {
        "nav_property_types": "Typy nehnutelnosti",
        "nav_popular_regions": "Popularne regiony",
        "nav_price": "Cena",
        "nav_real_estate": "Nehnutelnosti",
        "nav_planning_law": "Planovanie a pravo",
        "nav_find_expert": "Najdite spravneho experta",
        "nav_search_now": "Hladat",
    },
    "ru": {
        "nav_property_types": "Tipy nedvizhimosti",
        "nav_popular_regions": "Populyarnye regiony",
        "nav_price": "Cena",
        "nav_real_estate": "Nedvizhimost",
        "nav_planning_law": "Planirovanie i pravo",
        "nav_find_expert": "Naydite podkhodyashchego eksperta",
        "nav_search_now": "Iskat",
    },
    "gr": {
        "nav_property_types": "Typoi akineton",
        "nav_popular_regions": "Dimofilis perioches",
        "nav_price": "Timi",
        "nav_real_estate": "Akinita",
        "nav_planning_law": "Schediasmos kai dikaio",
        "nav_find_expert": "Vreite ton swsto eidiko",
        "nav_search_now": "Anazitisi",
    },
    "sw": {
        "nav_property_types": "Fastighetstyper",
        "nav_popular_regions": "Populara regioner",
        "nav_price": "Pris",
        "nav_real_estate": "Fastigheter",
        "nav_planning_law": "Planering och juridik",
        "nav_find_expert": "Hitta ratt expert",
        "nav_search_now": "Sok nu",
    },
    "no": {
        "nav_property_types": "Eiendomstyper",
        "nav_popular_regions": "Populaere regioner",
        "nav_price": "Pris",
        "nav_real_estate": "Eiendom",
        "nav_planning_law": "Planlegging og jus",
        "nav_find_expert": "Finn riktig ekspert",
        "nav_search_now": "Sok na",
    },
}


def get_nav_menu_translations(request):
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in NAV_MENU_TRANSLATIONS else None
    user_language = url_lang or request.session.get("site_language", "ge")
    return NAV_MENU_TRANSLATIONS.get(user_language, NAV_MENU_TRANSLATIONS["ge"])


# =============================================================================
# BREADCRUMB SCHEMA (GEO/SEO)
# =============================================================================

BREADCRUMB_TRANSLATIONS = {
    "ge": {"home": "Startseite", "listings": "Immobilien", "about": "Über uns", "contact": "Kontakt", "faq": "FAQ", "glossary": "Glossar", "news": "News", "professionals": "Experten"},
    "en": {"home": "Home", "listings": "Properties", "about": "About us", "contact": "Contact", "faq": "FAQ", "glossary": "Glossary", "news": "News", "professionals": "Experts"},
    "hr": {"home": "Početna", "listings": "Nekretnine", "about": "O nama", "contact": "Kontakt", "faq": "FAQ", "glossary": "Pojmovnik", "news": "Vijesti", "professionals": "Stručnjaci"},
    "fr": {"home": "Accueil", "listings": "Immobilier", "about": "À propos", "contact": "Contact", "faq": "FAQ", "glossary": "Glossaire", "news": "Actualités", "professionals": "Experts"},
    "nl": {"home": "Home", "listings": "Vastgoed", "about": "Over ons", "contact": "Contact", "faq": "FAQ", "glossary": "Woordenlijst", "news": "Nieuws", "professionals": "Experts"},
    "pl": {"home": "Strona główna", "listings": "Nieruchomości", "about": "O nas", "contact": "Kontakt", "faq": "FAQ", "glossary": "Słownik", "news": "Aktualności", "professionals": "Eksperci"},
    "cz": {"home": "Domů", "listings": "Nemovitosti", "about": "O nás", "contact": "Kontakt", "faq": "FAQ", "glossary": "Slovník", "news": "Novinky", "professionals": "Odborníci"},
    "sk": {"home": "Domov", "listings": "Nehnuteľnosti", "about": "O nás", "contact": "Kontakt", "faq": "FAQ", "glossary": "Slovník", "news": "Novinky", "professionals": "Odborníci"},
    "ru": {"home": "Главная", "listings": "Недвижимость", "about": "О нас", "contact": "Контакт", "faq": "FAQ", "glossary": "Глоссарий", "news": "Новости", "professionals": "Эксперты"},
    "gr": {"home": "Αρχική", "listings": "Ακίνητα", "about": "Σχετικά", "contact": "Επικοινωνία", "faq": "FAQ", "glossary": "Γλωσσάρι", "news": "Νέα", "professionals": "Ειδικοί"},
    "sw": {"home": "Hem", "listings": "Fastigheter", "about": "Om oss", "contact": "Kontakt", "faq": "FAQ", "glossary": "Ordlista", "news": "Nyheter", "professionals": "Experter"},
    "no": {"home": "Hjem", "listings": "Eiendommer", "about": "Om oss", "contact": "Kontakt", "faq": "FAQ", "glossary": "Ordliste", "news": "Nyheter", "professionals": "Eksperter"},
}

COUNTRY_SLUGS = {
    "ge": "kroatien", "en": "croatia", "hr": "hrvatska", "fr": "croatie",
    "nl": "kroatie", "pl": "chorwacja", "cz": "chorvatsko", "sk": "chorvatsko",
    "ru": "horvatiya", "gr": "kroatia", "sw": "kroatien", "no": "kroatia",
}


def get_breadcrumbs(request):
    """Generiert Breadcrumb-Daten für Schema.org und UI"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in BREADCRUMB_TRANSLATIONS else "ge"
    user_language = url_lang or request.session.get("site_language", "ge")
    
    translations = BREADCRUMB_TRANSLATIONS.get(user_language, BREADCRUMB_TRANSLATIONS["ge"])
    country_slug = COUNTRY_SLUGS.get(user_language, "kroatien")
    base_url = "https://123-kroatien.eu"
    
    breadcrumbs = [{"name": translations["home"], "url": f"{base_url}/{user_language}/"}]
    
    # Pfad analysieren und Breadcrumbs aufbauen
    if len(path_parts) > 1:
        section = path_parts[1] if len(path_parts) > 1 else ""
        
        # Mapping von URL-Segmenten zu Breadcrumb-Keys
        section_map = {
            "immobilien": "listings", "properties": "listings", "nekretnine": "listings",
            "about": "about", "contact": "contact", "faq": "faq",
            "glossar": "glossary", "glossary": "glossary", "pojmovnik": "glossary",
            "news": "news", "vijesti": "news", "professionals": "professionals",
            country_slug: None,  # Länder-Slug überspringen
        }
        
        if section in section_map and section_map[section]:
            key = section_map[section]
            breadcrumbs.append({
                "name": translations.get(key, section.title()),
                "url": f"{base_url}/{user_language}/{section}/"
            })
    
    return {
        "breadcrumbs": breadcrumbs,
        "breadcrumbs_json": breadcrumbs,
    }


# =============================================================================
# OPEN GRAPH / SOCIAL MEDIA META TAGS (GEO/SEO)
# =============================================================================

OG_TRANSLATIONS = {
    "ge": {"site_name": "123-Kroatien.eu", "title": "Immobilien in Kroatien", "description": "Der führende Immobilienmarktplatz für Kroatien. Finden Sie Häuser, Wohnungen, Villen und Grundstücke an der Adria."},
    "en": {"site_name": "123-Kroatien.eu", "title": "Real Estate in Croatia", "description": "The leading real estate marketplace for Croatia. Find houses, apartments, villas and land on the Adriatic coast."},
    "hr": {"site_name": "123-Kroatien.eu", "title": "Nekretnine u Hrvatskoj", "description": "Vodeće tržište nekretnina za Hrvatsku. Pronađite kuće, stanove, vile i zemljišta na Jadranskoj obali."},
    "fr": {"site_name": "123-Kroatien.eu", "title": "Immobilier en Croatie", "description": "Le principal marché immobilier pour la Croatie. Trouvez maisons, appartements, villas et terrains sur la côte adriatique."},
    "nl": {"site_name": "123-Kroatien.eu", "title": "Vastgoed in Kroatië", "description": "De toonaangevende vastgoedmarkt voor Kroatië. Vind huizen, appartementen, villa's en grond aan de Adriatische kust."},
    "pl": {"site_name": "123-Kroatien.eu", "title": "Nieruchomości w Chorwacji", "description": "Wiodący rynek nieruchomości w Chorwacji. Znajdź domy, mieszkania, wille i działki na wybrzeżu Adriatyku."},
    "cz": {"site_name": "123-Kroatien.eu", "title": "Nemovitosti v Chorvatsku", "description": "Přední trh s nemovitostmi v Chorvatsku. Najděte domy, byty, vily a pozemky na Jaderském pobřeží."},
    "sk": {"site_name": "123-Kroatien.eu", "title": "Nehnuteľnosti v Chorvátsku", "description": "Popredný trh s nehnuteľnosťami v Chorvátsku. Nájdite domy, byty, vily a pozemky na pobreží Jadranu."},
    "ru": {"site_name": "123-Kroatien.eu", "title": "Недвижимость в Хорватии", "description": "Ведущий рынок недвижимости Хорватии. Найдите дома, квартиры, виллы и участки на Адриатическом побережье."},
    "gr": {"site_name": "123-Kroatien.eu", "title": "Ακίνητα στην Κροατία", "description": "Η κορυφαία αγορά ακινήτων για την Κροατία. Βρείτε σπίτια, διαμερίσματα, βίλες και οικόπεδα στην Αδριατική."},
    "sw": {"site_name": "123-Kroatien.eu", "title": "Fastigheter i Kroatien", "description": "Den ledande fastighetsmarknaden för Kroatien. Hitta hus, lägenheter, villor och tomter vid Adriatiska kusten."},
    "no": {"site_name": "123-Kroatien.eu", "title": "Eiendom i Kroatia", "description": "Det ledende eiendomsmarkedet for Kroatia. Finn hus, leiligheter, villaer og tomter ved Adriaterhavskysten."},
}


def get_og_meta_tags(request):
    """Generiert Open Graph und Twitter Meta Tags für Social Media"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in OG_TRANSLATIONS else "ge"
    user_language = url_lang or request.session.get("site_language", "ge")
    
    translations = OG_TRANSLATIONS.get(user_language, OG_TRANSLATIONS["ge"])
    current_url = f"https://123-kroatien.eu{request.path}"
    
    return {
        "og_title": translations["title"],
        "og_description": translations["description"],
        "og_site_name": translations["site_name"],
        "og_url": current_url,
        "og_image": "https://123-kroatien.eu/static/images/og-image.jpg",
        "twitter_card": "summary_large_image",
    }


# =============================================================================
# PROPERTY DETAIL LABELS (12 Sprachen)
# =============================================================================

PROPERTY_DETAIL_LABELS = {
    "ge": {
        "label_floors": "Etagen",
        "label_garage": "Garage",
        "label_property_type": "Objektart",
        "label_property_status": "Status",
        "label_location": "Lage",
    },
    "en": {
        "label_floors": "Floors",
        "label_garage": "Garage",
        "label_property_type": "Property Type",
        "label_property_status": "Status",
        "label_location": "Location",
    },
    "hr": {
        "label_floors": "Katovi",
        "label_garage": "Garaža",
        "label_property_type": "Vrsta nekretnine",
        "label_property_status": "Status",
        "label_location": "Lokacija",
    },
    "fr": {
        "label_floors": "Étages",
        "label_garage": "Garage",
        "label_property_type": "Type de bien",
        "label_property_status": "Statut",
        "label_location": "Emplacement",
    },
    "nl": {
        "label_floors": "Verdiepingen",
        "label_garage": "Garage",
        "label_property_type": "Type woning",
        "label_property_status": "Status",
        "label_location": "Locatie",
    },
    "pl": {
        "label_floors": "Piętra",
        "label_garage": "Garaż",
        "label_property_type": "Typ nieruchomości",
        "label_property_status": "Status",
        "label_location": "Lokalizacja",
    },
    "cz": {
        "label_floors": "Podlaží",
        "label_garage": "Garáž",
        "label_property_type": "Typ nemovitosti",
        "label_property_status": "Stav",
        "label_location": "Poloha",
    },
    "sk": {
        "label_floors": "Poschodia",
        "label_garage": "Garáž",
        "label_property_type": "Typ nehnuteľnosti",
        "label_property_status": "Stav",
        "label_location": "Poloha",
    },
    "ru": {
        "label_floors": "Этажи",
        "label_garage": "Гараж",
        "label_property_type": "Тип недвижимости",
        "label_property_status": "Статус",
        "label_location": "Расположение",
    },
    "gr": {
        "label_floors": "Όροφοι",
        "label_garage": "Γκαράζ",
        "label_property_type": "Τύπος ακινήτου",
        "label_property_status": "Κατάσταση",
        "label_location": "Τοποθεσία",
    },
    "sw": {
        "label_floors": "Våningar",
        "label_garage": "Garage",
        "label_property_type": "Fastighetstyp",
        "label_property_status": "Status",
        "label_location": "Plats",
    },
    "no": {
        "label_floors": "Etasjer",
        "label_garage": "Garasje",
        "label_property_type": "Eiendomstype",
        "label_property_status": "Status",
        "label_location": "Beliggenhet",
    },
}


def get_property_detail_labels(request):
    """Labels für Property-Detailseite in 12 Sprachen"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in PROPERTY_DETAIL_LABELS else "ge"
    user_language = url_lang or request.session.get("site_language", "ge")
    return PROPERTY_DETAIL_LABELS.get(user_language, PROPERTY_DETAIL_LABELS["ge"])


# =============================================================================
# COUNTRY NAME TRANSLATIONS (für Standort-Anzeige)
# =============================================================================

COUNTRY_NAME_TRANSLATIONS = {
    "ge": "Kroatien",
    "en": "Croatia",
    "hr": "Hrvatska",
    "fr": "Croatie",
    "nl": "Kroatië",
    "pl": "Chorwacja",
    "cz": "Chorvatsko",
    "sk": "Chorvátsko",
    "ru": "Хорватия",
    "gr": "Κροατία",
    "sw": "Kroatien",
    "no": "Kroatia",
}


def get_country_name_translated(request):
    """Übersetzter Ländername für die aktuelle Sprache"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in COUNTRY_NAME_TRANSLATIONS else "ge"
    user_language = url_lang or request.session.get("site_language", "ge")
    return {"country_name_translated": COUNTRY_NAME_TRANSLATIONS.get(user_language, "Kroatien")}


# =============================================================================
# PROPERTY STATUS TRANSLATIONS (Zu Verkaufen / Zu Vermieten)
# =============================================================================

PROPERTY_STATUS_TRANSLATIONS = {
    "ge": {"Sale": "Zu Verkaufen", "Rent": "Zu Vermieten"},
    "en": {"Sale": "For Sale", "Rent": "For Rent"},
    "hr": {"Sale": "Na Prodaju", "Rent": "Za Najam"},
    "fr": {"Sale": "À Vendre", "Rent": "À Louer"},
    "nl": {"Sale": "Te Koop", "Rent": "Te Huur"},
    "pl": {"Sale": "Na Sprzedaż", "Rent": "Do Wynajęcia"},
    "cz": {"Sale": "Na Prodej", "Rent": "K Pronájmu"},
    "sk": {"Sale": "Na Predaj", "Rent": "Na Prenájom"},
    "ru": {"Sale": "Продажа", "Rent": "Аренда"},
    "gr": {"Sale": "Πωλείται", "Rent": "Ενοικιάζεται"},
    "sw": {"Sale": "Till Salu", "Rent": "Att Hyra"},
    "no": {"Sale": "Til Salgs", "Rent": "Til Leie"},
}


def get_property_status_translated(request):
    """Übersetzter Property Status für die aktuelle Sprache"""
    path_parts = request.path.strip("/").split("/")
    url_lang = path_parts[0] if path_parts and path_parts[0] in PROPERTY_STATUS_TRANSLATIONS else "ge"
    user_language = url_lang or request.session.get("site_language", "ge")
    return {"status_translations": PROPERTY_STATUS_TRANSLATIONS.get(user_language, PROPERTY_STATUS_TRANSLATIONS["ge"])}
