# 123-Kroatien.eu - Feature-Dokumentation

## Übersicht
123-Kroatien.eu ist ein mehrsprachiger Immobilienmarktplatz für Kroatien mit Fokus auf deutsche und internationale Käufer.

---

## 1. IMMOBILIEN-SYSTEM

### 1.1 Listings (Immobilienanzeigen)
**Dateien:** `listings/models.py`, `listings/views.py`, `main/views.py`

- **Immobilien erstellen/bearbeiten:** `/add-property/`, `/edit-property/<id>/`
- **Immobiliendetails:** `/property-details/<id>/`
- **Immobilienliste:** `/listing/`

**Felder:**
- Grunddaten: Titel, Beschreibung, Typ, Status, Standort
- Details: Schlafzimmer, Badezimmer, Etagen, Garage, Fläche, Größe
- Preis und ID
- Bilder: Hauptbild + 6 zusätzliche Fotos
- Adresse: Land, Stadt, Bundesland, PLZ, Nachbarschaft
- **12 Sprachversionen** der Beschreibung (DE, EN, FR, HR, PL, CZ, RU, GR, SW, NO, SK, NL)

### 1.2 AI-Übersetzung für Listings
**Datei:** `listings/ai_content_generator.py`

- Automatische Übersetzung von Immobilienbeschreibungen in 12 Sprachen
- Nutzt OpenAI GPT-4o via Emergent Integration

---

## 2. BENUTZER-SYSTEM

### 2.1 Gruppe A - Makler & Bauunternehmen (Agent/Professional)
**Dateien:** `accounts/models.py`, `main/professional_models.py`

**Können:**
- Immobilien einstellen und verwalten
- Öffentliches Profil haben
- Referenzprojekte präsentieren

**Profil-Verwaltung:** `/edit-agent/<id>/`
- Grunddaten (Name, Kontakt, Standort)
- Firmendetails (Slogan, Gründungsjahr, Mitarbeiter, Spezialisierungen)
- Social Media Links (Facebook, Instagram, LinkedIn, YouTube, Twitter, TikTok)
- **Toggle-Schalter:** Referenzen, Kontaktformular, Immobilien, Social Media anzeigen/verstecken

### 2.2 Gruppe B - Dienstleister (Professional Portal)
**Dateien:** `main/professional_portal_views.py`, `main/professional_models.py`

**Typen:**
- Rechtsanwälte (`lawyer`)
- Steuerberater (`tax_advisor`)
- Architekten (`architect`)

**Portal:** `/portal/dashboard/`
- Eigenes Dashboard
- 2FA-Authentifizierung (TOTP oder E-Mail)
- Profilbearbeitung

### 2.3 Referenzprojekte (NEU)
**Datei:** `main/professional_models.py` → `ReferenceProject`

**URLs:**
- Liste: `/agent/<id>/referenzen/`
- Erstellen: `/agent/<id>/referenzen/neu/`
- Bearbeiten: `/agent/<id>/referenzen/<project_id>/bearbeiten/`
- Löschen: `/agent/<id>/referenzen/<project_id>/loeschen/`

**Felder:**
- Titel, Beschreibung, Jahr, Standort, Projektart
- Bis zu 6 Bilder pro Projekt
- Sortierreihenfolge, Hervorgehoben-Status

---

## 3. MEHRSPRACHIGKEIT (12 Sprachen)

### 3.1 Unterstützte Sprachen
| Code | Sprache | URL-Präfix |
|------|---------|------------|
| ge | Deutsch | /ge/ |
| en | Englisch | /en/ |
| hr | Kroatisch | /hr/ |
| fr | Französisch | /fr/ |
| nl | Niederländisch | /nl/ |
| pl | Polnisch | /pl/ |
| cz | Tschechisch | /cz/ |
| sk | Slowakisch | /sk/ |
| ru | Russisch | /ru/ |
| gr | Griechisch | /gr/ |
| sw | Schwedisch | /sw/ |
| no | Norwegisch | /no/ |

### 3.2 Übersetzungssystem
**Dateien:** `pages/models.py` → `Translation`, `main/context_processors.py`

- 324 UI-Übersetzungen in der Datenbank
- Automatisches Laden via Context Processor `get_my_translations`
- Sprache wird per Session und URL erkannt

---

## 4. DIENSTLEISTER-VERZEICHNIS

### 4.1 Kategorien (5 Typen)
**Datei:** `main/professional_views.py`

| Typ | DE URL | HR URL |
|-----|--------|--------|
| Immobilienmakler | /ge/kroatien/immobilienmakler/ | /hr/hrvatska/agencije-za-nekretnine/ |
| Bauunternehmen | /ge/kroatien/bauunternehmen/ | /hr/hrvatska/gradevinske-tvrtke/ |
| Rechtsanwälte | /ge/kroatien/rechtsanwaelte/ | /hr/hrvatska/odvjetnici/ |
| Steuerberater | /ge/kroatien/steuerberater/ | /hr/hrvatska/porezni-savjetnici/ |
| Architekten | /ge/kroatien/architekten/ | /hr/hrvatska/arhitekti/ |

### 4.2 AI-generierte Profile
**Datei:** `main/ai_content_generator.py`

- Automatische Profilbeschreibungen in 12 Sprachen
- Generiert: Zusammenfassung, Tätigkeitsbereiche, Arbeitsweise, SEO-Meta-Daten
- Nutzt OpenAI GPT-4o

---

## 5. AUTHENTIFIZIERUNG & SICHERHEIT

### 5.1 Login & Registrierung
**Datei:** `accounts/views.py`

- Standard Django-Authentifizierung
- OTP-Verifizierung bei Registrierung
- Brute-Force-Schutz (5 Versuche, 5 Min Sperre)

### 5.2 Zwei-Faktor-Authentifizierung (2FA)
**Dateien:** `main/professional_models.py`, `main/professional_portal_views.py`

**Methoden:**
1. **TOTP (Authenticator-App):** Google Authenticator, Authy, etc.
2. **E-Mail-Code:** 6-stelliger Code per E-Mail

### 5.3 Admin-Bereich
- URL: `/nik-verwaltung-2026/` (obfuskiert)
- Vollzugriff auf alle Daten

---

## 6. KONTAKT & ANFRAGEN

### 6.1 Kontaktformulare
**Datei:** `main/views.py`

- Allgemeines Kontaktformular: `/contact/`
- Eigentümer-Formular: `/owner-form/`
- Immobilien-Anfrage: `/send-email/`

### 6.2 E-Mail-Benachrichtigungen
- Bei neuen Anfragen
- Bei Registrierungen
- Nutzt SMTP (Ethereal für Tests)

---

## 7. STATISCHE SEITEN

| Seite | URL |
|-------|-----|
| Startseite | / |
| Über uns | /about/ |
| Blog | /blog/ |
| FAQ | /faq/ |
| Impressum | /imprint/ |
| Datenschutz | /data-protection/ |
| AGB | /agb/ |
| Widerrufsbelehrung | /cancellation-policy/ |
| Sitemap | /sitemap/ |

---

## 8. XML-SCHNITTSTELLEN (GEPLANT)

### 8.1 OpenImmo Import
**Status:** Noch nicht implementiert

**Geplante Funktion:**
- Import von Immobilien im OpenImmo-XML-Format
- Automatische Zuordnung zu Maklern
- Synchronisation mit externen Systemen

### 8.2 WordPress XML Import
**Status:** Noch nicht implementiert

**Geplante Funktion:**
- Import von Immobilien aus WordPress-Seiten kroatischer Makler
- Unterstützung für gängige WordPress-Immobilien-Plugins
- Periodische Aktualisierung

---

## 9. TECHNISCHE DETAILS

### 9.1 Tech Stack
- **Backend:** Django 4.2
- **Datenbank:** SQLite (Entwicklung) / PostgreSQL (Produktion)
- **Frontend:** Bootstrap 4, jQuery
- **AI:** OpenAI GPT-4o via Emergent Integration

### 9.2 Wichtige Dateien
```
realstate/
├── accounts/          # Benutzer-Authentifizierung
├── listings/          # Immobilien-System
├── main/              # Hauptanwendung
│   ├── views.py       # Haupt-Views
│   ├── professional_views.py    # Dienstleister-Verzeichnis
│   ├── professional_models.py   # Professional & ReferenceProject
│   ├── ai_content_generator.py  # AI-Profilgenerierung
│   └── context_processors.py    # Übersetzungen
├── pages/             # Statische Seiten & Übersetzungen
├── templates/         # HTML-Templates
└── static/            # CSS, JS, Bilder
```

### 9.3 Umgebungsvariablen
```
SECRET_KEY=...
DEBUG=True/False
ALLOWED_HOSTS=...
DATABASE_URL=...
EMAIL_HOST=...
OPENAI_API_KEY=... (via Emergent)
```

---

## 10. NÄCHSTE SCHRITTE

### Hohe Priorität
1. [ ] OpenImmo XML-Import implementieren
2. [ ] WordPress XML-Import implementieren
3. [ ] Agent-Model Konsolidierung (accounts.Agent → main.Professional)

### Mittlere Priorität
4. [ ] Kundenbewertungs-System
5. [ ] 2FA-Logik Refactoring (Deduplizierung)

### Niedrige Priorität
6. [ ] CSS-Refactoring (Font Awesome Stabilität)
7. [ ] get_my_translations Refactoring

---

*Letzte Aktualisierung: Januar 2026*
