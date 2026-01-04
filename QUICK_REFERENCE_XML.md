# ====================================
# QUICK REFERENCE: XML-SCHNITTSTELLE
# Kurz-Anleitung für schnelle Installation
# ====================================

## 🚀 IN 3 SCHRITTEN INSTALLIERT:

### 1️⃣ DATEI ERSTELLEN
```
Pfad: listings/xml_export.py
Inhalt: Kopieren Sie ALLES aus django_xml_export.py
```

### 2️⃣ VIEWS HINZUFÜGEN
```
Datei öffnen: listings/views.py

Oben bei den Imports hinzufügen:
    from .xml_export import OpenImmoXMLGenerator, SimpleXMLGenerator
    from django.http import HttpResponse

Unten am Ende hinzufügen:
    (Kopieren Sie den Inhalt aus django_xml_views.py)
```

### 3️⃣ URLS KONFIGURIEREN
```
Datei öffnen: realstate/urls.py

Bei den Imports hinzufügen:
    from listings.views import listings_xml_openimmo, listings_xml_simple

In urlpatterns hinzufügen:
    path('api/listings/xml/', listings_xml_openimmo, name='listings_xml_openimmo'),
    path('api/listings/simple-xml/', listings_xml_simple, name='listings_xml_simple'),
```

## ✅ TESTEN:
```
1. Server neu starten:
   python manage.py runserver

2. Browser öffnen:
   http://localhost:8000/api/listings/xml/

3. XML sollte angezeigt werden! 🎉
```

## 📝 HÄUFIGSTE FEHLER:

**Fehler: "ModuleNotFoundError: No module named 'xml_export'"**
→ Lösung: Prüfen Sie, ob xml_export.py im richtigen Ordner ist (listings/)

**Fehler: "NameError: name 'OpenImmoXMLGenerator' is not defined"**
→ Lösung: Import in views.py vergessen? Prüfen Sie die Imports!

**Fehler: 404 Page Not Found**
→ Lösung: URLs nicht richtig konfiguriert? Prüfen Sie realstate/urls.py

**Leeres XML oder keine Daten**
→ Lösung: Haben Sie Immobilien mit is_published=True in der Datenbank?

## 🌐 LIVE-URLS (nach Deployment):

Geben Sie Ihren Maklern diese URLs:

```
OpenImmo (Standard):
https://123-kroatien.eu/api/listings/xml/

Einzelner Makler:
https://123-kroatien.eu/api/listings/xml/?agent_id=MAKLER_ID

Nur Verkauf:
https://123-kroatien.eu/api/listings/xml/?property_status=For Sale
```

## 💬 FRAGEN?

Siehe: INSTALLATIONS_ANLEITUNG_XML.md (ausführlich)
Siehe: XML_BEISPIELE.md (wie sieht es aus?)
