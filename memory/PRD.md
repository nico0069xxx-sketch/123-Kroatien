# 123-KROATIEN.EU - AGENT BRIEFING

## 🔒 BASELINE & WORKFLOW
- **BASELINE:** 7cf4ec0 on main
- **WORKFLOW:** Branch-only (feature/*, fix/*)
- **GITHUB:** Canonical history (Source of Truth)
- **TIME MACHINE:** Parallel backup (recovery only, NEVER merge from iCloud)

## 👤 USER CONTEXT
- **Name:** Nik (bitte duzen, Deutsch sprechen)
- **System:** Apple Mac M1, Terminal, Safari
- **Skill-Level:** Laie - JEDEN Befehl einzeln und kopierbar geben
- **Server-Neustart:** IMMER explizit sagen wann nötig: python3 manage.py runserver

## 🏗️ PROJEKT-ARCHITEKTUR
- **Django Monolith** (KEIN React/Vue Frontend)
- **Datenbank:** SQLite (dev), PostgreSQL (prod)
- **12 Sprachen:** ge, en, hr, fr, nl, pl, cz, sk, ru, gr, sw, no

### Sprach-Slugs (WICHTIG!)
| Code | Sprache | Land-Slug |
|------|---------|-----------|
| ge | Deutsch | kroatien |
| en | English | croatia |
| hr | Hrvatski | hrvatska |
| fr | Français | croatie |
| nl | Nederlands | kroatie |
| pl | Polski | chorwacja |
| cz | Čeština | chorvatsko |
| sk | Slovenčina | chorvatsko |
| ru | Русский | horvatiya |
| gr | Ελληνικά | kroatia |
| sw | Svenska | kroatien |
| no | Norsk | kroatia |

### ⚠️ KRITISCHE ARCHITEKTUR-REGELN

#### 1. URL-Architektur
- **Statische Seiten** (sitemap, imprint, agb, etc.) werden DIREKT in `realstate/urls.py` definiert (AUSSERHALB von i18n_patterns)
- **Dynamische Seiten** nutzen i18n_patterns am Ende von `realstate/urls.py`
- Bei URL-Änderungen IMMER in `realstate/urls.py` UND `main/urls.py` prüfen
- **Reihenfolge wichtig:** Spezifische URLs VOR generischen `<str:category>/` Routes!

#### 2. Sprache in Views KORREKT setzen
Wenn Views außerhalb von i18n_patterns definiert sind, MUSS die Sprache manuell gesetzt werden.

#### 3. Übersetzungen in Templates
- Bei Template-Übersetzungen IMMER alle 12 Sprachen prüfen
- `{{ language }}` Variable kommt aus `main/context_processors.py`

#### 4. JavaScript API-Aufrufe
- NIEMALS hardcoded `/ge/api/...` verwenden!
- IMMER `{{ language }}` Template-Variable nutzen

#### 5. Dienstleister-Bereich
- Registrierung, Makler-Portal nur für DE und HR verfügbar

## 📁 WICHTIGE DATEIEN
- `realstate/urls.py` - Haupt-URL-Routing
- `main/urls.py` - App-URLs
- `main/context_processors.py` - Globale Template-Variablen
- `listings/image_utils.py` - Automatische Bildkomprimierung (WebP)
- `main/xml_import.py` - XML-Import mit Bild-Download (OpenImmo + Simple)
- `main/chatbot.py` - KI-Chatbot mit Glossar-Integration

## 🖼️ BILDKOMPRIMIERUNG (Januar 2026)
- **Automatisch bei Upload:** Alle ImageFields in Listing, Agent, Professional, Realtor
- **Format:** WebP | **Max:** 1920x1080px | **Qualität:** 82%
- **XML-Import:** Bilder werden heruntergeladen UND komprimiert

## 🤖 GEO (Generative Engine Optimization)
- `llms.txt` - AI-Crawler Dokumentation (12 Sprachen)
- FAQ Schema, HowTo Schema, Glossar Schema implementiert
- 39 Glossar-Begriffe fließen in Chatbot-Antworten ein

## ✅ START CHECKLISTE

## 🚫 VERBOTEN
- Niemals direkt auf main arbeiten
- Niemals .env, db.sqlite3, media/ committen
- Niemals hardcoded /ge/ in JavaScript fetch() verwenden

## 📋 OFFENE PUNKTE

### P1 (Hoch)
- XML-Import mit echtem Makler-Feed testen

### P2 (Mittel)
- Glossar erweitern
- Fragile Django Migrations
- Automatische Sitemap-Aktualisierung

### P3 (Niedrig)
- base.html Schema mehrsprachig machen
