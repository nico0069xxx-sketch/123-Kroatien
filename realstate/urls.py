from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from main.views import set_language_from_url, news_page, sitemap as html_sitemap
from main.xml_views import rss_listings, xml_sitemap, robots_txt, xml_sitemap, robots_txt, rss_listings
from django.contrib.sitemaps.views import sitemap
from main.glossary_sitemaps import get_glossary_sitemaps

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("set-language/<str:user_language>/", set_language_from_url, name="set_language_from_url"),
        # SEO (öffentlich zugänglich)
    path('robots.txt', robots_txt, name='robots_txt'),
    path('sitemap.xml', xml_sitemap, name='xml_sitemap'),
    path('sitemaps/glossary.xml', sitemap, {'sitemaps': get_glossary_sitemaps()},    	name='glossary-sitemap'),
    path('sitemap', html_sitemap, name='sitemap-html'),
    path('ge/sitemap', html_sitemap, name='sitemap-ge'),
    path('en/sitemap', html_sitemap, name='sitemap-en'),
    path('hr/sitemap', html_sitemap, name='sitemap-hr'),
    path('fr/sitemap', html_sitemap, name='sitemap-fr'),
    path('nl/sitemap', html_sitemap, name='sitemap-nl'),
    path('pl/sitemap', html_sitemap, name='sitemap-pl'),
    path('cz/sitemap', html_sitemap, name='sitemap-cz'),
    path('sk/sitemap', html_sitemap, name='sitemap-sk'),
    path('ru/sitemap', html_sitemap, name='sitemap-ru'),
    path('gr/sitemap', html_sitemap, name='sitemap-gr'),
    path('sw/sitemap', html_sitemap, name='sitemap-sw'),
    path('no/sitemap', html_sitemap, name='sitemap-no'),
    path('rss/listings/', rss_listings, {'lang': 'ge'}, name='rss_listings'),
    path('en/rss/listings/', rss_listings, {'lang': 'en'}, name='rss_en'),
    path('hr/rss/listings/', rss_listings, {'lang': 'hr'}, name='rss_hr'),
    path('nik-verwaltung-2026/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('realstate.chatbot_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Makler-Portal (ohne Sprachpraefix)
from main.email_2fa import email_2fa_send, email_2fa_verify, email_2fa_resend, choose_2fa_method, choose_email_2fa
from main.professional_totp import (
    professional_login, professional_setup_2fa,
    professional_verify_2fa_setup, professional_verify_2fa_login
)

urlpatterns += [
    path('makler-portal/login/', professional_login, name='professional_login'),
    path('makler-portal/2fa-einrichten/', professional_setup_2fa, name='professional_setup_2fa'),
    path('makler-portal/2fa-verifizieren/', professional_verify_2fa_setup, name='professional_verify_2fa_setup'),
        path('makler-portal/email-code/', email_2fa_send, name='email_2fa_send'),
    path('makler-portal/email-code/verify/', email_2fa_verify, name='email_2fa_verify'),
    path('makler-portal/email-code/resend/', email_2fa_resend, name='email_2fa_resend'),
    path('makler-portal/2fa-auswahl/', choose_2fa_method, name='choose_2fa_method'),
    path('makler-portal/2fa-email-waehlen/', choose_email_2fa, name='choose_email_2fa'),
    path('makler-portal/2fa-login/', professional_verify_2fa_login, name='professional_verify_2fa'),
    path('ge/makler-portal/2fa-einrichten/', professional_setup_2fa, name='professional_setup_2fa_ge'),
    path('ge/makler-portal/2fa-verifizieren/', professional_verify_2fa_setup, name='professional_verify_2fa_setup_ge'),
    path('ge/makler-portal/2fa-login/', professional_verify_2fa_login, name='professional_verify_2fa_ge'),

]

# Professional Detail URLs (ohne i18n prefix)
from main import professional_views, views
from main import address_views, content_views
from main import glossary_views
from main.glossary_urls import glossary_urlpatterns
urlpatterns += [
    # MARKT - muss VOR Professional URLs stehen
    path("ge/kroatien/marktberichte/", content_views.market_report_list, {"country": "kroatien"}, name="market-reports-ge-direct"),
    path("ge/kroatien/nachrichten/", news_page, {"country": "kroatien", "lang": "ge"}, name="news-ge-direct"),
    path("hr/hrvatska/vijesti/", news_page, {"country": "hrvatska", "lang": "hr"}, name="news-hr-direct"),
    path("ge/kroatien/wichtige-adressen/", address_views.important_addresses, {"country": "kroatien"}, name="important-addresses-ge-direct"),
    path("hr/hrvatska/trzisni-izvjestaji/", content_views.market_report_list, {"country": "hrvatska"}, name="market-reports-hr-direct"),
    path("hr/hrvatska/vazne-adrese/", address_views.important_addresses, {"country": "hrvatska"}, name="important-addresses-hr-direct"),
    
    path("ge/kroatien/partner-werden/", views.partner_landing, {"lang": "ge"}, name="partner-landing-ge-direct"),
    path("hr/hrvatska/postanite-partner/", views.partner_landing, {"lang": "hr"}, name="partner-landing-hr-direct"),
    
    # GLOSSAR URLs für alle 12 Sprachen - VOR <str:category>!
    *glossary_urlpatterns,
    
    path("ge/kroatien/<str:category>/", professional_views.professional_list, {"country": "kroatien"}, name="professional-list-ge-direct"),
    path("ge/kroatien/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "kroatien"}, name="professional-detail-ge-direct"),
    path("hr/hrvatska/<str:category>/", professional_views.professional_list, {"country": "hrvatska"}, name="professional-list-hr-direct"),
    path("hr/hrvatska/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "hrvatska"}, name="professional-detail-hr-direct"),
]

urlpatterns += i18n_patterns(
    path('accounts/', include('accounts.urls')),
path('portal/', include('main.professional_portal_urls')),
    path('', include('main.urls')),
    prefix_default_language=True,
)

handler404 = 'main.views_404.smart_404_handler'
