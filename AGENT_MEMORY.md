# Agent Memory - 123-Kroatien.eu

**Letzte Aktualisierung:** 15. Januar 2026
**Benutzer:** Nik (Laie, Apple M1 Mac, Safari, Terminal/zsh)
**Sprache:** Deutsch (informelles "du")

---

## Implementierte Sicherheitsmaßnahmen (15.01.2026)

### 1. SECRET_KEY Absicherung
- **Datei:** `.env`
- **Änderung:** `SECRET_KEY` aus Umgebungsvariable laden
- **Code in settings.py:** `SECRET_KEY = os.environ.get('SECRET_KEY', 'fallback-nur-fuer-entwicklung')`

### 2. DEBUG & ALLOWED_HOSTS
- **Datei:** `.env` und `realstate/settings.py`
- **DEBUG:** `os.environ.get('DEBUG', 'False').lower() == 'true'`
- **ALLOWED_HOSTS:** `os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')`

### 3. Login Brute-Force-Schutz
- **Datei:** `accounts/views.py`
- **Cache:** `_login_attempts = {}`
- **Konstanten:** `MAX_LOGIN_ATTEMPTS = 5`, `LOCKOUT_TIME = 300`
- **Logik:** Nach 5 Fehlversuchen 5 Minuten Sperre pro IP+Username

### 4. Passwort-Mindestlänge
- **Datei:** `accounts/views.py`
- **Änderung:** `if len(password) < 10:` (vorher 6)

### 5. Anfrage-Formular Sicherheit
- **Datei:** `main/views.py` (Funktion: `send_listing_inquiry`)
- **Rate Limiting:** `_inquiry_cache = {}`, max 3 Anfragen/Minute
- **Input-Validierung:** Länge begrenzt, E-Mail-Format geprüft
- **Honeypot:** Verstecktes Feld in `templates/main/single-detail.html`

### 6. File-Upload Validierung
- **Datei:** `main/views.py`
- **Funktionen:** `validate_image_upload()`, `validate_document_upload()`
- **Limits:** Bilder max 5MB, Dokumente max 10MB
- **Typen:** JPEG/PNG/WebP für Bilder, PDF für Dokumente

### 7. Security Headers
- **Datei:** `realstate/settings.py` (am Ende)
- **Headers:** X_FRAME_OPTIONS, SECURE_BROWSER_XSS_FILTER, etc.

### 8. Admin-URL versteckt
- **Datei:** `realstate/urls.py`
- **Neue URL:** `/nik-verwaltung-2026/` (NICHT `/admin/`)

---

## Implementierte Features (15.01.2026)

### E-Mail-Benachrichtigung bei Anfragen
- **Datei:** `main/views.py` (Funktion: `send_listing_inquiry`)
- **URL:** `/api/listing-inquiry/`
- **Template:** `templates/main/single-detail.html` (Formular + JavaScript)
- **Funktion:** Kunde füllt Formular aus → Makler bekommt E-Mail

---

## Wichtige Dateien

| Datei | Zweck |
|-------|-------|
| `.env` | Umgebungsvariablen (SECRET_KEY, DEBUG, etc.) |
| `realstate/settings.py` | Django-Einstellungen, Security Headers |
| `accounts/views.py` | Login mit Brute-Force-Schutz |
| `main/views.py` | Anfrage-Formular, Upload-Validierung |
| `realstate/urls.py` | URL-Routing (Admin versteckt) |

---

## Credentials (nur für Entwicklung!)

- **Admin:** `/nik-verwaltung-2026/` - User: `Nik`, PW: `Admin1234!`
- **Ethereal Email:** `sasha.hilll87@ethereal.email` / `exVSXSneKTbU88mxHa`
- **Test-Makler:** `testmakler2` / `Test1234!`
- **Test-Architekt:** `testarchitekt` / `Test1234!`

---

## Offene Tasks

- [ ] 2FA-Anleitung auf Auswahlseite
- [ ] Sensible URL-Slugs umbenennen
- [ ] HTTPS erzwingen (Produktion)
- [ ] Logging für fehlgeschlagene Logins
- [ ] Referenzen/Projekte Bildergalerie
- [ ] Kundenbewertungen/Rating-System

---

## Hinweise für nächsten Agent

1. **Benutzer ist Laie** - Immer einfache, kopierbare Befehle geben
2. **Lokale Entwicklung** - Pfad: `~/Desktop/real-estate-django-ALTmain`
3. **E-Mail ist gemockt** - Ethereal.email nutzen zum Testen
4. **Admin-URL geheim halten** - Nicht in Nutzer-Dokumentation erwähnen

---

## URL-Mapping (Sicherheit - 15.01.2026)

| Alte URL | Neue URL | Zweck |
|----------|----------|-------|
| `/api/xml/openimmo/` | `/api/x1/export/` | XML Export |
| `/api/xml/croatia/` | `/api/x2/export/` | XML Export |
| `/api/chatbot/` | `/api/k-assist/` | KI Chatbot |
| `/api/smart-search/` | `/api/suche-v2/` | KI Suche |
| `/api/validate-oib/` | `/api/prv/oib/` | OIB Validierung |
| `/api/check-spelling/` | `/api/txt/sp/` | Rechtschreibung |
| `/api/improve-text/` | `/api/txt/opt/` | Text verbessern |
| `/api/regenerate-suggestions/` | `/api/txt/regen/` | Vorschläge |
| `/api/makler/ki-beschreibung/` | `/api/m/gen/` | KI Beschreibung |
| `/api/experten-matching/` | `/api/em/` | Experten-Matching |
| `/api/makler/verkauft/` | `/api/m/v/` | Objekt verkauft |
| `/api/makler/pausieren/` | `/api/m/p/` | Objekt pausieren |
| `/api/makler/aktivieren/` | `/api/m/a/` | Objekt aktivieren |
| `/admin/` | `/nik-verwaltung-2026/` | Admin-Bereich |

**WICHTIG:** Bei neuen Features immer die neuen URL-Pfade verwenden!
