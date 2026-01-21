from django.utils.translation import activate
from pages.models import Translation

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

    return context