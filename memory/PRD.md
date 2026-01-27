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

---

## SPRACH-SYSTEM (12 Sprachen)

### Sprach-Codes & Laender-Slugs
| Code | Sprache | Land-Slug (URL) |
|------|---------|-----------------|
| ge | Deutsch | kroatien |
| en | English | croatia |
| hr | Hrvatski | hrvatska |
| fr | Francais | croatie |
| nl | Nederlands | kroatie |
| pl | Polski | chorwacja |
| cz | Cestina | chorvatsko |
| sk | Slovencina | chorvatsko |
| ru | Russkij | horvatiya |
| gr | Ellinika | kroatia |
| sw | Svenska | kroatien |
| no | Norsk | kroatia |

### Uebersetzungs-Systematik

#### 1. Context Processors (Statische UI-Texte) - EMPFOHLEN fuer feste Texte
**Datei:** main/context_processors.py
**Kosten:** Keine (hardcodiert)
**Performance:** Sehr schnell (aus Dictionary)
**Verwendung:** UI-Labels, Buttons, Formulare, Navigation

Beispiele:
- COOKIE_TRANSLATIONS - Cookie Banner
- SITEMAP_TRANSLATIONS - Sitemap-Seite
- SEARCH_FILTER_TRANSLATIONS - Suchfilter
- TWO_FA_TRANSLATIONS - 2FA Setup
- BUYER_GUIDE_TRANSLATIONS - Kaeufer-Leitfaden

**Template-Nutzung:**
{{ sm_home }}  --> Sitemap: "Startseite"
{{ bg_title }}  --> Buyer Guide: "Kaeuferleitfaden"
{{ cookie_accept }}  --> Cookie: "Alle akzeptieren"

#### 2. Translation Model (DB-basiert) - Fuer verwaltbare Inhalte
**Datei:** pages/models.py -> Translation
**Kosten:** Keine (manuell gepflegt)
**Performance:** Schnell (DB-Query, cachebar)
**Verwendung:** Navbar, Footer, Home-Texte

**Felder:** german_content, english_content, croatian_content, etc.

**Template-Nutzung:**
{{ navbar_home }}  --> aus Translation Model
{{ footer_contact }}

#### 3. StaticContent Model (DB + KI) - Fuer groessere Textbloecke
**Datei:** main/models.py -> StaticContent
**Kosten:** Einmalig bei KI-Uebersetzung
**Performance:** Schnell (DB-Query)
**Verwendung:** Laengere statische Texte die zentral verwaltet werden sollen

**Felder:** german, english, croatian, etc.
**Methode:** get_translation(lang_code)

#### 4. On-Demand KI-Uebersetzung - NUR fuer dynamische Inhalte
**Datei:** main/translation_service.py
**Kosten:** Pro API-Call (OpenAI)
**Performance:** Langsamer (API-Aufruf, dann DB-Cache)
**Verwendung:** Listing-Beschreibungen, Property Titles

**Workflow:**
1. Nutzer wechselt Sprache
2. System prueft ob Uebersetzung in DB existiert
3. Falls nein: KI uebersetzt, speichert in DB
4. Falls ja: Laedt aus DB (keine API-Kosten)

### Sprache aus URL ermitteln
path_parts = request.path.strip("/").split("/")
url_lang = path_parts[0] if path_parts[0] in ["ge", "en", "hr", ...] else None
user_language = url_lang or request.session.get("site_language", "ge")

### Wichtige Dateien
- main/context_processors.py - Alle Context Processors
- main/translation_service.py - KI-Uebersetzung (OpenAI)
- main/static_translation_service.py - Batch-Uebersetzung fuer StaticContent
- pages/models.py - Translation Model
- main/models.py - StaticContent Model

### Regeln
1. UI-Texte (Buttons, Labels) -> Context Processor (hardcodiert)
2. Verwaltbare Texte (Navbar, Footer) -> Translation Model
3. Dynamische Inhalte (Listings) -> On-Demand KI mit DB-Cache
4. NIEMALS KI fuer statische UI-Texte verwenden (teuer + langsam)
