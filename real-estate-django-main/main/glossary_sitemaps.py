# main/glossary_sitemaps.py
"""
Sitemap-Generierung für Glossar
- Eine Sitemap pro Sprache
- Nur veröffentlichte Begriffe
- lastmod aus updated_at
"""

from django.contrib.sitemaps import Sitemap
from .glossary_models import (
    GlossaryTermTranslation,
    GLOSSARY_URLS,
    COUNTRY_NAMES,
    LANG_CHOICES,
)


class GlossaryTermSitemap(Sitemap):
    """
    Sitemap für Glossar-Begriffe.
    
    Generiert URLs für alle veröffentlichten Begriffe
    in der angegebenen Sprache.
    """
    changefreq = "weekly"
    priority = 0.7
    protocol = "https"
    
    def __init__(self, language="ge"):
        self.language = language
        super().__init__()
    
    def items(self):
        """Gibt alle veröffentlichten Übersetzungen für diese Sprache zurück."""
        return (GlossaryTermTranslation.objects
                .filter(
                    language=self.language,
                    term__is_published=True,
                    status__in=["approved", "published"]
                )
                .select_related("term")
                .order_by("title"))
    
    def lastmod(self, obj):
        """Letztes Änderungsdatum."""
        return obj.updated_at
    
    def location(self, obj):
        """URL für den Begriff."""
        return obj.get_absolute_url()


class GlossaryIndexSitemap(Sitemap):
    """
    Sitemap für Glossar-Indexseiten.
    
    Eine URL pro Sprache für die Glossar-Übersichtsseite.
    """
    changefreq = "daily"
    priority = 0.8
    protocol = "https"
    
    def __init__(self, language="ge"):
        self.language = language
        super().__init__()
    
    def items(self):
        """Gibt eine Liste mit einem Element zurück (Index-Seite)."""
        return [self.language]
    
    def location(self, item):
        """URL für die Index-Seite."""
        country = COUNTRY_NAMES.get(item, "kroatien")
        glossary_segment = GLOSSARY_URLS.get(item, "glossar")
        return f"/{item}/{country}/{glossary_segment}/"


class GlossaryLandingSitemap(Sitemap):
    """
    Sitemap für Glossar-Landingpages.
    
    URLs für Investoren, Ferien, Luxus pro Sprache.
    """
    changefreq = "weekly"
    priority = 0.6
    protocol = "https"
    
    def __init__(self, language="ge"):
        self.language = language
        super().__init__()
    
    def items(self):
        """Landing Page Slugs."""
        return ["investors", "holiday-properties", "luxury-real-estate"]
    
    def location(self, item):
        """URL für die Landing Page."""
        country = COUNTRY_NAMES.get(self.language, "kroatien")
        glossary_segment = GLOSSARY_URLS.get(self.language, "glossar")
        return f"/{self.language}/{country}/{glossary_segment}/{item}/"


def get_glossary_sitemaps():
    """
    Generiert Sitemap-Dictionary für alle Sprachen.
    
    Verwendung in urls.py:
    
    from main.glossary_sitemaps import get_glossary_sitemaps
    
    sitemaps = {
        **get_glossary_sitemaps(),
        # ... andere Sitemaps
    }
    
    urlpatterns = [
        path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    ]
    """
    sitemaps = {}
    
    for lang_code, _ in LANG_CHOICES:
        # Term-Sitemaps
        sitemaps[f"glossary-terms-{lang_code}"] = GlossaryTermSitemap(language=lang_code)
        
        # Index-Sitemaps
        sitemaps[f"glossary-index-{lang_code}"] = GlossaryIndexSitemap(language=lang_code)
        
        # Landing-Sitemaps
        sitemaps[f"glossary-landing-{lang_code}"] = GlossaryLandingSitemap(language=lang_code)
    
    return sitemaps
