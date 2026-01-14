"""
URL Configuration für das Professional Portal (Gruppe B)
"""
from django.urls import path
from main import professional_portal_views

app_name = 'professional_portal'

urlpatterns = [
    # Dashboard
    path('dashboard/', professional_portal_views.dashboard_gruppe_b, name='dashboard'),
    
    # Profil
    path('profil/bearbeiten/', professional_portal_views.edit_profile, name='edit_profile'),
    
    # Sicherheit
    path('passwort-aendern/', professional_portal_views.change_password, name='change_password'),
    path('2fa-einrichten/', professional_portal_views.setup_2fa, name='setup_2fa'),
]
