# 123-Kroatien.eu - Real Estate Portal PRD

## Original Problem Statement
Django-basiertes Immobilienportal mit zwei Benutzergruppen (Gruppe A: Makler/Bauträger, Gruppe B: Professionals/Dienstleister). Das Portal unterstützt 12 Sprachen und benötigt moderne UI/UX-Überarbeitung.

---

## User Context
- **User:** Nik (Deutsch, informelles "du")
- **System:** Apple Mac M1, Terminal, Safari
- **Lokaler Pfad:** `~/Desktop/real-estate-django-ALTmain`
- **Emergent Pfad:** `/app/real-estate-django-main`

---

## Git Workflow Rules (KRITISCH!)

```
BASELINE: 9ec9d9a on main — DO NOT BREAK
WORKFLOW: Branch-only (feature/*, fix/*)
GITHUB: Canonical history
TIME MACHINE: Parallel backup (recovery only)
```

### START (MUST):
1. `cd ~/Desktop/real-estate-django-ALTmain`
2. `git fetch --all`
3. Verify: git status clean, branch is main, HEAD at/from 9ec9d9a
4. Create feature/* or fix/* branch BEFORE any work
5. Dirty tree → WIP commit or timestamped stash immediately

### RULES (MUST):
- Never work directly on main
- Never delete/overwrite without Git history
- Never commit secrets (.env), db.sqlite3, media/, backups
- Never use iCloud as source/merge/restore
- Model changes require migrations
- GitHub Actions workflow changes via GitHub Web UI only

### END (MUST):
- Run checks/tests if available
- Commit changes
- Push branch to GitHub
- Update HANDOFF.md (done/next/risks)
- Ensure git status clean

---

## 📍 PROJEKT-SITEMAP

Vollständige Dokumentation: `PROJEKT_SITEMAP.md`

### Haupt-URLs
| Bereich | URLs | Beschreibung |
|---------|------|--------------|
| Öffentlich | `/`, `/listing/`, `/contact/`, `/about/`, `/faq/` | Hauptseiten |
| Glossar | `/{lang}/{country}/{glossar}/` | 12-sprachig, SEO-optimiert |
| Makler-Portal | `/makler-dashboard/`, `/makler-portal/*` | Für Makler & Bauträger |
| Professional Portal | `/portal/*` | Für Anwälte, Steuerberater, Architekten |
| Directory | `/ge/kroatien/{kategorie}/` | Öffentliches Dienstleister-Verzeichnis |
| Accounts | `/accounts/*` | Login, Register, Password-Reset |
| Technisch | `/admin/`, `/sitemap.xml`, `/robots.txt` | Admin & SEO |

### 12 unterstützte Sprachen
`ge` (DE), `en`, `hr`, `fr`, `nl`, `pl`, `cz`, `sk`, `ru`, `gr`, `sw`, `no`

---

## Prioritized Task List

### 🔴 P0 - Critical / Blocker

| Task | Status | Notes |
|------|--------|-------|
| Übersetzungs-Blocker lösen | ✅ DONE | Alle 12 Sprachen funktionieren |
| Objektnummer sichtbar machen | ✅ DONE | 123K-Prefix implementiert |
| Django Migrations instabil | ⚠️ BYPASSED | `makemigrations` schlägt fehl (professional_models Problem) |

### 🟡 P1 - Important

| Task | Status | Notes |
|------|--------|-------|
| Smart-404 Handler | ✅ DONE | Custom 404 mit Vorschlägen |
| Redirect Middleware | ✅ DONE | DB-basierte 301-Redirects aktiv |
| Sitemaps | ✅ DONE | `/sitemaps/glossary.xml` |
| Hreflang Tags | ✅ DONE | Auf Glossar-Detailseiten |
| Cookie Banner 12 Sprachen | ✅ DONE | Multilingual, URL-basierte Sprach-Erkennung |
| Glossar Akkordeon-UI | ✅ DONE | Premium-Design mit Pagination |
| FAQ Redesign | ✅ DONE | Öffentlich, multilingual aus JSON |
| CSS-Animationen fixen | TODO | Akkordeon-Animationen haben CSS-Konflikte |
| Sprint 4: Topic Clustering | TODO | Landing-Pages mit Compliance-Texten |
| Login-System vereinfachen | TODO | Verschiedene Rollen haben Anmeldeprobleme |

### 🟠 P2 - Backlog

| Task | Status | Notes |
|------|--------|-------|
| CSS-Architektur stabilisieren | TODO | KRITISCH - sehr fragil, inline vs. global |
| URL-Architektur refactoren | TODO | z.B. `/en/croatia/marktberichte/` nicht übersetzt |
| Glossar-Slugs RU/GR | TODO | Numerisch statt Wörter |
| Review/Rating System | TODO | |
| Mobile View Optimierung | TODO | |
| Legacy Code konsolidieren | TODO | z.B. zwei `partner_landing` Funktionen |

---

## Completed Work

### Letzte Session (Cookie Banner & SEO):
- ✅ Cookie-Banner 12 Sprachen reaktiviert
- ✅ FAQ-Seite öffentlich gemacht und redesigned
- ✅ Glossar mit Premium-Akkordeon-UI
- ✅ Smart-404 Handler implementiert
- ✅ Redirect Middleware aktiviert
- ✅ Sitemaps für Glossar erstellt
- ✅ Hreflang Tags implementiert
- ✅ `.env` Datei für lokale Entwicklung erstellt

### Frühere Sessions:
- ✅ Social Media Dokumentation für Gruppe B (`anleitung.html`)
- ✅ Logo-Bug behoben (`professional.logo` → `professional.company_logo`)
- ✅ 6 Dummy-Listings erstellt (ohne Bilder)
- ✅ Listing Card Error behoben (`NoReverseMatch`)
- ✅ Neue moderne Property-Detail-Seite (`single-detail-modern.html`)
- ✅ OpenStreetMap eingebunden (Stadt-Ebene, bleibt so)
- ✅ Übersetzungs-System für alle 12 Sprachen

---

## Key Files

| File | Purpose |
|------|---------|
| `PROJEKT_SITEMAP.md` | **NEU** - Vollständige URL-Struktur & Projektübersicht |
| `main/context_processors.py` | Lädt Übersetzungen + Cookie Banner Sprache |
| `main/glossary_*.py` | Glossar-System (Models, Views, URLs) |
| `main/middleware/*.py` | Redirect-Middleware |
| `templates/include/base.html` | Haupt-Layout mit Cookie Banner |
| `templates/glossary/*.html` | Glossar-Templates |
| `templates/main/faq.html` | FAQ mit multilingual JSON |

---

## Credentials

| Role | URL | Username | Password |
|------|-----|----------|----------|
| Admin | `/nik-verwaltung-2026/` | Nik | Admin1234! |
| Gruppe A (Makler) | `/accounts/login` | Nik | Admin1234! |
| Gruppe B (Professional) | `/accounts/login` | archtiket | Architekt!123456789 |

---

## Technical Architecture

- **Framework:** Django 4.2.1 Monolith
- **Python:** 3.8+
- **Location:** `/app/real-estate-django-main`
- **Database:** SQLite (Dev) / PostgreSQL (Prod)
- **Translations:** 
  - Dynamic: `json_content` JSONField auf Models
  - Static Labels: `pages.Translation` Model, geladen via Context Processor
  - Cookie Banner: Separate JSON-Dateien pro Sprache

### Middleware (Aktiv)
- `RedirectRegistryMiddleware` - DB-basierte 301-Redirects
- `SmartRedirectMiddleware` - Intelligente URL-Umleitung
- Custom 404 Handler - Smart-404 mit Vorschlägen

---

## Bekannte Technische Schulden

| Problem | Priorität | Details |
|---------|-----------|---------|
| **Django Migrations** | 🔴 Hoch | `makemigrations` schlägt fehl wegen NOT NULL in professional_models. Nur bypassed, nicht gelöst. |
| **CSS-Konflikte** | 🟡 Mittel | Inline Styles vs. `styles.css`/`modern-theme.css`. Akkordeon-Animationen funktionieren nicht. |
| **URL-Übersetzungen** | 🟡 Mittel | Einige Pfade nicht übersetzt (z.B. `/en/croatia/marktberichte/`) |
| **Context Processor** | 🟡 Mittel | `main/context_processors.py` ist komplex und fehleranfällig geworden. |

---

## Decisions Made

- OpenStreetMap bleibt auf Stadt-Ebene (kein Straßen-Zoom) ✅
- Objektnummer muss sichtbar sein, normale Größe ✅
- Cookie Banner nutzt URL-Path für Sprach-Erkennung (Fallback auf Session) ✅

---

*Last Updated: Dezember 2024*
