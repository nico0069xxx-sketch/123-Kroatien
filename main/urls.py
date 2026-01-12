from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('listings/', views.listings, name='listings'),
    path('listing/<str:id>/', views.listing, name='listing'),
    path('agent/<str:id>/', views.agent, name='agent'),
    path('blog/', views.blog, name='blog'),
    path('blog-single/', views.blog_single, name='blog_single'),
    path('blog-single-1/', views.blog_single_1, name='blog-single-1'),
    path('blog-single-2/', views.blog_single_2, name='blog-single-2'),
    path('blog-single-3/', views.blog_single_3, name='blog-single-3'),
    path('contact/', views.contact, name='contact'),
    path('owner/', views.owner, name='owner'),
    path('faq/', views.faq, name='faq'),
    path('<str:country>/faq/<slug:slug>/', views.faq_detail, name='faq_detail'),
    path('agb/', views.agb, name='agb'),
    path('imprint/', views.imprint, name='imprint'),
    path('data-protection/', views.data_protection, name='data-protection'),
    path('cancellation-policy/', views.cancellation_policy, name='cancellation-policy'),
    path('service/', views.service, name='service'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('profile/', views.profile, name='profile'),
    path('add-property/', views.add_property, name='add_property'),
    path('edit-property/<str:id>/', views.edit_property, name='edit_property'),
    path('edit-agent/<str:id>/', views.edit_agent, name='edit_agent'),
    path('property-details/<str:id>/', views.property_details, name='property_details'),
    path('real-estate-agent/', views.real_estate_agent, name='real-estate-agent'),
    path('building-contractor/', views.building_contractor, name='building-contractor'),
    path('realestate-contractor-registration/', views.realestate_contractor_registration, name='realestate-contractor-registration'),
    path('translate-listing/<str:id>/', views.translate_listing, name='translate_listing'),
]

from main.xml_export import openimmo_export, croatia_simple_export

urlpatterns += [
    path('api/xml/openimmo/', openimmo_export, name='openimmo_export'),
    path('api/xml/croatia/', croatia_simple_export, name='croatia_export'),
]

from main.content_views import market_report_list, market_report_detail
urlpatterns += [
    # Deutsch
    path('<str:country>/marktberichte/', market_report_list, name='market_reports'),
    path('<str:country>/marktbericht/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail'),
    # Englisch
    path('<str:country>/market-reports/', market_report_list, name='market_reports_en'),
    path('<str:country>/market-report/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_en'),
    # Kroatisch
    path('<str:country>/trzisna-izvjesca/', market_report_list, name='market_reports_hr'),
    path('<str:country>/trzisno-izvjesce/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_hr'),
    # Französisch
    path('<str:country>/rapports-immobiliers/', market_report_list, name='market_reports_fr'),
    path('<str:country>/rapport-immobilier/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_fr'),
    # Niederländisch
    path('<str:country>/marktrapporten/', market_report_list, name='market_reports_nl'),
    path('<str:country>/marktrapport/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_nl'),
    # Polnisch
    path('<str:country>/raporty-rynkowe/', market_report_list, name='market_reports_pl'),
    path('<str:country>/raport-rynkowy/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_pl'),
    # Tschechisch
    path('<str:country>/trzni-zpravy/', market_report_list, name='market_reports_cz'),
    path('<str:country>/trzni-zprava/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_cz'),
    # Slowakisch
    path('<str:country>/trhove-spravy/', market_report_list, name='market_reports_sk'),
    path('<str:country>/trhova-sprava/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_sk'),
    # Russisch
    path('<str:country>/rynochnye-otchety/', market_report_list, name='market_reports_ru'),
    path('<str:country>/rynochnyj-otchet/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_ru'),
    # Griechisch
    path('<str:country>/anafores-agoras/', market_report_list, name='market_reports_gr'),
    path('<str:country>/anafora-agoras/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_gr'),
    # Schwedisch
    path('<str:country>/marknadsrapporter/', market_report_list, name='market_reports_sw'),
    path('<str:country>/marknadsrapport/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_sw'),
    # Norwegisch
    path('<str:country>/markedsrapporter/', market_report_list, name='market_reports_no'),
    path('<str:country>/markedsrapport/<str:region_slug>-<int:year>/', market_report_detail, name='market_report_detail_no'),
]

from main.professional_views import professional_list, professional_detail

# Professional URLs - alle 5 Kategorien in 12 Sprachen
urlpatterns += [
    # Immobilienmakler
    path('<str:country>/immobilienmakler/', professional_list, {'category': 'immobilienmakler'}, name='professionals_agent_ge'),
    path('<str:country>/immobilienmakler/<slug:slug>/', professional_detail, {'category': 'immobilienmakler'}, name='professional_agent_detail_ge'),
    path('<str:country>/real-estate-agents/', professional_list, {'category': 'real-estate-agents'}, name='professionals_agent_en'),
    path('<str:country>/real-estate-agents/<slug:slug>/', professional_detail, {'category': 'real-estate-agents'}, name='professional_agent_detail_en'),
    path('<str:country>/agencije-za-nekretnine/', professional_list, {'category': 'agencije-za-nekretnine'}, name='professionals_agent_hr'),
    path('<str:country>/agencije-za-nekretnine/<slug:slug>/', professional_detail, {'category': 'agencije-za-nekretnine'}, name='professional_agent_detail_hr'),
    path('<str:country>/agents-immobiliers/', professional_list, {'category': 'agents-immobiliers'}, name='professionals_agent_fr'),
    path('<str:country>/agents-immobiliers/<slug:slug>/', professional_detail, {'category': 'agents-immobiliers'}, name='professional_agent_detail_fr'),
    path('<str:country>/makelaars/', professional_list, {'category': 'makelaars'}, name='professionals_agent_nl'),
    path('<str:country>/makelaars/<slug:slug>/', professional_detail, {'category': 'makelaars'}, name='professional_agent_detail_nl'),
    path('<str:country>/agenci-nieruchomosci/', professional_list, {'category': 'agenci-nieruchomosci'}, name='professionals_agent_pl'),
    path('<str:country>/agenci-nieruchomosci/<slug:slug>/', professional_detail, {'category': 'agenci-nieruchomosci'}, name='professional_agent_detail_pl'),
    path('<str:country>/realitni-makleri/', professional_list, {'category': 'realitni-makleri'}, name='professionals_agent_cz'),
    path('<str:country>/realitni-makleri/<slug:slug>/', professional_detail, {'category': 'realitni-makleri'}, name='professional_agent_detail_cz'),
    path('<str:country>/agenty-nedvizhimosti/', professional_list, {'category': 'agenty-nedvizhimosti'}, name='professionals_agent_ru'),
    path('<str:country>/agenty-nedvizhimosti/<slug:slug>/', professional_detail, {'category': 'agenty-nedvizhimosti'}, name='professional_agent_detail_ru'),
    path('<str:country>/mesites-akiniton/', professional_list, {'category': 'mesites-akiniton'}, name='professionals_agent_gr'),
    path('<str:country>/mesites-akiniton/<slug:slug>/', professional_detail, {'category': 'mesites-akiniton'}, name='professional_agent_detail_gr'),
    path('<str:country>/fastighetsmaklare/', professional_list, {'category': 'fastighetsmaklare'}, name='professionals_agent_sw'),
    path('<str:country>/fastighetsmaklare/<slug:slug>/', professional_detail, {'category': 'fastighetsmaklare'}, name='professional_agent_detail_sw'),
    path('<str:country>/eiendomsmeglere/', professional_list, {'category': 'eiendomsmeglere'}, name='professionals_agent_no'),
    path('<str:country>/eiendomsmeglere/<slug:slug>/', professional_detail, {'category': 'eiendomsmeglere'}, name='professional_agent_detail_no'),
    
    # Bauunternehmen
    path('<str:country>/bauunternehmen/', professional_list, {'category': 'bauunternehmen'}, name='professionals_construction_ge'),
    path('<str:country>/bauunternehmen/<slug:slug>/', professional_detail, {'category': 'bauunternehmen'}, name='professional_construction_detail_ge'),
    path('<str:country>/construction-companies/', professional_list, {'category': 'construction-companies'}, name='professionals_construction_en'),
    path('<str:country>/construction-companies/<slug:slug>/', professional_detail, {'category': 'construction-companies'}, name='professional_construction_detail_en'),
    path('<str:country>/gradevinske-tvrtke/', professional_list, {'category': 'gradevinske-tvrtke'}, name='professionals_construction_hr'),
    path('<str:country>/gradevinske-tvrtke/<slug:slug>/', professional_detail, {'category': 'gradevinske-tvrtke'}, name='professional_construction_detail_hr'),
    path('<str:country>/entreprises-construction/', professional_list, {'category': 'entreprises-construction'}, name='professionals_construction_fr'),
    path('<str:country>/entreprises-construction/<slug:slug>/', professional_detail, {'category': 'entreprises-construction'}, name='professional_construction_detail_fr'),
    path('<str:country>/bouwbedrijven/', professional_list, {'category': 'bouwbedrijven'}, name='professionals_construction_nl'),
    path('<str:country>/bouwbedrijven/<slug:slug>/', professional_detail, {'category': 'bouwbedrijven'}, name='professional_construction_detail_nl'),
    path('<str:country>/firmy-budowlane/', professional_list, {'category': 'firmy-budowlane'}, name='professionals_construction_pl'),
    path('<str:country>/firmy-budowlane/<slug:slug>/', professional_detail, {'category': 'firmy-budowlane'}, name='professional_construction_detail_pl'),
    path('<str:country>/stavebni-firmy/', professional_list, {'category': 'stavebni-firmy'}, name='professionals_construction_cz'),
    path('<str:country>/stavebni-firmy/<slug:slug>/', professional_detail, {'category': 'stavebni-firmy'}, name='professional_construction_detail_cz'),
    path('<str:country>/stroitelnye-kompanii/', professional_list, {'category': 'stroitelnye-kompanii'}, name='professionals_construction_ru'),
    path('<str:country>/stroitelnye-kompanii/<slug:slug>/', professional_detail, {'category': 'stroitelnye-kompanii'}, name='professional_construction_detail_ru'),
    path('<str:country>/kataskevestikes-etaireies/', professional_list, {'category': 'kataskevestikes-etaireies'}, name='professionals_construction_gr'),
    path('<str:country>/kataskevestikes-etaireies/<slug:slug>/', professional_detail, {'category': 'kataskevestikes-etaireies'}, name='professional_construction_detail_gr'),
    path('<str:country>/byggforetag/', professional_list, {'category': 'byggforetag'}, name='professionals_construction_sw'),
    path('<str:country>/byggforetag/<slug:slug>/', professional_detail, {'category': 'byggforetag'}, name='professional_construction_detail_sw'),
    path('<str:country>/byggefirmaer/', professional_list, {'category': 'byggefirmaer'}, name='professionals_construction_no'),
    path('<str:country>/byggefirmaer/<slug:slug>/', professional_detail, {'category': 'byggefirmaer'}, name='professional_construction_detail_no'),
    
    # Rechtsanwälte
    path('<str:country>/rechtsanwaelte/', professional_list, {'category': 'rechtsanwaelte'}, name='professionals_lawyer_ge'),
    path('<str:country>/rechtsanwaelte/<slug:slug>/', professional_detail, {'category': 'rechtsanwaelte'}, name='professional_lawyer_detail_ge'),
    path('<str:country>/lawyers/', professional_list, {'category': 'lawyers'}, name='professionals_lawyer_en'),
    path('<str:country>/lawyers/<slug:slug>/', professional_detail, {'category': 'lawyers'}, name='professional_lawyer_detail_en'),
    path('<str:country>/odvjetnici/', professional_list, {'category': 'odvjetnici'}, name='professionals_lawyer_hr'),
    path('<str:country>/odvjetnici/<slug:slug>/', professional_detail, {'category': 'odvjetnici'}, name='professional_lawyer_detail_hr'),
    path('<str:country>/avocats/', professional_list, {'category': 'avocats'}, name='professionals_lawyer_fr'),
    path('<str:country>/avocats/<slug:slug>/', professional_detail, {'category': 'avocats'}, name='professional_lawyer_detail_fr'),
    path('<str:country>/advocaten/', professional_list, {'category': 'advocaten'}, name='professionals_lawyer_nl'),
    path('<str:country>/advocaten/<slug:slug>/', professional_detail, {'category': 'advocaten'}, name='professional_lawyer_detail_nl'),
    path('<str:country>/prawnicy/', professional_list, {'category': 'prawnicy'}, name='professionals_lawyer_pl'),
    path('<str:country>/prawnicy/<slug:slug>/', professional_detail, {'category': 'prawnicy'}, name='professional_lawyer_detail_pl'),
    path('<str:country>/pravnici/', professional_list, {'category': 'pravnici'}, name='professionals_lawyer_cz'),
    path('<str:country>/pravnici/<slug:slug>/', professional_detail, {'category': 'pravnici'}, name='professional_lawyer_detail_cz'),
    path('<str:country>/advokaty/', professional_list, {'category': 'advokaty'}, name='professionals_lawyer_ru'),
    path('<str:country>/advokaty/<slug:slug>/', professional_detail, {'category': 'advokaty'}, name='professional_lawyer_detail_ru'),
    path('<str:country>/dikigoroi/', professional_list, {'category': 'dikigoroi'}, name='professionals_lawyer_gr'),
    path('<str:country>/dikigoroi/<slug:slug>/', professional_detail, {'category': 'dikigoroi'}, name='professional_lawyer_detail_gr'),
    path('<str:country>/advokater/', professional_list, {'category': 'advokater'}, name='professionals_lawyer_sw'),
    path('<str:country>/advokater/<slug:slug>/', professional_detail, {'category': 'advokater'}, name='professional_lawyer_detail_sw'),
    
    # Steuerberater
    path('<str:country>/steuerberater/', professional_list, {'category': 'steuerberater'}, name='professionals_tax_ge'),
    path('<str:country>/steuerberater/<slug:slug>/', professional_detail, {'category': 'steuerberater'}, name='professional_tax_detail_ge'),
    path('<str:country>/tax-advisors/', professional_list, {'category': 'tax-advisors'}, name='professionals_tax_en'),
    path('<str:country>/tax-advisors/<slug:slug>/', professional_detail, {'category': 'tax-advisors'}, name='professional_tax_detail_en'),
    path('<str:country>/porezni-savjetnici/', professional_list, {'category': 'porezni-savjetnici'}, name='professionals_tax_hr'),
    path('<str:country>/porezni-savjetnici/<slug:slug>/', professional_detail, {'category': 'porezni-savjetnici'}, name='professional_tax_detail_hr'),
    path('<str:country>/conseillers-fiscaux/', professional_list, {'category': 'conseillers-fiscaux'}, name='professionals_tax_fr'),
    path('<str:country>/conseillers-fiscaux/<slug:slug>/', professional_detail, {'category': 'conseillers-fiscaux'}, name='professional_tax_detail_fr'),
    path('<str:country>/belastingadviseurs/', professional_list, {'category': 'belastingadviseurs'}, name='professionals_tax_nl'),
    path('<str:country>/belastingadviseurs/<slug:slug>/', professional_detail, {'category': 'belastingadviseurs'}, name='professional_tax_detail_nl'),
    path('<str:country>/doradcy-podatkowi/', professional_list, {'category': 'doradcy-podatkowi'}, name='professionals_tax_pl'),
    path('<str:country>/doradcy-podatkowi/<slug:slug>/', professional_detail, {'category': 'doradcy-podatkowi'}, name='professional_tax_detail_pl'),
    path('<str:country>/danovi-poradci/', professional_list, {'category': 'danovi-poradci'}, name='professionals_tax_cz'),
    path('<str:country>/danovi-poradci/<slug:slug>/', professional_detail, {'category': 'danovi-poradci'}, name='professional_tax_detail_cz'),
    path('<str:country>/nalogovye-konsultanty/', professional_list, {'category': 'nalogovye-konsultanty'}, name='professionals_tax_ru'),
    path('<str:country>/nalogovye-konsultanty/<slug:slug>/', professional_detail, {'category': 'nalogovye-konsultanty'}, name='professional_tax_detail_ru'),
    path('<str:country>/forologikoi-symvouloi/', professional_list, {'category': 'forologikoi-symvouloi'}, name='professionals_tax_gr'),
    path('<str:country>/forologikoi-symvouloi/<slug:slug>/', professional_detail, {'category': 'forologikoi-symvouloi'}, name='professional_tax_detail_gr'),
    path('<str:country>/skatteradgivare/', professional_list, {'category': 'skatteradgivare'}, name='professionals_tax_sw'),
    path('<str:country>/skatteradgivare/<slug:slug>/', professional_detail, {'category': 'skatteradgivare'}, name='professional_tax_detail_sw'),
    path('<str:country>/skatteradgivere/', professional_list, {'category': 'skatteradgivere'}, name='professionals_tax_no'),
    path('<str:country>/skatteradgivere/<slug:slug>/', professional_detail, {'category': 'skatteradgivere'}, name='professional_tax_detail_no'),
    
    # Architekten
    path('<str:country>/architekten/', professional_list, {'category': 'architekten'}, name='professionals_architect_ge'),
    path('<str:country>/architekten/<slug:slug>/', professional_detail, {'category': 'architekten'}, name='professional_architect_detail_ge'),
    path('<str:country>/architects/', professional_list, {'category': 'architects'}, name='professionals_architect_en'),
    path('<str:country>/architects/<slug:slug>/', professional_detail, {'category': 'architects'}, name='professional_architect_detail_en'),
    path('<str:country>/arhitekti/', professional_list, {'category': 'arhitekti'}, name='professionals_architect_hr'),
    path('<str:country>/arhitekti/<slug:slug>/', professional_detail, {'category': 'arhitekti'}, name='professional_architect_detail_hr'),
    path('<str:country>/architectes/', professional_list, {'category': 'architectes'}, name='professionals_architect_fr'),
    path('<str:country>/architectes/<slug:slug>/', professional_detail, {'category': 'architectes'}, name='professional_architect_detail_fr'),
    path('<str:country>/architecten/', professional_list, {'category': 'architecten'}, name='professionals_architect_nl'),
    path('<str:country>/architecten/<slug:slug>/', professional_detail, {'category': 'architecten'}, name='professional_architect_detail_nl'),
    path('<str:country>/architekci/', professional_list, {'category': 'architekci'}, name='professionals_architect_pl'),
    path('<str:country>/architekci/<slug:slug>/', professional_detail, {'category': 'architekci'}, name='professional_architect_detail_pl'),
    path('<str:country>/architekti/', professional_list, {'category': 'architekti'}, name='professionals_architect_cz'),
    path('<str:country>/architekti/<slug:slug>/', professional_detail, {'category': 'architekti'}, name='professional_architect_detail_cz'),
    path('<str:country>/arhitektory/', professional_list, {'category': 'arhitektory'}, name='professionals_architect_ru'),
    path('<str:country>/arhitektory/<slug:slug>/', professional_detail, {'category': 'arhitektory'}, name='professional_architect_detail_ru'),
    path('<str:country>/architektons/', professional_list, {'category': 'architektons'}, name='professionals_architect_gr'),
    path('<str:country>/architektons/<slug:slug>/', professional_detail, {'category': 'architektons'}, name='professional_architect_detail_gr'),
    path('<str:country>/arkitekter/', professional_list, {'category': 'arkitekter'}, name='professionals_architect_sw'),
    path('<str:country>/arkitekter/<slug:slug>/', professional_detail, {'category': 'arkitekter'}, name='professional_architect_detail_sw'),
]

# ALTE REGISTRIERUNG DEAKTIVIERT - ersetzt durch mehrstufiges Formular
# from main.professional_views import professional_registration
# urlpatterns += [
#     path('<str:country>/professional-registrierung/', professional_registration, name='professional_registration_ge'),
#     path('<str:country>/registracija-profesionalaca/', professional_registration, name='professional_registration_hr'),
# ]

# Chatbot API
from main.views import chatbot_api
urlpatterns += [
    path('api/chatbot/', chatbot_api, name='chatbot_api'),
]

# Wichtige Adressen (12 Sprachen)
from main.address_views import important_addresses
urlpatterns += [
    path('<str:country>/wichtige-adressen/', important_addresses, name='important_addresses_ge'),
    path('<str:country>/important-addresses/', important_addresses, name='important_addresses_en'),
    path('<str:country>/vazne-adrese/', important_addresses, name='important_addresses_hr'),
    path('<str:country>/adresses-importantes/', important_addresses, name='important_addresses_fr'),
    path('<str:country>/belangrijke-adressen/', important_addresses, name='important_addresses_nl'),
    path('<str:country>/wazne-adresy/', important_addresses, name='important_addresses_pl'),
    path('<str:country>/dulezite-adresy/', important_addresses, name='important_addresses_cz'),
    path('<str:country>/dolezite-adresy/', important_addresses, name='important_addresses_sk'),
    path('<str:country>/vazhnye-adresa/', important_addresses, name='important_addresses_ru'),
    path('<str:country>/simantikes-diefthinseis/', important_addresses, name='important_addresses_gr'),
    path('<str:country>/viktiga-adresser/', important_addresses, name='important_addresses_sw'),
    path('<str:country>/viktige-adresser/', important_addresses, name='important_addresses_no'),
    path('api/smart-search/', views.smart_search, name='smart_search'),

    # RSS Feeds (SEO + AI optimiert)
    path('rss/listings/', views.rss_listings, {'lang': 'ge'}, name='rss_listings_ge'),
    path('en/rss/listings/', views.rss_listings, {'lang': 'en'}, name='rss_listings_en'),
    path('hr/rss/listings/', views.rss_listings, {'lang': 'hr'}, name='rss_listings_hr'),
    path('fr/rss/listings/', views.rss_listings, {'lang': 'fr'}, name='rss_listings_fr'),
    path('nl/rss/listings/', views.rss_listings, {'lang': 'nl'}, name='rss_listings_nl'),
    path('pl/rss/listings/', views.rss_listings, {'lang': 'pl'}, name='rss_listings_pl'),
    path('cz/rss/listings/', views.rss_listings, {'lang': 'cz'}, name='rss_listings_cz'),
    path('sk/rss/listings/', views.rss_listings, {'lang': 'sk'}, name='rss_listings_sk'),
    path('ru/rss/listings/', views.rss_listings, {'lang': 'ru'}, name='rss_listings_ru'),
    path('gr/rss/listings/', views.rss_listings, {'lang': 'gr'}, name='rss_listings_gr'),
    path('sw/rss/listings/', views.rss_listings, {'lang': 'sw'}, name='rss_listings_sw'),
    path('no/rss/listings/', views.rss_listings, {'lang': 'no'}, name='rss_listings_no'),

    # SEO: Sitemap & robots.txt
    path('sitemap.xml', views.xml_sitemap, name='xml_sitemap'),
    path('robots.txt', views.robots_txt, name='robots_txt'),

    # News-Bereich (SEO + AI optimiert)
    
    
    
    
    
    
    
    
    
    
    
    

    # News-Bereich
    path('<str:country>/nachrichten/', views.news_page, name='news'),

    # News-Bereich (alle Sprachen)
    path('croatia/news/', views.news_page, name='news_en'),
    path('hrvatska/vijesti/', views.news_page, name='news_hr'),
    path('croatie/actualites/', views.news_page, name='news_fr'),
    path('kroatie/nieuws/', views.news_page, name='news_nl'),
    path('chorwacja/wiadomosci/', views.news_page, name='news_pl'),
    path('chorvatsko/zpravy/', views.news_page, name='news_cz'),
    path('horvatiya/novosti/', views.news_page, name='news_ru'),
    path('kroatia/nea/', views.news_page, name='news_gr'),
]

# =============================================================================
# MEHRSTUFIGE PROFESSIONAL-REGISTRIERUNG
# =============================================================================
from main.registration_views import (
    registration_step1, registration_step2, registration_step3,
    ajax_check_spelling, ajax_improve_text, ajax_regenerate_suggestions, ajax_validate_oib
)

urlpatterns += [
    # Registrierung Schritt 1 (ersetzt alte Registrierung)
    path('<str:country>/professional-registrierung/', registration_step1, name='registration_step1'),
    path('<str:country>/professional-registration/', registration_step1, name='registration_step1_en'),
    path('<str:country>/registracija-profesionalaca/', registration_step1, name='registration_step1_hr'),
    
    # Registrierung Schritt 2
    path('<str:country>/professional-registrierung-schritt2/', registration_step2, name='registration_step2'),
    path('<str:country>/professional-registration-step2/', registration_step2, name='registration_step2_en'),
    path('<str:country>/registracija-korak2/', registration_step2, name='registration_step2_hr'),
    
    # Registrierung Schritt 3
    path('<str:country>/professional-registrierung-schritt3/', registration_step3, name='registration_step3'),
    path('<str:country>/professional-registration-step3/', registration_step3, name='registration_step3_en'),
    path('<str:country>/registracija-korak3/', registration_step3, name='registration_step3_hr'),
    
    # AJAX Endpoints
    path('api/validate-oib/', ajax_validate_oib, name='ajax_validate_oib'),
    path('api/check-spelling/', ajax_check_spelling, name='ajax_check_spelling'),
    path('api/improve-text/', ajax_improve_text, name='ajax_improve_text'),
    path('api/regenerate-suggestions/', ajax_regenerate_suggestions, name='ajax_regenerate_suggestions'),
]

# Datenschutz Verifizierung
from django.shortcuts import render as _render

def privacy_verification(request, country):
    return _render(request, 'main/registration/privacy_verification.html', {})

urlpatterns += [
    path('<str:country>/datenschutz-verifizierung/', privacy_verification, name='privacy_verification'),
]
