# 123-KROATIEN.EU - AGENT BRIEFING

## 🔒 BASELINE & WORKFLOW
- **BASELINE:** 9ec9d9a on main — DO NOT BREAK
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
Wenn Views außerhalb von i18n_patterns definiert sind, MUSS die Sprache manuell gesetzt werden:
```python
def my_view(request):
    path = request.path
    lang_code = path.split('/')[1] if len(path.split('/')) > 1 else 'ge'
    if lang_code in ['ge', 'en', 'hr', 'fr', 'nl', 'pl', 'cz', 'sk', 'ru', 'gr', 'sw', 'no']:
        translation.activate(lang_code)
        request.LANGUAGE_CODE = lang_code
        request.session['site_language'] = lang_code  # WICHTIG für Context Processor!
    return render(request, 'template.html')
3. Übersetzungen in Templates
Problem: {% if language == 'hr' %}...{% elif %}...{% endif %} überall
Bei Template-Übersetzungen IMMER alle 12 Sprachen prüfen
{{ language }} Variable kommt aus main/context_processors.py → set_language()
Diese liest aus request.session['site_language'] - daher MUSS die Session gesetzt werden!
4. JavaScript API-Aufrufe
NIEMALS hardcoded /ge/api/... verwenden!
IMMER {{ language }} Template-Variable nutzen: fetch('/{{ language }}/api/...')
Betrifft: Smart-Search, Experten-Finder, Makler-Portal, etc.
5. Dienstleister-Bereich
Registrierung, Makler-Portal, etc. sind NUR für DE und HR verfügbar
In Sitemap ausblenden für andere Sprachen: {% if language == 'ge' or language == 'hr' %}
📁 WICHTIGE DATEIEN
realstate/urls.py - Haupt-URL-Routing (statische Seiten OBEN, i18n_patterns am ENDE!)
main/urls.py - App-URLs (Reihenfolge wichtig, content_urlpatterns am Anfang)
main/content_urls.py - Generiert dynamisch URLs für News, Adressen, Marktberichte
main/glossary_urls.py - Glossar-URLs für alle 12 Sprachen
main/context_processors.py - Globale Template-Variablen inkl. Cookie-Übersetzungen
main/views.py - set_language_from_url() und statische Seiten-Views
templates/include/base.html - changelanguage() JavaScript Zeile ~379
🔧 GELÖSTE PROBLEME (Januar 2026)
Sitemap-Links 404
Problem: Links auf Sitemap führten zu 404 für viele Sprachen
Ursache: URLs waren nur für DE/HR definiert, nicht für alle 12 Sprachen
Lösung: content_urlpatterns in main/content_urls.py generiert dynamisch URLs für alle Sprachen
Statische Seiten falsche Sprache
Problem: /fr/agb/ zeigte deutschen Inhalt
Ursache: Views setzten request.session['site_language'] nicht
Lösung: Alle statischen Seiten-Views (imprint, agb, sitemap, etc.) setzen jetzt Session-Sprache
KI-Suche falsche Sprache
Problem: KI-Suche zeigte immer deutsche Ergebnisse
Ursache: JavaScript fetch() war hardcoded auf /ge/api/...
Lösung: Alle fetch()-Aufrufe nutzen jetzt {{ language }} Template-Variable
✅ START CHECKLISTE

cd ~/Desktop/real-estate-django-ALTmain
git fetch --all
git status (MUSS SAUBER SEIN)
git checkout main && git pull origin main
git checkout -b fix/beschreibung-hier (NEUER Branch VOR jeder Arbeit)
🚫 VERBOTEN

Niemals direkt auf main arbeiten
Niemals .env, db.sqlite3, media/ committen
Niemals iCloud als Source nutzen
Niemals Model ändern ohne Migration
Niemals hardcoded /ge/ in JavaScript fetch() verwenden
✅ ENDE CHECKLISTE

python3 manage.py check
git add . && git commit -m "beschreibung"
git push origin BRANCH-NAME
AGENT_BRIEFING.md aktualisieren falls nötig
git status (MUSS clean sein)
🔧 HÄUFIGE PROBLEME & LÖSUNGEN

Problem	Lösung
Sprachwechsel kaputt	Prüfe changelanguage() in base.html und set_language_from_url() in views.py
404 bei Sprachen	Route muss VOR i18n_patterns in realstate/urls.py stehen
Übersetzung fehlt	Alle 12 Sprachen im {% if %} Block prüfen
Falsche Sprache angezeigt	View muss request.session['site_language'] setzen
API gibt falsche Sprache	JavaScript fetch() muss {{ language }} nutzen, nicht /ge/
Dienstleister für alle sichtbar	Block mit {% if language == 'ge' or language == 'hr' %} umschließen
