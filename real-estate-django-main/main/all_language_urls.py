# main/all_language_urls.py
"""
Generiert mehrsprachige URLs für alle 12 Sprachen.

WICHTIG: Die generischen <str:category>/ URLs müssen NACH dem Glossar
eingebunden werden, da sie sonst das Glossar überlagern!

Verwendung in main/urls.py:
```
from .all_language_urls import specific_language_urlpatterns, generic_category_urlpatterns

urlpatterns = [
    # ... statische URLs ...
] + glossary_urlpatterns + specific_language_urlpatterns + generic_category_urlpatterns
```
"""

from django.urls import path
from . import views
from . import professional_views
from .glossary_models import COUNTRY_NAMES

# ============================================
# URL-SEGMENT ÜBERSETZUNGEN
# ============================================

EXPERT_FINDER_URLS = {
    "ge": "experten-finder", "en": "expert-finder", "hr": "pronalazac-strucnjaka",
    "fr": "recherche-experts", "nl": "expert-zoeker", "pl": "wyszukiwarka-ekspertow",
    "cz": "vyhledavac-odborniku", "sk": "vyhladavac-odbornikov", "ru": "poisk-ekspertov",
    "gr": "anazhthsh-eidikwn", "sw": "expert-sokare", "no": "ekspert-soker",
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


def get_specific_language_urlpatterns():
    """
    Generiert SPEZIFISCHE URL-Patterns für alle Sprachen.
    Diese müssen VOR den generischen <str:category>/ URLs stehen.
    """
    patterns = []
    
    # Prüfe ob matching_views existiert (für Experten-Finder)
    try:
        from . import matching_views
        has_matching = True
    except ImportError:
        has_matching = False
    
    for lang_code, country_slug in COUNTRY_NAMES.items():
        
        # ========================================
        # EXPERTEN-FINDER (wenn vorhanden)
        # ========================================
        if has_matching:
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
    
    return patterns


def get_generic_category_urlpatterns():
    """
    Generiert GENERISCHE <str:category>/ URL-Patterns für alle Sprachen.
    Diese MÜSSEN ZULETZT stehen, da sie alles matchen!
    """
    patterns = []
    
    for lang_code, country_slug in COUNTRY_NAMES.items():
        # Diese URLs fangen alle /{lang}/{country}/{irgendwas}/ ab
        # Sie müssen NACH spezifischen URLs (Glossar, Experten-Finder, etc.) stehen
        patterns.append(path(
            f"{lang_code}/{country_slug}/<str:category>/",
            professional_views.professional_list,
            {"country": country_slug},
            name=f"professional-list-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/<str:category>/<str:slug>/",
            professional_views.professional_detail,
            {"country": country_slug},
            name=f"professional-detail-{lang_code}",
        ))
    
    return patterns


# URL-Patterns für Import
specific_language_urlpatterns = get_specific_language_urlpatterns()
generic_category_urlpatterns = get_generic_category_urlpatterns()

# Für Abwärtskompatibilität (falls jemand all_language_urlpatterns importiert)
# ACHTUNG: Diese Reihenfolge ist FALSCH wenn Glossar dazwischen soll!
all_language_urlpatterns = specific_language_urlpatterns + generic_category_urlpatterns
