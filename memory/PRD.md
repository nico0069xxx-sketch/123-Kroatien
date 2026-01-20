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

## Prioritized Task List

### 🔴 P0 - Critical / Blocker

| Task | Status | Notes |
|------|--------|-------|
| Übersetzungs-Blocker lösen | ✅ DONE | Alle 12 Sprachen funktionieren. Fehlende Keys hinzugefügt (nav_back, btn_send_message, label_details) |
| Objektnummer sichtbar machen | ✅ DONE | 123K-Prefix implementiert für Branding (z.B. 123K-4567) |

### 🟡 P1 - Important

| Task | Status | Notes |
|------|--------|-------|
| Login-System vereinfachen | TODO | Verschiedene Rollen haben Anmeldeprobleme, kostet Zeit und nervt |
| Gruppe B User Guide erweitern | TODO | Soll wie Gruppe A Guide strukturiert sein |
| OpenAI Chatbot prüfen | TODO | Möglichkeiten für Service Provider |

### 🟠 P2 - Backlog

| Task | Status | Notes |
|------|--------|-------|
| CSS-Architektur stabilisieren | TODO | KRITISCH - sehr fragil |
| URL-Architektur refactoren | TODO | Dringend |
| Review/Rating System | TODO | |
| Mobile View Optimierung | TODO | |
| Legacy Code konsolidieren | TODO | z.B. zwei `partner_landing` Funktionen |
| Brittle Topbar Model | TODO | Hotfix existiert, Root Cause offen |
| nice-select.js Dropdown Styling | TODO | Legacy Plugin, schwer zu stylen |

---

## Completed Work

### Session vor diesem Fork:
- ✅ Social Media Dokumentation für Gruppe B (`anleitung.html`)
- ✅ Logo-Bug behoben (`professional.logo` → `professional.company_logo`)
- ✅ 6 Dummy-Listings erstellt (ohne Bilder)
- ✅ Listing Card Error behoben (`NoReverseMatch`)
- ✅ Neue moderne Property-Detail-Seite (`single-detail-modern.html`)
- ✅ OpenStreetMap eingebunden (Stadt-Ebene, bleibt so)

---

## Translation System Debug Checklist

Der Übersetzungs-Blocker erfordert folgende Schritte:

1. **Alle `page`-Werte in DB auflisten:**
   ```bash
   python3 manage.py shell -c "from pages.models import Translation; print(set(t.page for t in Translation.objects.all()))"
   ```

2. **`context_processors.py` analysieren:**
   - Datei: `main/context_processors.py`
   - Funktion: `get_my_translations`
   - Problem: Lädt nicht alle benötigten Seiten

3. **Query erweitern:** 
   Alle Seiten hinzufügen die Labels für Detail-Seite haben (z.B. 'contact', etc.)

4. **Testen:** Mit `?lang=fr` Parameter

---

## Key Files

| File | Purpose |
|------|---------|
| `templates/main/single-detail-modern.html` | Neue Property-Detail-Seite (BLOCKER) |
| `main/context_processors.py` | Lädt Übersetzungen (DEBUG HERE) |
| `main/views.py` | `property_details` View |
| `pages/models.py` | `Translation` Model |

---

## Credentials

| Role | URL | Username | Password |
|------|-----|----------|----------|
| Admin | `/nik-verwaltung-2026/` | Nik | Admin1234! |
| Gruppe A (Makler) | `/accounts/login` | Nik | Admin1234! |
| Gruppe B (Professional) | `/accounts/login` | archtiket | Architekt!123456789 |

---

## Technical Architecture

- **Framework:** Django Monolith
- **Location:** `/app/real-estate-django-main`
- **Translations:** 
  - Dynamic: `json_content` JSONField auf Models
  - Static Labels: `pages.Translation` Model, geladen via Context Processor

---

## Decisions Made

- OpenStreetMap bleibt auf Stadt-Ebene (kein Straßen-Zoom) ✅
- Objektnummer muss sichtbar sein, normale Größe ✅

---

*Last Updated: December 2024*
