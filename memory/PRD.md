# 123-KROATIEN.EU - Project Requirements & Status

## Original Problem Statement
Multilingual (12 languages) Django real estate portal for Croatian properties. The platform connects European buyers from 12 countries with certified Croatian real estate agents and construction companies.

**Business Model:**
- Properties: Exclusively Croatian real estate
- Sellers: Only certified Croatian agents and construction companies
- Buyers: Prospects from 12 European countries
- Languages: ge, en, hr, fr, nl, pl, cz, sk, ru, gr, sw, no

## Current State: PRE-LAUNCH
The portal is not yet live. All development is done locally and pushed to GitHub.

---

## What's Been Implemented

### GEO (Generative Engine Optimization) - January 2026
| Feature | Status | Files |
|---------|--------|-------|
| `llms.txt` for AI crawlers | ✅ Done | `llms.txt`, `main/xml_views.py`, `realstate/urls.py` |
| `robots.txt` with Llms-txt reference | ✅ Done | `main/xml_views.py` |
| FAQ Schema (`FAQPage`) | ✅ Done | `templates/main/faq.html` |
| HowTo Schema (Buyer Guide) | ✅ Done | `templates/legal/buyer_guide.html` |
| Organization Schema (fixed) | ✅ Done | `templates/include/base.html` |
| Glossar `DefinedTerm` Schema | ✅ Was existing | `templates/glossary/_jsonld_defined_term.html` |

### Chatbot Integration - January 2026
| Feature | Status | Files |
|---------|--------|-------|
| Glossar integration in Chatbot | ✅ Done | `main/chatbot.py` |
| FAQ Cleanup (62 → 10) | ✅ Done | `main/faq_data*.json` (all 12 languages) |

### Previous Sessions (per Handoff)
- Fixed all critical URL/routing bugs for 12 languages
- Refactored templates to use context processors instead of hardcoded translations
- Fixed hardcoded `/ge/` API URLs in JavaScript
- Fixed missing database translations

---

## Architecture

### Tech Stack
- **Framework**: Django Monolith (NO React/Vue)
- **Database**: SQLite (dev), PostgreSQL (prod)
- **Languages**: 12 (ge, en, hr, fr, nl, pl, cz, sk, ru, gr, sw, no)

### Key Patterns
1. **Translations**: Centralized in context processors (`main/context_processors.py`)
2. **URL Routing**: Static pages OUTSIDE `i18n_patterns`, dynamic pages inside
3. **Session Language**: Views must set `request.session['site_language']` for context processors
4. **JavaScript**: Always use `{{ language }}` template variable, never hardcode `/ge/`

### Key Files
- `AGENT_BRIEFING.md` - **MUST READ** for any agent
- `realstate/urls.py` - Main URL routing
- `main/urls.py` - App URLs
- `main/context_processors.py` - Translation dictionaries
- `main/chatbot.py` - Chatbot with FAQ + Glossar integration
- `main/glossary_models.py` - Glossar database models

---

## P0 - Next Priority Tasks
- None critical

## P1 - Should Do
- Article Schema for Marktberichte (market reports)
- Add more Glossar terms as needed

## P2 - Backlog
- Fragile Django Migrations (investigate)
- Chatbot/UI Styling improvements
- Hardcoded German text in `base.html` Schema.org JSON-LD block

---

## User Context
- **Name**: Nik (use informal German "du")
- **System**: Apple Mac M1, Terminal, Safari
- **Skill Level**: Laie - provide single, copy-pasteable commands
- **Workflow**: Branch-only (feature/*, fix/*), never commit to main directly

## Workflow Rules
1. Always create new branch before work
2. Always merge via GitHub Pull Request
3. Always `git checkout main && git pull origin main` after merge
4. Server restart: `python3 manage.py runserver`

---

## Testing Notes
- All features tested locally via browser
- FAQ page: `http://127.0.0.1:8000/ge/faq/`
- Chatbot: Available on homepage
- Glossar: 39 terms in database (German)
