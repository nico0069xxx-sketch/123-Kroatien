from django.urls import path
from main import professional_portal_views

app_name = 'professional_portal'

urlpatterns = [
    path('dashboard/', professional_portal_views.dashboard_gruppe_b, name='dashboard'),
    path('profil/bearbeiten/', professional_portal_views.edit_profile, name='edit_profile'),
    path('passwort-aendern/', professional_portal_views.change_password, name='change_password'),
]