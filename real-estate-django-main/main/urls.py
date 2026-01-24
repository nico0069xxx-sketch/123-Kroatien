from django.urls import path
from . import views
from . import professional_views
from . import xml_views
from . import makler_views
from pages.views import translate_all
from .glossary_urls import glossary_urlpatterns

app_name = 'main'

urlpatterns = [
    path('', views.home, name='home'),
    path('listing/', views.listings, name='listing'),
    path('listings/', views.listings, name='listings'),  # Alias
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('profile/', views.agency_details, name='profile'),
    path('add-property/', views.add_property, name='add_property'),
    path('edit-property/<int:id>/', views.edit_property, name='edit_property'),
    path('delete-property/<int:id>/', views.delete_property, name='delete_property'),
    path('property-details/<int:id>/', views.single_details, name='property_details'),
    path('blog/single/', views.blog_single, name="blog_single"),
    path('blog-single-1', views.blog_single_1, name="blog-single-1"),
    path('blog-single-2', views.blog_single_2, name="blog-single-2"),
    path('blog-single-3', views.blog_single_3, name="blog-single-3"),
    path('send-email/', views.send_email, name='send_email'),
    path('send-registration-email/', views.send_registration_email, name='send-registration-email'),
    path('send-owner-form/', views.send_owner_form, name='send-owner-form'),
    path('faq/', views.faq, name='faq'),
    path('owner/', views.owner, name='owner'),
    path('real-estate-agent/', views.real_estate_agent, name='real-estate-agent'),
    path('building-contractor/', views.building_contractor, name='building-contractor'),
    path('realestate-contractor-registration', views.realestate_contractor_registration, name='realestate-contractor-registration'),
    path('owner-form/', views.owner_form, name='owner-form'),
    path('imprint/', views.imprint, name='imprint'),
    path('data-protection/', views.data_protection, name='data-protection'),
    path('agb', views.agb, name='agb'),
    path('cancellation-policy', views.cancellation_policy, name='cancellation-policy'),
    path('sitemap/', views.sitemap, name='sitemap'),
    path('sitemap', views.sitemap, name='sitemap-no-slash'),  # Redirect für URLs ohne Slash
    path('service', views.service, name='service'),
    # temporary
    path('login-required/', views.loginRequired, name='login_required'),
    path('translate-all/', translate_all, name='translate'),
    
    path('agent/<str:id>/', views.agent, name='agent'),
    path('edit-agent/<str:id>/', views.edit_agent, name='edit_agent'),
    
    # Reference Projects Management
    path('agent/<str:id>/referenzen/', views.reference_projects_list, name='reference_projects_list'),
    path('agent/<str:id>/referenzen/neu/', views.reference_project_create, name='reference_project_create'),
    path('agent/<str:id>/referenzen/<int:project_id>/bearbeiten/', views.reference_project_edit, name='reference_project_edit'),
    path('agent/<str:id>/referenzen/<int:project_id>/loeschen/', views.reference_project_delete, name='reference_project_delete'),
    
    # XML Import
    path('agent/<str:id>/xml-import/', xml_views.xml_import_dashboard, name='xml_import_dashboard'),
    path('agent/<str:id>/xml-import/file/', xml_views.xml_import_file, name='xml_import_file'),
    path('agent/<str:id>/xml-import/url/', xml_views.xml_import_url, name='xml_import_url'),
    
    # ========================================
    # MAKLER PORTAL
    # ========================================
    path('makler-dashboard/', makler_views.makler_dashboard, name='makler_dashboard'),
    path('makler-portal/objekt/neu/', makler_views.makler_objekt_neu, name='makler_objekt_neu'),
    path('makler-portal/objekt/<int:listing_id>/bearbeiten/', makler_views.makler_objekt_bearbeiten, name='makler_objekt_bearbeiten'),
    path('makler-portal/xml-import/', makler_views.makler_xml_import, name='makler_xml_import'),
    path('makler-portal/xml-dokumentation/', makler_views.makler_xml_dokumentation, name='makler_xml_dokumentation'),
    path('makler-portal/anleitung/', makler_views.makler_anleitung, name='makler_anleitung'),
    
    # Makler API Endpoints
    path('api/makler/verkauft/<int:listing_id>/', makler_views.makler_objekt_verkauft, name='makler_objekt_verkauft'),
    path('api/makler/pausieren/<int:listing_id>/', makler_views.makler_objekt_pausieren, name='makler_objekt_pausieren'),
    path('api/makler/aktivieren/<int:listing_id>/', makler_views.makler_objekt_aktivieren, name='makler_objekt_aktivieren'),
    
    # KI-Text Generation API
    path('ge/api/m/gen/', makler_views.makler_ki_beschreibung, name='makler_ki_beschreibung'),
    path('ge/api/m/gen/<int:listing_id>/', makler_views.makler_ki_beschreibung_listing, name='makler_ki_beschreibung_listing'),
    
    # Professional Registration URLs (Bilingual: German & Croatian)
    path('ge/kroatien/professional-registrierung/', views.professional_registration, {'lang': 'ge'}, name='professional-registration-ge'),
    path('hr/hrvatska/registracija-profesionalaca/', views.professional_registration, {'lang': 'hr'}, name='professional-registration-hr'),
    
    # Professional Directory URLs (DE & HR)
    # German URLs - specific URLs BEFORE generic category URLs
    path('ge/kroatien/registrierung/', professional_views.professional_registration, {'country': 'kroatien'}, name='professional-reg-ge'),
    path('ge/kroatien/partner-werden/', views.partner_landing, {'lang': 'ge'}, name='partner-landing-ge'),
    path('ge/kroatien/<str:category>/', professional_views.professional_list, {'country': 'kroatien'}, name='professional-list-ge'),
    path('ge/kroatien/<str:category>/<str:slug>/', professional_views.professional_detail, {'country': 'kroatien'}, name='professional-detail-ge'),
    
    # Croatian URLs - specific URLs BEFORE generic category URLs
    path('hr/hrvatska/registracija/', professional_views.professional_registration, {'country': 'hrvatska'}, name='professional-reg-hr'),
    path('hr/hrvatska/postanite-partner/', views.partner_landing, {'lang': 'hr'}, name='partner-landing-hr'),
    path('hr/hrvatska/<str:category>/', professional_views.professional_list, {'country': 'hrvatska'}, name='professional-list-hr'),
    path('hr/hrvatska/<str:category>/<str:slug>/', professional_views.professional_detail, {'country': 'hrvatska'}, name='professional-detail-hr'),
] + glossary_urlpatterns  # Dynamische Glossar-URLs für alle 12 Sprachen