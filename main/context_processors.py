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
    translations = Translation.objects.filter(page=page) | Translation.objects.filter(page='navbar') | Translation.objects.filter(page='footer') | Translation.objects.filter(page='listings') | Translation.objects.filter(page='property details') | Translation.objects.filter(page='home') | Translation.objects.filter(page='contact') | Translation.objects.filter(page='chatbot')
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
    
    # News Label
    news_labels = {
        'ge': 'Nachrichten', 'en': 'News', 'hr': 'Vijesti', 'fr': 'Actualités',
        'nl': 'Nieuws', 'pl': 'Wiadomości', 'cz': 'Zprávy', 'sk': 'Správy',
        'ru': 'Новости', 'gr': 'Νέα', 'sw': 'Nyheter', 'no': 'Nyheter',
    }
    context['news_label'] = news_labels.get(user_language, 'Nachrichten')

    # Partner Section Labels
    partner_labels = {
        'ge': 'Unsere Partner', 'en': 'Our Partners', 'hr': 'Naši partneri',
        'fr': 'Nos partenaires', 'nl': 'Onze partners', 'pl': 'Nasi partnerzy',
        'cz': 'Naši partneři', 'sk': 'Naši partneri', 'ru': 'Наши партнеры',
        'gr': 'Οι συνεργάτες μας', 'sw': 'Våra partners', 'no': 'Våre partnere',
    }
    context['our_partners'] = partner_labels.get(user_language, 'Unsere Partner')
    
    partner_subtitle = {
        'ge': 'Verifizierte Partner aus Kroatien', 'en': 'Verified partners from Croatia',
        'hr': 'Verificirani partneri iz Hrvatske', 'fr': 'Partenaires vérifiés de Croatie',
        'nl': 'Geverifieerde partners uit Kroatië', 'pl': 'Zweryfikowani partnerzy z Chorwacji',
        'cz': 'Ověření partneři z Chorvatska', 'sk': 'Overení partneri z Chorvátska',
        'ru': 'Проверенные партнеры из Хорватии', 'gr': 'Επαληθευμένοι συνεργάτες από την Κροατία',
        'sw': 'Verifierade partners från Kroatien', 'no': 'Verifiserte partnere fra Kroatia',
    }
    context['partner_subtitle'] = partner_subtitle.get(user_language, 'Verifizierte Partner aus Kroatien')

    # Hero Section - Tagline
    hero_tagline = {
        'ge': 'KROATIEN - ADRIA - MITTELMEER', 'en': 'CROATIA - ADRIATIC - MEDITERRANEAN',
        'hr': 'HRVATSKA - JADRAN - MEDITERAN', 'fr': 'CROATIE - ADRIATIQUE - MÉDITERRANÉE',
        'nl': 'KROATIË - ADRIATISCHE ZEE - MIDDELLANDSE ZEE', 'pl': 'CHORWACJA - ADRIATYK - MORZE ŚRÓDZIEMNE',
        'cz': 'CHORVATSKO - JADRAN - STŘEDOMOŘÍ', 'sk': 'CHORVÁTSKO - JADRAN - STREDOMORIE',
        'ru': 'ХОРВАТИЯ - АДРИАТИКА - СРЕДИЗЕМНОМОРЬЕ', 'gr': 'ΚΡΟΑΤΊΑ - ΑΔΡΙΑΤΙΚΉ - ΜΕΣΌΓΕΙΟΣ',
        'sw': 'KROATIEN - ADRIATISKA HAVET - MEDELHAVET', 'no': 'KROATIA - ADRIATERHAVET - MIDDELHAVET',
    }
    context['hero_tagline'] = hero_tagline.get(user_language, 'KROATIEN - ADRIA - MITTELMEER')

    # Hero Section - Title
    hero_title = {
        'ge': 'Exklusive Immobilien<br>an der kroatischen Küste', 'en': 'Exclusive Properties<br>on the Croatian Coast',
        'hr': 'Ekskluzivne nekretnine<br>na hrvatskoj obali', 'fr': 'Propriétés exclusives<br>sur la côte croate',
        'nl': 'Exclusief vastgoed<br>aan de Kroatische kust', 'pl': 'Ekskluzywne nieruchomości<br>na chorwackim wybrzeżu',
        'cz': 'Exkluzivní nemovitosti<br>na chorvatském pobřeží', 'sk': 'Exkluzívne nehnuteľnosti<br>na chorvátskom pobreží',
        'ru': 'Эксклюзивная недвижимость<br>на хорватском побережье', 'gr': 'Αποκλειστικά ακίνητα<br>στην κροατική ακτή',
        'sw': 'Exklusiva fastigheter<br>vid den kroatiska kusten', 'no': 'Eksklusive eiendommer<br>ved den kroatiske kysten',
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
    # Sortiere nach Länge (längste zuerst) damit 'glossary' vor 'glossar' matched
    sorted_glossary_slugs = sorted(GLOSSARY_URLS.values(), key=len, reverse=True)
    glossary_pattern = re.compile(
        r'^/([a-z]{2})/([^/]+)/(' + '|'.join(sorted_glossary_slugs) + r')/?(.*)$'
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
        # Sitemap hat keine Sprachpräfixe - bleibt immer gleich
        for lang in ALL_LANGUAGES:
            urls[lang] = '/sitemap/'
    
    else:
        # Statische Seiten oder unbekannte Pfade
        # Fallback: Sprache in Session setzen, aber auf gleicher Seite bleiben
        # (für Seiten ohne übersetzte URLs wie /contact/, /about/, etc.)
        for lang in ALL_LANGUAGES:
            urls[lang] = current_path if current_path else '/'
    
    return json.dumps(urls)