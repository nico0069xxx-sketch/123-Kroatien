from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from main.views import set_language_from_url
from main.xml_views import rss_listings, xml_sitemap, robots_txt

# URLs ohne Sprachpräfix (Admin, API, technische Routen)
urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("set-language/<str:user_language>/", set_language_from_url, name="set_language_from_url"),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('accounts/', include('accounts.urls')),
    
    # XML/RSS Feeds (ohne Sprachpräfix)
    path('rss/listings/', rss_listings, name='rss_listings'),
    path('sitemap.xml', xml_sitemap, name='xml_sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
    
    # Professional Portal
    path('portal/', include('main.professional_portal_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# URLs MIT Sprachpräfix (/en/, /de/, /hr/, etc.)
urlpatterns += i18n_patterns(
    path('', include('main.urls')),
    prefix_default_language=False,  # /about/ für Deutsch (default), /en/about/ für English
)

