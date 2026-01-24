# main/content_urls.py
from django.urls import path
from . import views
from . import content_views
from . import address_views
from .glossary_models import COUNTRY_NAMES

# URL-Pfade für News in allen Sprachen
NEWS_URLS = {
    "ge": "nachrichten",
    "en": "news",
    "hr": "vijesti",
    "fr": "actualites",
    "nl": "nieuws",
    "pl": "wiadomosci",
    "cz": "zpravy",
    "sk": "spravy",
    "ru": "novosti",
    "gr": "nea",
    "sw": "nyheter",
    "no": "nyheter",
}

# URL-Pfade für Wichtige Adressen in allen Sprachen
ADDRESS_URLS = {
    "ge": "wichtige-adressen",
    "en": "important-addresses",
    "hr": "vazne-adrese",
    "fr": "adresses-importantes",
    "nl": "belangrijke-adressen",
    "pl": "wazne-adresy",
    "cz": "dulezite-adresy",
    "sk": "dolezite-adresy",
    "ru": "vazhnye-adresa",
    "gr": "simantikes-dieythynseis",
    "sw": "viktiga-adresser",
    "no": "viktige-adresser",
}

# URL-Pfade für Marktberichte in allen Sprachen
MARKET_URLS = {
    "ge": "marktberichte",
    "en": "market-reports",
    "hr": "trzisni-izvjestaji",
    "fr": "rapports-marche",
    "nl": "marktverslagen",
    "pl": "raporty-rynkowe",
    "cz": "trzni-zpravy",
    "sk": "trhove-spravy",
    "ru": "rynochnye-otchety",
    "gr": "anafores-agoras",
    "sw": "marknadsrapporter",
    "no": "markedsrapporter",
}


def get_content_urlpatterns():
    patterns = []
    
    for lang_code, country_slug in COUNTRY_NAMES.items():
        # News URLs
        news_segment = NEWS_URLS.get(lang_code, "nachrichten")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{news_segment}/",
            views.news_page,
            {"lang": lang_code, "country": country_slug},
            name=f"news-{lang_code}",
        ))
        
        # Wichtige Adressen URLs
        address_segment = ADDRESS_URLS.get(lang_code, "wichtige-adressen")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{address_segment}/",
            address_views.important_addresses,
            {"country": country_slug},
            name=f"important-addresses-{lang_code}",
        ))
        
        # Marktberichte URLs
        market_segment = MARKET_URLS.get(lang_code, "marktberichte")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{market_segment}/",
            content_views.market_report_list,
            {"country": country_slug},
            name=f"market-reports-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{market_segment}/<str:region_slug>/<int:year>/",
            content_views.market_report_detail,
            {"country": country_slug},
            name=f"market-report-detail-{lang_code}",
        ))
    
    return patterns


content_urlpatterns = get_content_urlpatterns()