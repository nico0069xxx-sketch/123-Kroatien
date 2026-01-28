from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from main.views import set_language_from_url
from main.xml_views import rss_listings, xml_sitemap, robots_txt, llms_txt

# Alle unterstützten Sprachen
SUPPORTED_LANGUAGES = ['en', 'ge', 'fr', 'gr', 'hr', 'pl', 'cz', 'ru', 'sw', 'no', 'sk', 'nl']

# URLs ohne Sprachpräfix (Admin, API, technische Routen)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("set-language/<str:user_language>/", set_language_from_url, name="set_language_from_url"),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls')),
    
    # XML/RSS Feeds & AI Crawler Files (ohne Sprachpräfix)
    path('rss/listings/', rss_listings, name='rss_listings'),
    path('sitemap.xml', xml_sitemap, name='xml_sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('llms.txt', llms_txt, name='llms_txt'),
    
    # Professional Portal
    path('portal/', include('main.professional_portal_urls')),
    
    # Haupt-App URLs (ohne Präfix = Default Sprache Deutsch)
    path('', include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs MIT Sprachpräfix für alle 12 Sprachen (/en/, /hr/, /fr/, etc.)
# Jede Sprache bekommt ihre eigenen URL-Patterns
for lang in SUPPORTED_LANGUAGES:
    urlpatterns.append(
        path(f'{lang}/', include('main.urls'))
    )

