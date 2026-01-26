# 123-Kroatien.eu - Product Requirements Document

## Original Problem Statement
Nik entwickelt ein 12-sprachiges Django Immobilienportal für Kroatien. Das Portal soll für AI-Suchmaschinen (GEO) optimiert sein und einen intelligenten Chatbot mit Glossar-Integration bieten.

## User Context
- **Name:** Nik (duzen, Deutsch sprechen)
- **System:** Apple Mac M1, Terminal, Safari
- **Skill-Level:** Laie - JEDEN Befehl einzeln und kopierbar geben
- **Repository:** https://github.com/nico0069xxx-sketch/123-Kroatien

## Core Architecture
- **Framework:** Django Monolith (KEIN React/Vue Frontend)
- **Datenbank:** SQLite (dev), PostgreSQL (prod)
- **12 Sprachen:** ge, en, hr, fr, nl, pl, cz, sk, ru, gr, sw, no

## What's Been Implemented

### Session 26. Januar 2026:
- ✅ GitHub PRs aufgeräumt (4 PRs geschlossen)
- ✅ Norwegisch-Startseite `/no/` gefixt (explizite Route)
- ✅ Preis-Format korrigiert (`$ 350000 €` → `350000 €`)
- ✅ CTA-Banner für 12 Sprachen übersetzt
- ✅ URL-Struktur für alle Sprachen validiert

### Frühere Sessions:
- ✅ GEO-Strategie implementiert (llms.txt, Schema.org)
- ✅ Chatbot mit Glossar-Integration
- ✅ FAQ Cleanup (62 → 10 Fragen)
- ✅ Article Schema für Marktberichte

## Prioritized Backlog

### P0 - Critical Bugs:
1. **Dummy-Listings erscheinen trotz is_published=False**
   - IDs: 2, 3, 4, 5
   - Query in `main/views.py` Zeile 59 prüfen
   - Möglicherweise Cache-Problem

### P1 - High Priority:
1. Übersetzungs-Generator für leere Listing-Felder
2. Glossar erweitern (basierend auf entfernten FAQ-Themen)

### P2 - Medium Priority:
1. Fragile Django Migrations fixen (`listing_id` Spalte fehlt)
2. Schema.org auf weitere Seiten ausweiten (RealEstateListing)
3. base.html Schema mehrsprachig machen

### P3 - Backlog:
1. White Listing Feature für Makler/Bauunternehmen
2. Chatbot UI Styling verbessern
3. Expertenfinder Ergebnisse Styling

## Key Files Reference
- `realstate/urls.py` - Haupt-URL-Routing
- `main/urls.py` - App-URLs
- `main/views.py` - Home View mit Listing-Übersetzungslogik
- `main/context_processors.py` - Template-Variablen
- `templates/main/home.html` - Startseite Template
- `listings/models.py` - Listing Model mit Übersetzungsfeldern
- `AGENT_BRIEFING.md` - Projekt-Dokumentation

## Technical Notes

### Listing-Übersetzungen:
- Jedes Listing hat Felder: `german_content`, `english_content`, `french_content`, etc.
- Diese Felder enthalten JSON mit übersetztem Titel, Beschreibung, etc.
- Wenn Feld leer → Fallback auf `get_json()` (Deutsch)
- View setzt `listing.json_content` basierend auf `user_language`

### URL-Struktur:
- Statische Seiten: `/ge/sitemap/`, `/ge/imprint/`, etc.
- Dynamische Seiten mit Land-Slug: `/ge/kroatien/glossar/`, `/fr/croatie/actualites/`
- Sprach-spezifische URL-Segmente definiert in `main/content_urls.py` und `main/glossary_models.py`

### Bekannte Architektur-Regeln:
- Views außerhalb i18n_patterns MÜSSEN `request.session['site_language']` setzen
- JavaScript fetch() MUSS `{{ language }}` nutzen, nicht hardcoded `/ge/`
- Dienstleister-Bereich nur für DE und HR
