# Auftrag für nächste Session - 123-Kroatien.eu

## 🎯 Ziel
Kroatische Dienstleister akquirieren (Makler, Bauunternehmer, Anwälte, Architekten, Steuerberater)

---

## 📋 Priorität 1: Dashboards strukturieren

### Gruppe A (Immobilien/Bau):
- Eigene Immobilien-Anzeigen verwalten (XML/OpenImmo, erstellen, bearbeiten, löschen)
- Anfragen von Interessenten sehen
- Profil/Firmendaten bearbeiten

### Gruppe B (Rechtsanwälte, Architekten, Steuerberater):
- Dienstleistungen verwalten
- Profil/Firmendaten bearbeiten

### Anforderungen:
- Logisch und einfach für Laien aufbauen
- Grafisch leicht verständlich
- Übersicht-Seite mit: Anzahl aktiver Anzeigen/Dienste, Profil-Vollständigkeit, Schnellzugriff-Buttons

---

## 📋 Priorität 2: Anleitung erstellen

### Reihenfolge:
1. 🇩🇪 **Deutsch** (zuerst - User muss prüfen können)
2. 🇭🇷 **Kroatisch** (Zielgruppe)
3. 🇬🇧 **Englisch** (international)

### Format:
- Als Hilfe-Seite im Dashboard
- Als PDF-Download
- Für jeden Menüpunkt eine Erklärung

---

## 📊 Feature-Status (Stand 18.01.2026)

### ✅ Implementiert:
- Django Apps: accounts, listings, main, contacts, pages, realtors
- Professional Model (5 Typen)
- AI Beschreibungen (OpenAI GPT-4o)
- 12 Sprachen (manuell)
- Dashboards (Basis vorhanden)
- 2FA Login

### ❌ Nicht implementiert:
- Celery + Redis
- Newsletter/Subscriber System
- Review/Bewertungs-System
- Events & Webinare
- Meta Pixel / Tracking
- ML Preisanalyse
- Personalisierte Empfehlungen

---

## ⚠️ Wichtige Regeln

### Git Workflow:
- BASELINE: 9ec9d9a auf main - NICHT BRECHEN
- Nur auf feature/* oder fix/* Branches arbeiten
- Niemals direkt auf main

### User-Kontext:
- Laie auf Apple Mac M1
- Braucht exakte Terminal-Befehle Schritt für Schritt
- Kein Kroatisch - daher zuerst Deutsch

### Dashboard URLs:
- Makler-Dashboard: /makler-dashboard/
- Login: /makler-portal/login/
- Admin: /nik-verwaltung-2026/ (User: Nik, PW: Admin1234!)

---

## 🔧 CSS-Probleme - WICHTIG!

### ⚠️ Status VOR dieser Session (18.01.2026):
Die Webseite war FUNKTIONSFÄHIG und sah KORREKT aus! Folgende Features waren implementiert und funktionierten:

- ✅ Hero-Slider mit Textschatten und Overlay (Commit c5a5fb6)
- ✅ Hover-Effekte auf Cards (Commit 089e4e1)
- ✅ Scroll-Animationen (Commit 089e4e1)
- ✅ Desktop Navigation - blauer Hintergrund (Commit 21c87e1)
- ✅ Registrieren-Button entfernt (Commit 21c87e1)
- ✅ Partner-Carousel dynamisch (Commit fc523e8)

### ❌ Problem WÄHREND dieser Session:
Trotz gleicher Commit-Historie (fc523e8) zeigt die Webseite diese Probleme:
- Navigation: Weiß statt dunkelblau
- Registrieren-Button: Wieder sichtbar
- Footer: Falsche Hintergrundfarbe
- Schriftarten: Inkonsistent
- Hover-Effekte: Teilweise nicht sichtbar

### 🔍 Mögliche Ursachen:
1. Browser-Cache (wurde bereits geleert - hat nicht geholfen)
2. CSS-Datei wird falsch ausgeliefert
3. CSS-Spezifität: Andere Stylesheets überschreiben modern-theme.css
4. Django collectstatic Problem

### 📁 Relevante Dateien:
- `static/css/modern-theme.css` - Hauptdatei für neue Styles
- `static/css/custom.css` - Kann Konflikte verursachen
- `static/css/styles.css` - Ursprüngliches Template CSS
- `templates/include/base.html` - Lädt alle CSS-Dateien
- `templates/main/home.html` - Hat inline Styles für Hero

### 🛠️ Empfohlene Debugging-Schritte:
1. Prüfen welche CSS-Datei tatsächlich ausgeliefert wird:
   `curl -s http://127.0.0.1:8000/static/css/modern-theme.css | tail -50`

2. Prüfen ob collectstatic nötig ist:
   `python3 manage.py collectstatic --noinput`

3. CSS-Reihenfolge in base.html prüfen (modern-theme.css muss ZULETZT geladen werden)

4. Browser Developer Tools: Welche CSS-Regeln überschreiben die Navigation?

### 📌 Commits die funktioniert haben (zur Referenz):
- `21c87e1` - Fix: Desktop Navigation - blauer Hintergrund und Registrieren-Button entfernt
- `089e4e1` - feat: Hover-Effekte auf Cards und Scroll-Animationen hinzugefuegt
- `c5a5fb6` - feat: Neuer Hero-Slider mit Textschatten und Overlay
- `fc523e8` - feat: Dynamisches Partner-Carousel mit verifizierten Dienstleistern

---

Erstellt: 18.01.2026

---

## 🚨 HÖCHSTE PRIORITÄT: CSS-PROBLEM LÖSEN

**Das CSS-Problem muss ZUERST behoben werden, bevor andere Arbeiten beginnen!**

Die Webseite sieht aktuell falsch aus, obwohl der Code laut Git-History korrekt sein sollte. Ohne funktionierendes CSS macht es keinen Sinn, Dashboards zu strukturieren oder Anleitungen zu erstellen.

### Reihenfolge:
1. 🔴 **ZUERST:** CSS-Problem lösen (Navigation, Footer, Hover-Effekte)
2. 🟡 **DANN:** Dashboards strukturieren
3. 🟢 **DANACH:** Anleitungen erstellen

