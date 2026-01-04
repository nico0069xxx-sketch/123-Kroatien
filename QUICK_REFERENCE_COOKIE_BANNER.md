# ====================================
# QUICK REFERENCE: DATENSCHUTZBANNER
# Kurz-Anleitung für schnelle Installation
# ====================================

## 🚀 IN 3 SCHRITTEN INSTALLIERT:

### 1️⃣ DATEIEN KOPIEREN
```
Kopieren nach:
├── static/js/cookie_consent_translations.js
├── static/js/cookie_consent.js
└── static/css/cookie_consent.css
```

### 2️⃣ IN BASE.HTML EINFÜGEN
```html
{% load static %}

<!-- VOR </body> Tag einfügen: -->
<link rel="stylesheet" href="{% static 'css/cookie_consent.css' %}">
<script src="{% static 'js/cookie_consent_translations.js' %}"></script>
<script src="{% static 'js/cookie_consent.js' %}"></script>

<script>
(function() {
    const lang = '{{ request.session.site_language|default:"hr" }}';
    setTimeout(() => {
        if (window.cookieConsent) window.cookieConsent.changeLanguage(lang);
    }, 100);
})();
</script>
```

### 3️⃣ TESTEN
```bash
# Server neu starten
python manage.py runserver

# Browser öffnen
http://localhost:8000/

# Banner sollte erscheinen! 🎉
```

## ✅ CHECKLISTE:

- [ ] 3 Dateien in static/ kopiert
- [ ] Code in base.html eingefügt
- [ ] {% load static %} vorhanden
- [ ] Server neu gestartet
- [ ] Banner erscheint
- [ ] Buttons funktionieren
- [ ] Sprache korrekt

## 🌐 12 SPRACHEN:

hr (Kroatisch) | ge (Deutsch) | en (Englisch)
fr (Französisch) | gr (Griechisch) | pl (Polnisch)
cz (Tschechisch) | ru (Russisch) | sw (Schwedisch)
no (Norwegisch) | sk (Slowakisch) | nl (Niederländisch)

## 🐛 FEHLER BEHEBEN:

**Banner erscheint nicht?**
→ F12 → Console → Fehler prüfen
→ Reihenfolge: translations.js VOR consent.js!

**Falsche Sprache?**
→ Prüfen: {{ request.session.site_language }}
→ Standard: 'hr' (Kroatisch)

**Styling kaputt?**
→ Cache leeren (Strg+F5)
→ collectstatic ausführen

## 🔧 ANPASSEN:

**Datenschutz-Link ändern:**
```javascript
// In cookie_consent.js, Zeile ~186:
<a href="/IHRE-URL/" target="_blank">
```

**Farben ändern:**
```css
/* In cookie_consent.css: */
#4CAF50 → Ihre Farbe
```

## 🧪 TESTEN:

**Einstellungen löschen:**
```javascript
// Browser-Konsole (F12):
localStorage.removeItem('cookie_consent');
location.reload();
```

**Sprache manuell ändern:**
```javascript
// Browser-Konsole (F12):
window.cookieConsent.changeLanguage('ge'); // Deutsch
window.cookieConsent.changeLanguage('en'); // Englisch
```

## 📱 FEATURES:

✅ GDPR-konform
✅ 3 Cookie-Kategorien
✅ LocalStorage (kein Cookie!)
✅ Responsive Design
✅ 🍪 Einstellungs-Button
✅ Automatische Spracherkennung

## 💡 FERTIG!

Banner ist einsatzbereit!
Alle Details: INSTALLATIONS_ANLEITUNG_COOKIE_BANNER.md
