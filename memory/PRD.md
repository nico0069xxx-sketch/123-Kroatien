# 123-Kroatien.eu - Immobilienportal PRD

## Original Problem Statement
Multilinguales Immobilienportal für Kroatien mit 12 Sprachen (DE, EN, HR, FR, NL, PL, CZ, SK, RU, GR, SW, NO).

## Architektur
- **Framework**: Django Monolith
- **Datenbank**: SQLite (dev) / PostgreSQL (prod)
- **Sprachen**: 12 Sprachen mit übersetzten URLs

## Completed (Session 23. Jan 2025)

### ✅ P0 Critical Bug Fix: Globaler Sprachumschalter
- **Problem**: Header-Sprachumschalter funktionierte nicht bei übersetzten URL-Slugs (z.B. `/glossar/` vs `/pojmovnik/`)
- **Lösung**: 
  1. `main/context_processors.py` - URL-Mapping für alle 12 Sprachen hinzugefügt
  2. `templates/include/base.html` - JavaScript nutzt generierte `languageUrls`
  3. `main/views.py` - `next` Parameter hat jetzt Priorität vor `HTTP_REFERER`
- **Status**: GETESTET & FUNKTIONIERT ✅
- **Commit**: e9c62d7 on feature/glossary

### Vorherige Session (Handoff)
- Mehrsprachige Sitemap (12 Sprachen) mit SEO/JSON-LD
- Mehrsprachiger Buyer Guide mit page-spezifischem Sprachumschalter
- Session-Dauer auf 2 Wochen verlängert
- KI-Status-Audit durchgeführt

## Pending Issues

### 🟠 P1: Nicht existierende KI-Features
- "Expertenfinder" und "Chatbot" sind in der UI verlinkt, existieren aber nicht
- **Entscheidung nötig**: Links entfernen oder Features bauen?

### 🟠 P1: Fragile Django Migrations
- `makemigrations` ist instabil (professional, referenceproject Models)
- Blocker für zukünftige DB-Änderungen

### 🟡 P1: Sprint 4 Tasks
- Topic Clustering auf Landing Pages
- Compliance-Texte integrieren
- UX/Akkordeon-Layout Animationen

## Backlog / Technical Debt

- **P0**: CSS Instabilität refactoren
- **P0**: URL-Architektur überarbeiten (inkonsistente Übersetzungen)
- **P1**: Glossar-Slugs für RU/GR (numerische Slugs)
- **P1**: Registration URLs & Views konsolidieren
- **P1**: Review/Rating System implementieren

## Key Files Reference
- `main/context_processors.py` - Sprach-URL-Mapping
- `main/views.py` - set_language_from_url View
- `templates/include/base.html` - Header mit Sprachumschalter
- `main/glossary_urls.py` - Glossar URL Patterns
- `main/glossary_models.py` - GLOSSARY_URLS, COUNTRY_NAMES Konstanten
