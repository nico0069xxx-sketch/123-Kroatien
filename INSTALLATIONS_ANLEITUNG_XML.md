# ==========================================
# INSTALLATIONS-ANLEITUNG: XML-SCHNITTSTELLE
# für Ihr Django Immobilien-Marktplatz
# ==========================================

## WAS WURDE ENTWICKELT:
========================

✅ XML-Export im **OpenImmo 1.2.7 Format** (Standard für Immobilien-Portale)
✅ Einfaches XML-Format als Alternative
✅ Automatischer Export aller veröffentlichten Immobilien
✅ Makler-Informationen inklusive (OIB-Nummer, Firma, etc.)
✅ Alle Fotos und Details enthalten
✅ Mehrsprachig (Kroatisch als Standard)


## DATEIEN, DIE SIE ERHALTEN HABEN:
====================================

1. `xml_export.py` - XML-Generator-Klassen
2. `xml_views.py` - Django Views für XML-Export
3. `xml_urls.py` - URL-Konfiguration (Beispiele)


## SCHRITT-FÜR-SCHRITT-ANLEITUNG:
==================================

### SCHRITT 1: Dateien in Ihr Projekt kopieren
-----------------------------------------------

1. Öffnen Sie Ihren Django-Projekt-Ordner: `real-estate-django-main`

2. Gehen Sie in den Ordner: `listings/`

3. ERSTELLEN Sie eine neue Datei: `xml_export.py`
   - Kopieren Sie den KOMPLETTEN Inhalt aus der Datei `django_xml_export.py`
   - Speichern Sie die Datei

4. Öffnen Sie die vorhandene Datei: `listings/views.py`
   - Fügen Sie ganz OBEN zu den Imports hinzu:
   
   ```python
   from .xml_export import OpenImmoXMLGenerator, SimpleXMLGenerator
   from django.http import HttpResponse
   ```

5. Fügen Sie ganz UNTEN in `listings/views.py` die neuen Views hinzu:
   - Kopieren Sie den Inhalt aus `django_xml_views.py`
   - Fügen Sie ihn am Ende der Datei ein


### SCHRITT 2: URLs konfigurieren
-----------------------------------

1. Öffnen Sie: `realstate/urls.py`

2. Fügen Sie zu den Imports hinzu (ganz oben):
   ```python
   from listings.views import listings_xml_openimmo, listings_xml_simple
   ```

3. Fügen Sie in die `urlpatterns = [...]` Liste hinzu:
   ```python
   # XML-Export Endpoints
   path('api/listings/xml/', listings_xml_openimmo, name='listings_xml_openimmo'),
   path('api/listings/simple-xml/', listings_xml_simple, name='listings_xml_simple'),
   ```

   Die Liste sollte dann z.B. so aussehen:
   ```python
   urlpatterns = [
       path('admin/', admin.site.urls),
       path('api/listings/xml/', listings_xml_openimmo, name='listings_xml_openimmo'),
       path('api/listings/simple-xml/', listings_xml_simple, name='listings_xml_simple'),
       path('accounts/', include('accounts.urls')),
       path('', include('main.urls')),
   ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
   ```


### SCHRITT 3: Server neu starten
-----------------------------------

1. Falls Ihr Django-Server läuft, stoppen Sie ihn (Strg+C)

2. Starten Sie neu:
   ```
   python manage.py runserver
   ```


### SCHRITT 4: Testen Sie die XML-Schnittstelle
------------------------------------------------

Öffnen Sie in Ihrem Browser:

**OpenImmo XML (Standard-Format):**
http://localhost:8000/api/listings/xml/

**Einfaches XML:**
http://localhost:8000/api/listings/simple-xml/

Sie sollten jetzt XML-Daten sehen! 🎉


## WAS ENTHALTEN IST IM XML:
=============================

### OpenImmo XML enthält:
- Makler-Informationen (OIB, Firma, Logo)
- Immobilien-Details (Titel, Beschreibung, Typ)
- Preis (Kauf/Miete)
- Flächen (Wohnfläche, Grundstück, Zimmer)
- Adresse (Straße, Stadt, PLZ, Land: Kroatien)
- Kontaktperson
- Alle Fotos mit URLs
- Video-URL
- Standard-konform für Import in Immobilien-Portale

### Einfaches XML enthält:
- Alle Immobilien-Daten in übersichtlichem Format
- Leichter zu lesen
- Einfach anzupassen


## URLs FÜR IHRE MAKLER:
=========================

Nach der Installation können Ihre Makler diese URLs verwenden:

**Live-System (nach Deployment):**
https://IhreDomain.com/api/listings/xml/

**Einzelner Makler (mit Filter):**
https://IhreDomain.com/api/listings/xml/?agent_id=MAKLER_ID

**Nur Verkaufs-Immobilien:**
https://IhreDomain.com/api/listings/xml/?property_status=For Sale

**Nur Miet-Immobilien:**
https://IhreDomain.com/api/listings/xml/?property_status=For Rent


## HÄUFIGE FRAGEN:
===================

**Q: Wie oft wird das XML aktualisiert?**
A: Automatisch! Jedes Mal wenn jemand die URL aufruft, werden die aktuellen Daten exportiert.

**Q: Kann ich das XML-Format anpassen?**
A: Ja! Bearbeiten Sie einfach die Datei `listings/xml_export.py`

**Q: Werden nur veröffentlichte Immobilien exportiert?**
A: Ja, nur Immobilien mit `is_published=True`

**Q: Sind die Bilder enthalten?**
A: Ja, als URLs zu den Bildern auf Ihrem Server

**Q: Funktioniert es mit allen Sprachen?**
A: Ja! Die Immobilien-Daten werden in der jeweiligen Sprache exportiert


## SUPPORT:
============

Bei Fragen oder Problemen:
- Prüfen Sie die Django-Logs: `python manage.py runserver`
- Testen Sie die URL im Browser
- Prüfen Sie, ob Immobilien mit `is_published=True` existieren


## FERTIG! 🎉
==============

Ihre XML-Schnittstelle ist einsatzbereit!

Makler können jetzt:
✅ Ihre Immobilien als XML exportieren
✅ In andere Portale importieren
✅ Automatische Updates erhalten
