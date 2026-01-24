# 123-Kroatien.eu - Immobilienportal PRD

## Original Problem Statement
Multilinguales Immobilienportal für Kroatien mit 12 Sprachen (DE, EN, HR, FR, NL, PL, CZ, SK, RU, GR, SW, NO).

## Architektur
- **Framework**: Django Monolith
- **Datenbank**: SQLite (dev) / PostgreSQL (prod)
- **Sprachen**: 12 Sprachen mit übersetzten URLs

---

## Completed (Session 24. Januar 2026)

### ✅ P0 Bug Fix: Sitemap 12-Sprachen Übersetzungen
- **Problem**: Sitemap zeigte nur 3 Sprachen (DE, EN, HR), alle anderen zeigten deutschen Text
- **Lösung**: 
  1. `templates/main/sitemap.html` – Alle `{% if %}` Blöcke auf 12 Sprachen erweitert
  2. Dienstleister-Links (Immobilienmakler, etc.) mit direkten Übersetzungen versehen
- **Status**: IMPLEMENTIERT ✅

### ✅ Bug Fix: Header-Sprachumschalter vereinfacht
- **Problem**: Komplexe `languageUrls` Logik verursachte gemischte Sprachen
- **Lösung**: `changelanguage()` Funktion auf einfache `/set-language/xx/` Weiterleitung reduziert
- **Datei**: `templates/include/base.html`
- **Status**: IMPLEMENTIERT ✅

### ✅ URL Fix: Sitemap mit Trailing Slash
- **Problem**: `/sitemap` vs `/sitemap/` Inkonsistenz
- **Lösung**: Beide Varianten in `main/urls.py` registriert
- **Status**: IMPLEMENTIERT ✅

---

## Completed (Session 23. Januar 2026)

### ✅ P0 Bug Fix: Globaler Sprachumschalter
- **Problem**: Header-Sprachumschalter funktionierte nicht bei übersetzten URL-Slugs (z.B. `/glossar/` vs `/pojmovnik/`)
- **Lösung**: 
  1. `main/context_processors.py` – URL-Mapping für alle 12 Sprachen hinzugefügt
  2. `main/views.py` – `next` Parameter hat jetzt Priorität vor `HTTP_REFERER`
  3. `templates/include/base.html` – JavaScript nutzt generierte `languageUrls`
- **Commits**: 
  - `e9c62d7` – Sprachumschalter Fix
  - `6d63108` – Hero-Übersetzungen + Regex-Fix
- **Status**: GETESTET & FUNKTIONIERT ✅

### ✅ Bug Fix: Regex-Reihenfolge für Glossar-URLs
- **Problem**: `glossar` matchte vor `glossary`, was zu `/y/buyer-guide/` URLs führte
- **Lösung**: Glossar-Slugs nach Länge sortiert (längste zuerst)
- **Status**: GETESTET & FUNKTIONIERT ✅

### ✅ Bug Fix: Hero-Section Übersetzungen wiederhergestellt
- **Problem**: Hero-Texte (Tagline, Title, Subtitle) waren leer
- **Ursache**: Template verwendete `{{hero_tagline}}` aber die Übersetzungen fehlten im context_processors.py
- **Lösung**: Alle 12 Sprachen wieder in `get_my_translations()` hinzugefügt
- **Status**: GETESTET & FUNKTIONIERT ✅

### ✅ Bug Fix: Professional Form
- **Problem**: `languages` Feld existierte nicht im Model
- **Lösung**: Geändert zu `spoken_languages`
- **Status**: GETESTET & FUNKTIONIERT ✅

---

## Pending Issues

### 🟠 P1: Nicht existierende KI-Features
- **Status**: Laut KI_STATUS_REPORT.md existieren "Expertenfinder" und "Chatbot" nicht im Code
- **Betroffene Stellen**: 
  - `templates/main/sitemap.html` – Expertenfinder als "derzeit nicht verfügbar" markiert
  - Möglicherweise weitere Links in Header/Footer (in Niks lokaler Version)
- **Entscheidung nötig**: Links entfernen oder Features implementieren?

### 🟠 P1: Fragile Django Migrations
- **Problem**: `makemigrations` war instabil in früheren Sessions
- **Aktueller Status**: In meiner Umgebung funktioniert es – Problem evtl. nur lokal bei Nik
- **Betroffene Models**: `professional`, `referenceproject`

### 🟠 P1: Legacy API Key in translate.py
- **Datei**: `listings/translate.py`
- **Problem**: Verwendet hardcodierten OpenAI Key statt Emergent Integrations
- **Empfehlung**: Migration auf Emergent LLM Key

### 🟡 P1: Sprint 4 Tasks
- Topic Clustering auf Landing Pages
- Compliance-Texte integrieren
- UX/Akkordeon-Layout Animationen

---

## KI-Features Status (aus KI_STATUS_REPORT.md)

| Feature | Status | API |
|---------|--------|-----|
| KI-Textgenerierung | ✅ OK | Emergent |
| Professional AI | ✅ OK | Emergent |
| Übersetzung | ⚠️ Legacy Key | Direkt OpenAI |
| Expertenfinder | ❌ Nicht implementiert | - |
| KI Schnellsuche | ❓ Unklar | - |
| Chatbot | ❌ Nicht implementiert | - |

---

## Backlog / Technical Debt

- **P0**: CSS Instabilität refactoren
- **P0**: URL-Architektur überarbeiten (inkonsistente Übersetzungen)
- **P1**: Glossar-Slugs für RU/GR (numerische Slugs)
- **P1**: Registration URLs & Views konsolidieren
- **P1**: Review/Rating System implementieren

---

## Key Files Reference

### Sprachumschalter
- `main/context_processors.py` – `get_language_urls_for_path()`, Hero-Übersetzungen
- `main/views.py` – `set_language_from_url()` View
- `templates/include/base.html` – JavaScript `changelanguage()` Funktion

### Glossar System
- `main/glossary_urls.py` – URL Patterns für 12 Sprachen
- `main/glossary_models.py` – `GLOSSARY_URLS`, `COUNTRY_NAMES` Konstanten
- `main/glossary_views.py` – Views für Index, Detail, Landing Pages

### KI Features
- `main/listing_description_ai.py` – KI-Textgenerierung (funktioniert)
- `main/professional_ai_generator.py` – Professional AI (funktioniert)
- `listings/translate.py` – Übersetzungen (Legacy Key!)
- `KI_STATUS_REPORT.md` – Vollständiger Audit

---

## Git Workflow (Nik's Setup)

- **BASELINE**: `9ec9d9a` on main – DO NOT BREAK
- **WORKFLOW**: Branch-only (`feature/*`, `fix/*`)
- **AKTUELLER BRANCH**: `feature/glossary`
- **Letzte Commits**:
  - `6d63108` – Hero-Übersetzungen + Regex-Fix
  - `e9c62d7` – Sprachumschalter Fix
  - `b93b3a4` – 12-language buyer guide

---

## User Context

- **Name**: Nik
- **Sprache**: Deutsch (informell "du")
- **System**: Apple Mac M1, Safari, Terminal
- **Lokales Verzeichnis**: `~/Desktop/real-estate-django-ALTmain`
