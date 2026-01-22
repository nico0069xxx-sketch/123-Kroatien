from django.contrib.sitemaps import Sitemap
from .glossary_models import GlossaryTermTranslation, GLOSSARY_URLS, COUNTRY_NAMES, LANG_CHOICES


class GlossaryTermSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7
    protocol = "https"
    
    def __init__(self, language="ge"):
        self.language = language
        super().__init__()
    
    def items(self):
        return (GlossaryTermTranslation.objects
                .filter(language=self.language, term__is_published=True, status__in=["approved", "published"])
                .select_related("term")
                .order_by("title"))
    
    def lastmod(self, obj):
        return obj.updated_at
    
    def location(self, obj):
        return obj.get_absolute_url()


class GlossaryIndexSitemap(Sitemap):
    changefreq = "daily"
    priority = 0.8
    protocol = "https"
    
    def __init__(self, language="ge"):
        self.language = language
        super().__init__()
    
    def items(self):
        return [self.language]
    
    def location(self, item):
        country = COUNTRY_NAMES.get(item, "kroatien")
        glossary_segment = GLOSSARY_URLS.get(item, "glossar")
        return f"/{item}/{country}/{glossary_segment}/"


def get_glossary_sitemaps():
    sitemaps = {}
    for lang_code, _ in LANG_CHOICES:
        sitemaps[f"glossary-terms-{lang_code}"] = GlossaryTermSitemap(language=lang_code)
        sitemaps[f"glossary-index-{lang_code}"] = GlossaryIndexSitemap(language=lang_code)
    return sitemaps
