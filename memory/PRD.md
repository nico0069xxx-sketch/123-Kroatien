# Real Estate Django Platform - PRD

## Original Problem Statement
Transform a local Django real estate marketplace into a "Königsklasse" (King Class) platform. The primary goal is to restore lost features (chatbot, professional group profiles, 2FA) after a data incident, fix UI/UX issues, and add new content pages for SEO.

## User Persona
- **Name:** Nik
- **Technical Level:** Non-developer ("Laie")
- **Environment:** macOS, Terminal
- **Language:** German (informal "du")
- **Special Note:** User's TextEdit app corrupts HTML files - always use Python scripts for file modifications

## Tech Stack
- **Backend:** Django
- **Frontend:** Django Templates, JavaScript, jQuery (nice-select plugin)
- **Database:** SQLite3
- **AI Integration:** OpenAI GPT-3.5-turbo

---

## Completed Features ✅

### Session 1 (Completed)
- [x] **Dynamic Price Filter** - Homepage price dropdowns switch between Sale/Rent ranges
- [x] **AI Chatbot** - Fully restored, 12 languages, GPT-3.5-turbo integration
- [x] **2FA/TOTP Login** - Reactivated, setup page redesigned (DE/EN/HR)
- [x] **Important Addresses Page** - New page with categorized contacts, 12 languages
- [x] **Navigation Update** - "MARKT" dropdown with Market Reports & Addresses
- [x] **XML Interfaces** - OpenImmo and Croatian XML exports verified

---

## Pending Issues 🔴

### P0 - High Priority
1. **Homepage Search Filter Incomplete**
   - Missing: Wohnfläche, Grundstücksgröße, Zimmeranzahl, Bäder
   - Files: `templates/main/home.html`, `main/views.py`

### P1 - Medium Priority
2. **Language Switcher Bug**
   - Redirects to homepage instead of current page
   - Files: `templates/include/base.html`, Django `set-language` view

3. **Professional Groups Not Working**
   - Navigation links lead to 404s
   - Files: `main/professional_models.py`, `main/professional_views.py`

### P2 - Low Priority
4. **Email Notifications Broken**
   - BadCredentials error - needs Google App Password
   - Status: BLOCKED (waiting for user action)

---

## Future Tasks 🔵

- [ ] AI Smart-Search feature
- [ ] RSS Feed for Croatian news
- [ ] Refactor `get_my_translations` function in `context_processors.py`

---

## Key Files Reference

| File | Purpose |
|------|---------|
| `templates/main/home.html` | Homepage with search filter |
| `templates/include/base.html` | Main navigation, chatbot include |
| `main/context_processors.py` | Translations and URLs |
| `main/views.py` | Main listings view, search processing |
| `main/chatbot.py` | AI chatbot backend |
| `accounts/totp_views.py` | 2FA logic |
| `main/address_views.py` | Important Addresses page |

---

## API Endpoints

- `/api/chatbot/` - AI chatbot backend
- `/api/xml/openimmo/` - German property portal XML
- `/api/xml/croatia/` - Croatian partner XML

---

## Critical Workflow Notes

⚠️ **DO NOT ask user to edit files directly** - TextEdit corrupts HTML
✅ **Use Python scripts** (`cat > script.py`) for all file modifications
✅ **Communicate in German** (informal "du")
✅ **Provide simple, copy-paste Terminal commands**

---

*Last Updated: December 2025*
