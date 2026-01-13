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

# Makler-Portal (ohne Sprachpraefix)
from main.professional_totp import (
    professional_login, professional_setup_2fa,
    professional_verify_2fa_setup, professional_verify_2fa_login
)

urlpatterns += [
    path('makler-portal/login/', professional_login, name='professional_login'),
    path('makler-portal/2fa-einrichten/', professional_setup_2fa, name='professional_setup_2fa'),
    path('makler-portal/2fa-verifizieren/', professional_verify_2fa_setup, name='professional_verify_2fa_setup'),
    path('makler-portal/2fa-login/', professional_verify_2fa_login, name='professional_verify_2fa'),
    path('ge/makler-portal/2fa-einrichten/', professional_setup_2fa, name='professional_setup_2fa_ge'),
    path('ge/makler-portal/2fa-verifizieren/', professional_verify_2fa_setup, name='professional_verify_2fa_setup_ge'),
    path('ge/makler-portal/2fa-login/', professional_verify_2fa_login, name='professional_verify_2fa_ge'),

]

urlpatterns += i18n_patterns(
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),
    prefix_default_language=True,
)
