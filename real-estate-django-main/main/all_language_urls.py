# main/all_language_urls.py
"""
Generiert ALLE mehrsprachigen URLs für alle 12 Sprachen.

Dieses Modul konsolidiert:
- News URLs
- Adressen URLs  
- Marktberichte URLs
- Dienstleister URLs (Professional)
- Experten-Finder URLs
- Rechtliche Seiten (AGB, Widerruf, etc.)

Alle URLs werden dynamisch für alle 12 Sprachen generiert.
"""

from django.urls import path
from . import views
from . import content_views
from . import address_views
from . import professional_views
from . import matching_views
from . import glossary_views
from .glossary_models import COUNTRY_NAMES

# ============================================
# URL-SEGMENT ÜBERSETZUNGEN
# ============================================

NEWS_URLS = {
    "ge": "nachrichten", "en": "news", "hr": "vijesti", "fr": "actualites",
    "nl": "nieuws", "pl": "wiadomosci", "cz": "zpravy", "sk": "spravy",
    "ru": "novosti", "gr": "nea", "sw": "nyheter", "no": "nyheter",
}

ADDRESS_URLS = {
    "ge": "wichtige-adressen", "en": "important-addresses", "hr": "vazne-adrese",
    "fr": "adresses-importantes", "nl": "belangrijke-adressen", "pl": "wazne-adresy",
    "cz": "dulezite-adresy", "sk": "dolezite-adresy", "ru": "vazhnye-adresa",
    "gr": "simantikes-dieythynseis", "sw": "viktiga-adresser", "no": "viktige-adresser",
}

MARKET_URLS = {
    "ge": "marktberichte", "en": "market-reports", "hr": "trzisni-izvjestaji",
    "fr": "rapports-marche", "nl": "marktverslagen", "pl": "raporty-rynkowe",
    "cz": "trzni-zpravy", "sk": "trhove-spravy", "ru": "rynochnye-otchety",
    "gr": "anafores-agoras", "sw": "marknadsrapporter", "no": "markedsrapporter",
}

EXPERT_FINDER_URLS = {
    "ge": "experten-finder", "en": "expert-finder", "hr": "pronalazac-strucnjaka",
    "fr": "recherche-experts", "nl": "expert-zoeker", "pl": "wyszukiwarka-ekspertow",
    "cz": "vyhledavac-odborniku", "sk": "vyhladavac-odbornikov", "ru": "poisk-ekspertov",
    "gr": "anazhthsh-eidikwn", "sw": "expert-sokare", "no": "ekspert-soker",
}

# Dienstleister-Kategorien
REALTOR_URLS = {
    "ge": "immobilienmakler", "en": "real-estate-agents", "hr": "agencije-za-nekretnine",
    "fr": "agents-immobiliers", "nl": "makelaars", "pl": "agenci-nieruchomosci",
    "cz": "realitni-makleri", "sk": "realitni-makleri", "ru": "agenty-nedvizhimosti",
    "gr": "mesites-akiniton", "sw": "fastighetsmaklare", "no": "eiendomsmeglere",
}

CONTRACTOR_URLS = {
    "ge": "bauunternehmen", "en": "construction-companies", "hr": "gradevinske-tvrtke",
    "fr": "entreprises-construction", "nl": "bouwbedrijven", "pl": "firmy-budowlane",
    "cz": "stavebni-firmy", "sk": "stavebne-firmy", "ru": "stroitelnye-kompanii",
    "gr": "kataskevestikes-etaireies", "sw": "byggforetag", "no": "byggefirmaer",
}

LAWYER_URLS = {
    "ge": "rechtsanwaelte", "en": "lawyers", "hr": "odvjetnici",
    "fr": "avocats", "nl": "advocaten", "pl": "prawnicy",
    "cz": "pravnici", "sk": "pravnici", "ru": "advokaty",
    "gr": "dikigoroi", "sw": "advokater", "no": "advokater",
}

TAX_ADVISOR_URLS = {
    "ge": "steuerberater", "en": "tax-advisors", "hr": "porezni-savjetnici",
    "fr": "conseillers-fiscaux", "nl": "belastingadviseurs", "pl": "doradcy-podatkowi",
    "cz": "danovi-poradci", "sk": "danovi-poradcovia", "ru": "nalogovye-konsultanty",
    "gr": "forologikoi-symvouloi", "sw": "skatteradgivare", "no": "skatteradgivere",
}

ARCHITECT_URLS = {
    "ge": "architekten", "en": "architects", "hr": "arhitekti",
    "fr": "architectes", "nl": "architecten", "pl": "architekci",
    "cz": "architekti", "sk": "architekti", "ru": "arhitektory",
    "gr": "architektons", "sw": "arkitekter", "no": "arkitekter",
}

PARTNER_URLS = {
    "ge": "partner-werden", "en": "become-partner", "hr": "postanite-partner",
    "fr": "devenir-partenaire", "nl": "partner-worden", "pl": "zostan-partnerem",
    "cz": "stanat-se-partnerem", "sk": "stat-sa-partnerom", "ru": "stat-partnerom",
    "gr": "gineite-synergatis", "sw": "bli-partner", "no": "bli-partner",
}

REGISTRATION_URLS = {
    "ge": "registrierung", "en": "registration", "hr": "registracija",
    "fr": "inscription", "nl": "registratie", "pl": "rejestracja",
    "cz": "registrace", "sk": "registracia", "ru": "registratsiya",
    "gr": "eggraphi", "sw": "registrering", "no": "registrering",
}


def get_all_language_urlpatterns():
    """
    Generiert URL-Patterns für alle Sprachen dynamisch.
    """
    patterns = []
    
    for lang_code, country_slug in COUNTRY_NAMES.items():
        
        # ========================================
        # NEWS
        # ========================================
        news_segment = NEWS_URLS.get(lang_code, "nachrichten")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{news_segment}/",
            views.news_page,
            {"lang": lang_code, "country": country_slug},
            name=f"news-{lang_code}",
        ))
        
        # ========================================
        # WICHTIGE ADRESSEN
        # ========================================
        address_segment = ADDRESS_URLS.get(lang_code, "wichtige-adressen")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{address_segment}/",
            address_views.important_addresses,
            {"country": country_slug},
            name=f"important-addresses-{lang_code}",
        ))
        
        # ========================================
        # MARKTBERICHTE
        # ========================================
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
        
        # ========================================
        # EXPERTEN-FINDER
        # ========================================
        expert_segment = EXPERT_FINDER_URLS.get(lang_code, "experten-finder")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{expert_segment}/",
            matching_views.matching_page,
            {"lang": lang_code},
            name=f"experten-finder-{lang_code}",
        ))
        
        # ========================================
        # PARTNER WERDEN
        # ========================================
        partner_segment = PARTNER_URLS.get(lang_code, "partner-werden")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{partner_segment}/",
            views.partner_landing,
            {"lang": lang_code},
            name=f"partner-landing-{lang_code}",
        ))
        
        # ========================================
        # REGISTRIERUNG
        # ========================================
        reg_segment = REGISTRATION_URLS.get(lang_code, "registrierung")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{reg_segment}/",
            professional_views.professional_registration,
            {"country": country_slug},
            name=f"professional-reg-{lang_code}",
        ))
        
        # ========================================
        # DIENSTLEISTER (nur DE, EN, HR haben Daten)
        # Aber URLs müssen für alle Sprachen funktionieren
        # ========================================
        
        # Immobilienmakler
        realtor_segment = REALTOR_URLS.get(lang_code, "immobilienmakler")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{realtor_segment}/",
            professional_views.professional_list,
            {"country": country_slug, "category_override": "immobilienmakler"},
            name=f"realtor-list-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{realtor_segment}/<str:slug>/",
            professional_views.professional_detail,
            {"country": country_slug, "category_override": "immobilienmakler"},
            name=f"realtor-detail-{lang_code}",
        ))
        
        # Bauunternehmen
        contractor_segment = CONTRACTOR_URLS.get(lang_code, "bauunternehmen")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{contractor_segment}/",
            professional_views.professional_list,
            {"country": country_slug, "category_override": "bauunternehmen"},
            name=f"contractor-list-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{contractor_segment}/<str:slug>/",
            professional_views.professional_detail,
            {"country": country_slug, "category_override": "bauunternehmen"},
            name=f"contractor-detail-{lang_code}",
        ))
        
        # Rechtsanwälte
        lawyer_segment = LAWYER_URLS.get(lang_code, "rechtsanwaelte")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{lawyer_segment}/",
            professional_views.professional_list,
            {"country": country_slug, "category_override": "rechtsanwaelte"},
            name=f"lawyer-list-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{lawyer_segment}/<str:slug>/",
            professional_views.professional_detail,
            {"country": country_slug, "category_override": "rechtsanwaelte"},
            name=f"lawyer-detail-{lang_code}",
        ))
        
        # Steuerberater
        tax_segment = TAX_ADVISOR_URLS.get(lang_code, "steuerberater")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{tax_segment}/",
            professional_views.professional_list,
            {"country": country_slug, "category_override": "steuerberater"},
            name=f"tax-advisor-list-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{tax_segment}/<str:slug>/",
            professional_views.professional_detail,
            {"country": country_slug, "category_override": "steuerberater"},
            name=f"tax-advisor-detail-{lang_code}",
        ))
        
        # Architekten
        architect_segment = ARCHITECT_URLS.get(lang_code, "architekten")
        patterns.append(path(
            f"{lang_code}/{country_slug}/{architect_segment}/",
            professional_views.professional_list,
            {"country": country_slug, "category_override": "architekten"},
            name=f"architect-list-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{architect_segment}/<str:slug>/",
            professional_views.professional_detail,
            {"country": country_slug, "category_override": "architekten"},
            name=f"architect-detail-{lang_code}",
        ))
    
    return patterns


# URL-Patterns für Import
all_language_urlpatterns = get_all_language_urlpatterns()
