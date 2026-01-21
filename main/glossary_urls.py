# main/glossary_urls.py
from django.urls import path
from . import glossary_views
from .glossary_models import COUNTRY_NAMES, GLOSSARY_URLS


def get_glossary_urlpatterns():
    patterns = []
    for lang_code, country_slug in COUNTRY_NAMES.items():
        glossary_segment = GLOSSARY_URLS.get(lang_code, "glossar")
        
        patterns.append(path(
            f"{lang_code}/{country_slug}/{glossary_segment}/",
            glossary_views.glossary_index,
            {"lang": lang_code, "country": country_slug},
            name=f"glossary-index-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{glossary_segment}/investors/",
            glossary_views.landing_investors,
            {"lang": lang_code, "country": country_slug},
            name=f"glossary-landing-investors-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{glossary_segment}/holiday-properties/",
            glossary_views.landing_holiday,
            {"lang": lang_code, "country": country_slug},
            name=f"glossary-landing-holiday-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{glossary_segment}/luxury-real-estate/",
            glossary_views.landing_luxury,
            {"lang": lang_code, "country": country_slug},
            name=f"glossary-landing-luxury-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{glossary_segment}/disclaimer/",
            glossary_views.disclaimer_page,
            {"lang": lang_code, "country": country_slug},
            name=f"glossary-disclaimer-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{glossary_segment}/buyer-guide/",
            glossary_views.buyer_guide_page,
            {"lang": lang_code, "country": country_slug},
            name=f"glossary-buyer-guide-{lang_code}",
        ))
        patterns.append(path(
            f"{lang_code}/{country_slug}/{glossary_segment}/<str:slug>/",
            glossary_views.glossary_detail,
            {"lang": lang_code, "country": country_slug},
            name=f"glossary-detail-{lang_code}",
        ))
    return patterns


glossary_urlpatterns = get_glossary_urlpatterns()