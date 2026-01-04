# URL-Konfiguration für XML-Export
# Fügen Sie diese zu Ihrer realstate/urls.py oder main/urls.py hinzu

"""
ANLEITUNG:
==========

1. Öffnen Sie Ihre Datei: realstate/urls.py

2. Fügen Sie oben zu den Imports hinzu:
   from main.views import listings_xml_openimmo, listings_xml_simple

   ODER (falls Sie die Views in listings/views.py haben):
   from listings.views import listings_xml_openimmo, listings_xml_simple

3. Fügen Sie zu urlpatterns hinzu:
   path('api/listings/xml/', listings_xml_openimmo, name='listings_xml_openimmo'),
   path('api/listings/simple-xml/', listings_xml_simple, name='listings_xml_simple'),

"""

# Beispiel - Vollständige URL-Konfiguration:

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.views import (
    listings_xml_openimmo, 
    listings_xml_simple,
    # ... andere Views
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # XML-Export Endpoints
    path('api/listings/xml/', listings_xml_openimmo, name='listings_xml_openimmo'),
    path('api/listings/openimmo/', listings_xml_openimmo, name='listings_openimmo'),  # Alternative URL
    path('api/listings/simple-xml/', listings_xml_simple, name='listings_xml_simple'),
    
    # Ihre bestehenden URLs
    path('i18n/', include('django.conf.urls.i18n')),
    path('accounts/', include('accounts.urls')),
    path('', include('main.urls')),
    # ... weitere URLs
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# TESTEN SIE DIE XML-URLS:
# ========================
# Nach dem Server-Start können Sie testen:
# 
# OpenImmo XML:
# http://localhost:8000/api/listings/xml/
# http://IhreDomain.com/api/listings/xml/
#
# Einfaches XML:
# http://localhost:8000/api/listings/simple-xml/
# http://IhreDomain.com/api/listings/simple-xml/
