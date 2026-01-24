# 123-KROATIEN.EU - AGENT BRIEFING

## 🔒 BASELINE & WORKFLOW
- **BASELINE:** 9ec9d9a on main — DO NOT BREAK
- **WORKFLOW:** Branch-only (feature/*, fix/*)
- **GITHUB:** Canonical history (Source of Truth)
- **TIME MACHINE:** Parallel backup (recovery only, NEVER merge from iCloud)

## 👤 USER CONTEXT
- **Name:** Nik (bitte dutzen, Deutsch sprechen)
- **System:** Apple Mac M1, Terminal, Safari
- **Skill-Level:** Laie - JEDEN Befehl einzeln und kopierbar geben
- **Server-Neustart:** IMMER explizit sagen wann nötig: python3 manage.py runserver

## 🏗️ PROJEKT-ARCHITEKTUR
- **Django Monolith** (KEIN React/Vue Frontend)
- **Datenbank:** SQLite (dev), PostgreSQL (prod)
- **12 Sprachen:** ge, en, hr, fr, nl, pl, cz, sk, ru, gr, sw, no

### ⚠️ KRITISCHE ARCHITEKTUR-PROBLEME

#### 1. URL-Architektur INKONSISTENT
- Manche Seiten nutzen i18n-Prefix (/en/listing/), manche nicht (/listing/)
- Bei URL-Änderungen IMMER in realstate/urls.py UND main/urls.py prüfen
- i18n_patterns in realstate/urls.py - Routen AUSSERHALB davon haben KEIN Sprachpräfix

#### 2. Übersetzungen HARDCODED in Templates
- Problem: {% if language == 'hr' %}...{% elif %}...{% endif %} überall
- Besser wäre: Übersetzungen in DB (pages.models.Translation)
- Bei Template-Übersetzungen IMMER alle 12 Sprachen prüfen

#### 3. LocaleMiddleware Konflikte
- Django LocaleMiddleware interpretiert /no/, /fr/ etc. als Sprachpräfix
- Statische Seiten (sitemap, etc.) AUSSERHALB von i18n_patterns registrieren

### 📁 WICHTIGE DATEIEN
- realstate/urls.py - Haupt-URL-Routing (i18n_patterns am Ende!)
- main/urls.py - App-URLs (Reihenfolge wichtig)
- main/context_processors.py - Globale Template-Variablen
- templates/include/base.html - changelanguage() Funktion Zeile ~379
- main/views.py - set_language_from_url()

## ✅ START CHECKLISTE
1) cd ~/Desktop/real-estate-django-ALTmain
2) git fetch --all
3) git status (MUSS SAUBER SEIN)
4) git checkout main && git pull origin main
5) git checkout -b fix/beschreibung-hier (NEUER Branch VOR jeder Arbeit)

## 🚫 VERBOTEN
- Niemals direkt auf main arbeiten
- Niemals .env, db.sqlite3, media/ committen
- Niemals iCloud als Source nutzen
- Niemals Model ändern ohne Migration

## ✅ ENDE CHECKLISTE
1) python3 manage.py check
2) git add . && git commit -m "beschreibung"
3) git push origin BRANCH-NAME
4) HANDOFF.md aktualisieren
5) git status (MUSS clean sein)

## 🔧 HÄUFIGE PROBLEME
- Sprachwechsel kaputt: Prüfe changelanguage() in base.html und set_language_from_url() in views.py
- 404 bei Sprachen: Route muss VOR i18n_patterns in realstate/urls.py stehen
- Übersetzung fehlt: Alle 12 Sprachen im {% if %} Block prüfen
