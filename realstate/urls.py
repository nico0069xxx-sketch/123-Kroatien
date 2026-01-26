from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static 
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from main.views import set_language_from_url, news_page, sitemap as html_sitemap, imprint, agb, cancellation_policy, home
from main.xml_views import rss_listings, xml_sitemap, robots_txt, llms_txt
from django.contrib.sitemaps.views import sitemap
from main.glossary_sitemaps import get_glossary_sitemaps

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path("set-language/<str:user_language>/", set_language_from_url, name="set_language_from_url"),
    path('robots.txt', robots_txt, name='robots_txt'),
    path('llms.txt', llms_txt, name='llms_txt'),
    path('sitemap.xml', xml_sitemap, name='xml_sitemap'),
    path('sitemaps/glossary.xml', sitemap, {'sitemaps': get_glossary_sitemaps()}, name='glossary-sitemap'),
    path('sitemap', html_sitemap, name='sitemap-html'),
    
    # Sitemap für alle 12 Sprachen (ohne Slash)
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
    
    # Sitemap für alle 12 Sprachen (MIT Slash)
    path('ge/sitemap/', html_sitemap, name='sitemap-ge-slash'),
    path('en/sitemap/', html_sitemap, name='sitemap-en-slash'),
    path('hr/sitemap/', html_sitemap, name='sitemap-hr-slash'),
    path('fr/sitemap/', html_sitemap, name='sitemap-fr-slash'),
    path('nl/sitemap/', html_sitemap, name='sitemap-nl-slash'),
    path('pl/sitemap/', html_sitemap, name='sitemap-pl-slash'),
    path('cz/sitemap/', html_sitemap, name='sitemap-cz-slash'),
    path('sk/sitemap/', html_sitemap, name='sitemap-sk-slash'),
    path('ru/sitemap/', html_sitemap, name='sitemap-ru-slash'),
    path('gr/sitemap/', html_sitemap, name='sitemap-gr-slash'),
    path('sw/sitemap/', html_sitemap, name='sitemap-sw-slash'),
    path('no/sitemap/', html_sitemap, name='sitemap-no-slash'),
    
    # Statische Seiten: IMPRINT für alle 12 Sprachen
    path('ge/imprint/', imprint, name='imprint-ge'),
    path('en/imprint/', imprint, name='imprint-en'),
    path('hr/imprint/', imprint, name='imprint-hr'),
    path('fr/imprint/', imprint, name='imprint-fr'),
    path('nl/imprint/', imprint, name='imprint-nl'),
    path('pl/imprint/', imprint, name='imprint-pl'),
    path('cz/imprint/', imprint, name='imprint-cz'),
    path('sk/imprint/', imprint, name='imprint-sk'),
    path('ru/imprint/', imprint, name='imprint-ru'),
    path('gr/imprint/', imprint, name='imprint-gr'),
    path('sw/imprint/', imprint, name='imprint-sw'),
    path('no/imprint/', imprint, name='imprint-no'),
    
    # Statische Seiten: AGB für alle 12 Sprachen
    path('ge/agb/', agb, name='agb-ge'),
    path('en/agb/', agb, name='agb-en'),
    path('hr/agb/', agb, name='agb-hr'),
    path('fr/agb/', agb, name='agb-fr'),
    path('nl/agb/', agb, name='agb-nl'),
    path('pl/agb/', agb, name='agb-pl'),
    path('cz/agb/', agb, name='agb-cz'),
    path('sk/agb/', agb, name='agb-sk'),
    path('ru/agb/', agb, name='agb-ru'),
    path('gr/agb/', agb, name='agb-gr'),
    path('sw/agb/', agb, name='agb-sw'),
    path('no/agb/', agb, name='agb-no'),
    
    # Statische Seiten: CANCELLATION-POLICY für alle 12 Sprachen
    path('ge/cancellation-policy/', cancellation_policy, name='cancellation-policy-ge'),
    path('en/cancellation-policy/', cancellation_policy, name='cancellation-policy-en'),
    path('hr/cancellation-policy/', cancellation_policy, name='cancellation-policy-hr'),
    path('fr/cancellation-policy/', cancellation_policy, name='cancellation-policy-fr'),
    path('nl/cancellation-policy/', cancellation_policy, name='cancellation-policy-nl'),
    path('pl/cancellation-policy/', cancellation_policy, name='cancellation-policy-pl'),
    path('cz/cancellation-policy/', cancellation_policy, name='cancellation-policy-cz'),
    path('sk/cancellation-policy/', cancellation_policy, name='cancellation-policy-sk'),
    path('ru/cancellation-policy/', cancellation_policy, name='cancellation-policy-ru'),
    path('gr/cancellation-policy/', cancellation_policy, name='cancellation-policy-gr'),
    path('sw/cancellation-policy/', cancellation_policy, name='cancellation-policy-sw'),
    path('no/cancellation-policy/', cancellation_policy, name='cancellation-policy-no'),
    
    # Norwegische Startseite (explizit, da i18n_patterns Problem mit 'no')
    path('no/', home, name='home-no'),
    
    # RSS Feeds
    path('rss/listings/', rss_listings, {'lang': 'ge'}, name='rss_listings'),
    path('en/rss/listings/', rss_listings, {'lang': 'en'}, name='rss_en'),
    path('hr/rss/listings/', rss_listings, {'lang': 'hr'}, name='rss_hr'),
    
    # Admin & CKEditor
    path('nik-verwaltung-2026/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('api/', include('realstate.chatbot_urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Makler-Portal
from main.professional_totp import (
    professional_login,
    professional_setup_2fa,
    professional_verify_2fa_setup,
    professional_verify_2fa_login,
)
from main.email_2fa import (
    email_2fa_send,
    email_2fa_verify,
    email_2fa_resend,
    choose_2fa_method,
    choose_email_2fa,
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

# Content URLs für alle 12 Sprachen
from main import professional_views, views, matching_views
from main import address_views, content_views
from main.glossary_urls import glossary_urlpatterns
from main.content_urls import content_urlpatterns

# Content URLs (News, Adressen, Marktberichte) für alle 12 Sprachen
urlpatterns += content_urlpatterns

# Registrierung NUR für DE und HR
urlpatterns += [
    path("ge/kroatien/registrierung/", professional_views.professional_registration, {'country': 'kroatien'}, name="registration-ge"),
    path("hr/hrvatska/registracija/", professional_views.professional_registration, {'country': 'hrvatska'}, name="registration-hr"),
]

# Spezifische URLs
urlpatterns += [
    path("ge/kroatien/partner-werden/", views.partner_landing, {"lang": "ge"}, name="partner-landing-ge-direct"),
    path("hr/hrvatska/postanite-partner/", views.partner_landing, {"lang": "hr"}, name="partner-landing-hr-direct"),
    path("en/croatia/become-partner/", views.partner_landing, {"lang": "en"}, name="partner-landing-en-direct"),
    
    # Experten-Finder für alle Sprachen
    path("ge/kroatien/experten-finder/", matching_views.matching_page, name="experten-finder-ge-direct"),
    path("hr/hrvatska/pronalazac-strucnjaka/", matching_views.matching_page, name="experten-finder-hr-direct"),
    path("en/croatia/expert-finder/", matching_views.matching_page, name="experten-finder-en-direct"),
    path("fr/croatie/recherche-experts/", matching_views.matching_page, name="experten-finder-fr-direct"),
    path("nl/kroatie/expert-zoeker/", matching_views.matching_page, name="experten-finder-nl-direct"),
    path("pl/chorwacja/wyszukiwarka-ekspertow/", matching_views.matching_page, name="experten-finder-pl-direct"),
    path("cz/chorvatsko/vyhledavac-odborniku/", matching_views.matching_page, name="experten-finder-cz-direct"),
    path("sk/chorvatsko/vyhladavac-odbornikov/", matching_views.matching_page, name="experten-finder-sk-direct"),
    path("ru/horvatiya/poisk-ekspertov/", matching_views.matching_page, name="experten-finder-ru-direct"),
    path("gr/kroatia/anazhthsh-eidikwn/", matching_views.matching_page, name="experten-finder-gr-direct"),
    path("sw/kroatien/expert-sokare/", matching_views.matching_page, name="experten-finder-sw-direct"),
    path("no/kroatia/ekspert-soker/", matching_views.matching_page, name="experten-finder-no-direct"),
    
    # GLOSSAR URLs für alle 12 Sprachen
    *glossary_urlpatterns,
    
    # Generische Professional URLs für alle 12 Sprachen
    path("ge/kroatien/<str:category>/", professional_views.professional_list, {"country": "kroatien"}, name="professional-list-ge-direct"),
    path("ge/kroatien/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "kroatien"}, name="professional-detail-ge-direct"),
    path("hr/hrvatska/<str:category>/", professional_views.professional_list, {"country": "hrvatska"}, name="professional-list-hr-direct"),
    path("hr/hrvatska/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "hrvatska"}, name="professional-detail-hr-direct"),
    path("en/croatia/<str:category>/", professional_views.professional_list, {"country": "croatia"}, name="professional-list-en-direct"),
    path("en/croatia/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "croatia"}, name="professional-detail-en-direct"),
    path("fr/croatie/<str:category>/", professional_views.professional_list, {"country": "croatie"}, name="professional-list-fr-direct"),
    path("fr/croatie/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "croatie"}, name="professional-detail-fr-direct"),
    path("nl/kroatie/<str:category>/", professional_views.professional_list, {"country": "kroatie"}, name="professional-list-nl-direct"),
    path("nl/kroatie/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "kroatie"}, name="professional-detail-nl-direct"),
    path("pl/chorwacja/<str:category>/", professional_views.professional_list, {"country": "chorwacja"}, name="professional-list-pl-direct"),
    path("pl/chorwacja/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "chorwacja"}, name="professional-detail-pl-direct"),
    path("cz/chorvatsko/<str:category>/", professional_views.professional_list, {"country": "chorvatsko"}, name="professional-list-cz-direct"),
    path("cz/chorvatsko/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "chorvatsko"}, name="professional-detail-cz-direct"),
    path("sk/chorvatsko/<str:category>/", professional_views.professional_list, {"country": "chorvatsko"}, name="professional-list-sk-direct"),
    path("sk/chorvatsko/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "chorvatsko"}, name="professional-detail-sk-direct"),
    path("ru/horvatiya/<str:category>/", professional_views.professional_list, {"country": "horvatiya"}, name="professional-list-ru-direct"),
    path("ru/horvatiya/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "horvatiya"}, name="professional-detail-ru-direct"),
    path("gr/kroatia/<str:category>/", professional_views.professional_list, {"country": "kroatia"}, name="professional-list-gr-direct"),
    path("gr/kroatia/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "kroatia"}, name="professional-detail-gr-direct"),
    path("sw/kroatien/<str:category>/", professional_views.professional_list, {"country": "kroatien"}, name="professional-list-sw-direct"),
    path("sw/kroatien/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "kroatien"}, name="professional-detail-sw-direct"),
    path("no/kroatia/<str:category>/", professional_views.professional_list, {"country": "kroatia"}, name="professional-list-no-direct"),
    path("no/kroatia/<str:category>/<str:slug>/", professional_views.professional_detail, {"country": "kroatia"}, name="professional-detail-no-direct"),
]

urlpatterns += i18n_patterns(
    path('accounts/', include('accounts.urls')),
    path('portal/', include('main.professional_portal_urls')),
    path('', include('main.urls')),
    prefix_default_language=True,
)

handler404 = 'main.views_404.smart_404_handler'