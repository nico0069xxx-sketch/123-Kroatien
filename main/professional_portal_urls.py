from django.urls import path
from main import professional_portal_views

app_name = 'professional_portal'

urlpatterns = [
    path('dashboard/', professional_portal_views.dashboard_gruppe_b, name='dashboard'),
    path('profil/bearbeiten/', professional_portal_views.edit_profile, name='edit_profile'),
    path('passwort-aendern/', professional_portal_views.change_password, name='change_password'),
    path('2fa-auswahl/', professional_portal_views.twofa_auswahl, name='2fa_auswahl'),
    path('2fa-einrichten/', professional_portal_views.setup_2fa, name='setup_2fa'),
    path('2fa-email-waehlen/', professional_portal_views.setup_email_2fa, name='setup_email_2fa'),
    path('2fa-email-verifizieren/', professional_portal_views.verify_email_2fa, name='verify_email_2fa'),
    path('2fa-email-erneut/', professional_portal_views.resend_email_code, name='resend_email_code'),
    path('ki-beschreibung/', professional_portal_views.generate_description, name='generate_description'),
    path('anleitung/', professional_portal_views.anleitung, name='anleitung'),
]
