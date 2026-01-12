from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from main.views import set_language_from_url, xml_sitemap, robots_txt, rss_listings

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("set-language/<str:user_language>/", set_language_from_url, name="set_language_from_url"),
        # SEO (öffentlich zugänglich)
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', xml_sitemap, name='xml_sitemap'),
    path('rss/listings/', rss_listings, {'lang': 'ge'}, name='rss_listings'),
    path('en/rss/listings/', rss_listings, {'lang': 'en'}, name='rss_en'),
    path('hr/rss/listings/', rss_listings, {'lang': 'hr'}, name='rss_hr'),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('realstate.chatbot_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),
    prefix_default_language=True,
)
