# ============================================
# INSTALLATIONS-ANLEITUNG: DATENSCHUTZBANNER
# Cookie Consent Banner für alle 12 Sprachen
# ============================================

## ✅ WAS WURDE ENTWICKELT:
===========================

✅ GDPR-konformes Cookie-Consent-Banner
✅ Alle 12 Sprachen (Kroatisch, Deutsch, Englisch, Französisch, Griechisch, Polnisch, Tschechisch, Russisch, Schwedisch, Norwegisch, Slowakisch, Niederländisch)
✅ 3 Cookie-Kategorien: Notwendig, Analytik, Marketing
✅ "Alle akzeptieren" / "Alle ablehnen" / "Anpassen"
✅ Einstellungen in LocalStorage gespeichert
✅ Einstellungs-Button zum erneuten Öffnen (🍪)
✅ Responsive Design (Desktop & Mobile)
✅ Automatische Sprach-Synchronisation mit Django


## 📦 DATEIEN, DIE SIE ERHALTEN HABEN:
======================================

1. **cookie_consent_translations.js** - Übersetzungen für alle 12 Sprachen
2. **cookie_consent.css** - Styling (responsive)
3. **cookie_consent.js** - JavaScript Logik
4. **cookie_consent_template.html** - Integration-Beispiel


## 🎯 SCHRITT-FÜR-SCHRITT-ANLEITUNG:
=====================================

### SCHRITT 1: Dateien in Ihr Projekt kopieren
-----------------------------------------------

1. **JavaScript-Dateien:**
   - Erstellen Sie (falls nicht vorhanden): `static/js/`
   - Kopieren Sie `cookie_consent_translations.js` nach: `static/js/cookie_consent_translations.js`
   - Kopieren Sie `cookie_consent.js` nach: `static/js/cookie_consent.js`

2. **CSS-Datei:**
   - Erstellen Sie (falls nicht vorhanden): `static/css/`
   - Kopieren Sie `cookie_consent.css` nach: `static/css/cookie_consent.css`


### SCHRITT 2: In Base-Template integrieren
--------------------------------------------

1. Öffnen Sie Ihre Haupt-Template-Datei:
   - `templates/base.html` oder
   - `templates/main/base.html` oder
   - Eine andere Template-Datei, die auf ALLEN Seiten geladen wird

2. Fügen Sie VOR dem schließenden `</body>`-Tag folgendes ein:

```html
<!-- Cookie Consent Banner -->
<link rel="stylesheet" href="{% static 'css/cookie_consent.css' %}">
<script src="{% static 'js/cookie_consent_translations.js' %}"></script>
<script src="{% static 'js/cookie_consent.js' %}"></script>

<!-- Sprach-Synchronisation -->
<script>
    (function() {
        const djangoLanguage = '{{ request.session.site_language|default:"hr" }}';
        setTimeout(() => {
            if (window.cookieConsent && djangoLanguage) {
                window.cookieConsent.changeLanguage(djangoLanguage);
            }
        }, 100);
    })();
</script>
```

3. Stellen Sie sicher, dass `{% load static %}` ganz oben in der Datei steht:

```html
{% load static %}
<!DOCTYPE html>
<html>
...
```


### SCHRITT 3: Static Files sammeln (für Produktion)
-----------------------------------------------------

Führen Sie folgenden Befehl aus:

```bash
python manage.py collectstatic
```

(Nur notwendig wenn Sie in Produktion sind oder DEBUG=False haben)


### SCHRITT 4: Testen
----------------------

1. **Server neu starten:**
   ```bash
   python manage.py runserver
   ```

2. **Browser öffnen:**
   - Gehen Sie zu Ihrer Website: `http://localhost:8000/`

3. **Sie sollten sehen:**
   - ✅ Cookie-Banner erscheint unten auf der Seite
   - ✅ In der richtigen Sprache (basierend auf Django Session)
   - ✅ Buttons funktionieren ("Alle akzeptieren", "Alle ablehnen", "Anpassen")

4. **Nach dem Akzeptieren:**
   - ✅ Banner verschwindet
   - ✅ Cookie-Button (🍪) erscheint unten links
   - ✅ Klick auf Button öffnet Banner erneut

5. **Sprache testen:**
   - Wechseln Sie die Sprache auf Ihrer Website
   - Cookie-Banner sollte automatisch die Sprache wechseln


## 🌐 UNTERSTÜTZTE SPRACHEN:
=============================

1. **hr** - Kroatisch (Hauptsprache)
2. **ge** - Deutsch
3. **en** - Englisch
4. **fr** - Französisch
5. **gr** - Griechisch
6. **pl** - Polnisch
7. **cz** - Tschechisch
8. **ru** - Russisch
9. **sw** - Schwedisch
10. **no** - Norwegisch
11. **sk** - Slowakisch
12. **nl** - Niederländisch


## ⚙️ FUNKTIONSWEISE:
======================

### Cookie-Kategorien:

1. **Notwendige Cookies** (Immer aktiv)
   - Django Session Cookie
   - CSRF Token
   - Sprachauswahl
   - Login-Status

2. **Analytik Cookies** (Optional)
   - Google Analytics
   - Matomo
   - Eigene Analytics

3. **Marketing Cookies** (Optional)
   - Facebook Pixel
   - Google Ads
   - Andere Werbe-Tracker


### Speicherung:

- Einstellungen werden in **LocalStorage** gespeichert
- Schlüssel: `cookie_consent`
- Format: JSON mit Zeitstempel
- Beispiel:
  ```json
  {
    "necessary": true,
    "analytics": true,
    "marketing": false,
    "timestamp": "2025-01-04T20:00:00.000Z"
  }
  ```


## 🔧 ANPASSUNGEN:
==================

### Link zur Datenschutzerklärung ändern:

Öffnen Sie: `cookie_consent.js`

Suchen Sie (ca. Zeile 186):
```javascript
<a href="/data-protection/" target="_blank">${t.privacyPolicy}</a>
```

Ändern Sie die URL zu Ihrer Datenschutz-Seite:
```javascript
<a href="/privacy/" target="_blank">${t.privacyPolicy}</a>
```


### Farben anpassen:

Öffnen Sie: `cookie_consent.css`

Suchen Sie diese Werte und ändern Sie sie:
- Grüne Farbe (Accept): `#4CAF50` → Ihre Farbe
- Hintergrund: `rgba(0, 0, 0, 0.98)` → Ihre Farbe


### Analytics integrieren (Google Analytics):

Öffnen Sie: `cookie_consent.js`

Suchen Sie die Funktion `enableAnalytics()` (ca. Zeile 308):

```javascript
enableAnalytics() {
    console.log('Analytics cookies enabled');
    
    // Google Analytics aktivieren
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'GA_MEASUREMENT_ID'); // Ihre GA ID hier!
    
    // Script laden
    const script = document.createElement('script');
    script.async = true;
    script.src = 'https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID';
    document.head.appendChild(script);
}
```


## 📱 RESPONSIVE DESIGN:
========================

Der Banner passt sich automatisch an:
- ✅ Desktop: Volle Breite, alle Buttons nebeneinander
- ✅ Tablet: Angepasste Breite, Buttons umbrechen
- ✅ Mobile: Volle Breite, Buttons untereinander


## 🔐 GDPR-KONFORMITÄT:
========================

✅ Nutzer kann frei wählen (Opt-In)
✅ Klare Kategorisierung
✅ Beschreibung jeder Kategorie
✅ Link zur Datenschutzerklärung
✅ Einstellungen können jederzeit geändert werden
✅ Keine Cookies vor Einwilligung (außer notwendige)


## 🐛 HÄUFIGE FEHLER:
=====================

**Fehler: Banner erscheint nicht**
→ Lösung: 
  - Prüfen Sie, ob die Dateien korrekt eingebunden sind
  - Öffnen Sie Browser-Konsole (F12) und schauen Sie nach Fehlern
  - Prüfen Sie, ob `{% load static %}` vorhanden ist

**Fehler: Banner ist in falscher Sprache**
→ Lösung:
  - Prüfen Sie `request.session.site_language`
  - Standard ist 'hr' (Kroatisch)
  - Sprach-Synchronisations-Script korrekt eingebunden?

**Fehler: Styling ist kaputt**
→ Lösung:
  - CSS-Datei korrekt eingebunden?
  - `python manage.py collectstatic` ausgeführt?
  - Cache leeren (Strg+F5)

**Fehler: "cookieConsentTranslations is not defined"**
→ Lösung:
  - `cookie_consent_translations.js` MUSS VOR `cookie_consent.js` geladen werden
  - Reihenfolge der Script-Tags prüfen!


## 💡 TIPPS:
=============

1. **Testen Sie alle Sprachen:**
   - Wechseln Sie die Sprache und prüfen Sie den Banner

2. **Browser-Cache:**
   - Leeren Sie den Cache nach Änderungen (Strg+F5)

3. **LocalStorage leeren:**
   - Browser-Konsole (F12) → Console → Eingeben:
     ```javascript
     localStorage.removeItem('cookie_consent');
     location.reload();
     ```

4. **Mobile testen:**
   - Browser-Entwicklertools (F12) → Geräte-Ansicht


## ✅ CHECKLISTE:
=================

- [ ] Dateien kopiert (JS und CSS)
- [ ] In base.html integriert
- [ ] {% load static %} vorhanden
- [ ] Static files gesammelt (collectstatic)
- [ ] Server neu gestartet
- [ ] Banner erscheint
- [ ] Buttons funktionieren
- [ ] Einstellungen werden gespeichert
- [ ] Cookie-Button (🍪) erscheint nach Akzeptieren
- [ ] Sprach-Wechsel funktioniert
- [ ] Responsive (Mobile getestet)


## 🎉 FERTIG!
==============

Ihr Datenschutzbanner ist einsatzbereit!

Ihre Makler und Besucher können jetzt:
✅ Ihre Cookie-Präferenzen einstellen
✅ In ihrer eigenen Sprache
✅ GDPR-konform
✅ Jederzeit Einstellungen ändern


## 📞 SUPPORT:
===============

Bei Fragen:
1. Prüfen Sie die Browser-Konsole (F12) auf Fehler
2. Testen Sie mit `localStorage.removeItem('cookie_consent')`
3. Prüfen Sie die Reihenfolge der Script-Tags
4. Leeren Sie den Browser-Cache
