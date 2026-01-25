# HANDOFF - 25. Januar 2026

## Original Problem Statement
Nik entwickelt ein großes, mehrsprachiges Django-basiertes Immobilienportal (123-kroatien.eu). Die Session konzentrierte sich auf die Reparatur der URL-Architektur für alle 12 Sprachen, insbesondere die Sitemap-Links die zu 404-Fehlern führten.

## User Context
- **Name:** Nik (bitte duzen, Deutsch sprechen)
- **System:** Apple Mac M1, Terminal, Safari
- **Skill-Level:** Laie - JEDEN Befehl einzeln und kopierbar geben
- **Lokales Repo:** `~/Desktop/real-estate-django-ALTmain`
- **Branch:** `fix/url-i18n-architecture`

## Unterstützte Sprachen (12)
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

---

## Was in dieser Session repariert wurde ✅

### 1. URL-Routing für alle 12 Sprachen
- **Problem:** Sitemap-Links führten zu 404-Fehlern
- **Ursache:** URLs waren nur für DE/HR definiert, nicht für alle 12 Sprachen
- **Lösung:** `content_urlpatterns` generiert jetzt dynamisch URLs für alle Sprachen

### 2. Sitemap Template korrigiert
- **Problem:** `{{ country_name }}` zeigte falsches Land (z.B. "croatie" statt "kroatia" für Norwegisch)
- **Lösung:** `{{ country_name }}` durch sprachspezifische `{% if language == '...' %}` Blöcke ersetzt

### 3. Experten-Finder URLs
- **Problem:** Sitemap verlinkte auf `/experten-finder/` für alle Sprachen
- **Lösung:** Sprachspezifische URLs hinzugefügt (z.B. `/no/kroatia/ekspert-soker/`)

### 4. Reihenfolge der URL-Patterns korrigiert
- **Problem:** Generische `<str:category>/` Routes fingen spezifische URLs ab
- **Lösung:** `content_urlpatterns` am ANFANG, generische Routes am ENDE

---

## Was noch offen ist ❌

### P0 - Kritisch
1. **Statische Seiten für alle Sprachen**
   - `/no/imprint/` → 404
   - `/no/agb/` → 404
   - `/no/cancellation-policy/` → 404
   - **Lösung:** In `realstate/urls.py` für alle 12 Sprachen hinzufügen

2. **Registrierung für alle Sprachen**
   - `/no/kroatia/registrering/` → 404
   - **Lösung:** In `realstate/urls.py` für alle 12 Sprachen hinzufügen

3. **Sitemap Slash-Varianten**
   - `/fr/sitemap/` (mit Slash) → 404
   - Nur `/fr/sitemap` (ohne Slash) funktioniert
   - **Lösung:** Slash-Varianten für alle 12 Sprachen hinzufügen

### P1 - Hoch
4. **Glossar-Detail Sprachwechsel**
   - Beim Wechsel von `/ge/kroatien/glossar/alleineigentum/` zu EN kommt 404
   - Der Slug muss übersetzt werden (z.B. `alleineigentum` → `sole-ownership`)
   - **Lösung:** `set_language_from_url()` in `main/views.py` muss Glossar-Slugs aus DB übersetzen

5. **Cookie-Banner Texte**
   - Texte fehlen manchmal beim ersten Laden
   - Wurde in dieser Session nicht adressiert

### P2 - Mittel
6. **KI-Suche zeigt falschen Inhalt**
   - `/ge/#ki-suche` zeigt deutschen Inhalt auch nach Sprachwechsel
   - JavaScript-Problem

---

## Geänderte Dateien

### 1. `realstate/urls.py`
- Imports für `matching_views`, `content_urlpatterns` hinzugefügt
- `content_urlpatterns` eingebunden
- Experten-Finder URLs für alle 12 Sprachen hinzugefügt
- Generische `<str:category>/` Routes für alle 12 Sprachen hinzugefügt

### 2. `main/urls.py`
- `content_urlpatterns` am Anfang eingebunden: `urlpatterns = content_urlpatterns + [...]`
- Generische Routes am Ende: `] + glossary_urlpatterns + [...]`

### 3. `main/content_urls.py`
- Generiert dynamisch URLs für News, Adressen, Marktberichte
- Nutzt `COUNTRY_NAMES` aus `glossary_models.py`

### 4. `templates/main/sitemap.html`
- `{{ country_name }}` ersetzt durch sprachspezifische Übersetzungen
- `experten-finder` ersetzt durch sprachspezifische URLs

---

## Wichtige Code-Strukturen

### URL-Segment Übersetzungen (aus content_urls.py)
```python
NEWS_URLS = {
    "ge": "nachrichten", "en": "news", "hr": "vijesti", "fr": "actualites",
    "nl": "nieuws", "pl": "wiadomosci", "cz": "zpravy", "sk": "spravy",
    "ru": "novosti", "gr": "nea", "sw": "nyheter", "no": "nyheter",
}

ADDRESS_URLS = {
    "ge": "wichtige-adressen", "en": "important-addresses", "hr": "vazne-adrese",
    "fr": "adresses-importantes", "nl": "belangrijke-adressen", "pl": "wazne-adresy",
    "cz": "dulezite-adresy", "sk": "dolezite-adresy", "ru": "vazhnye-adresa",
    "gr": "simantikes-dieythynseis", "sw": "viktiga-adresser", "no": "viktige-adresser",
}

MARKET_URLS = {
    "ge": "marktberichte", "en": "market-reports", "hr": "trzisni-izvjestaji",
    "fr": "rapports-marche", "nl": "marktverslagen", "pl": "raporty-rynkowe",
    "cz": "trzni-zpravy", "sk": "trhove-spravy", "ru": "rynochnye-otchety",
    "gr": "anafores-agoras", "sw": "marknadsrapporter", "no": "markedsrapporter",
}
```

### Experten-Finder URLs
```python
EXPERT_FINDER_URLS = {
    "ge": "experten-finder", "en": "expert-finder", "hr": "pronalazac-strucnjaka",
    "fr": "recherche-experts", "nl": "expert-zoeker", "pl": "wyszukiwarka-ekspertow",
    "cz": "vyhledavac-odborniku", "sk": "vyhladavac-odbornikov", "ru": "poisk-ekspertov",
    "gr": "anazhthsh-eidikwn", "sw": "expert-sokare", "no": "ekspert-soker",
}
```

---

## Dateien von Referenz

1. `realstate/urls.py` - Haupt-URL-Routing
2. `main/urls.py` - App-URLs
3. `main/content_urls.py` - Dynamische Content-URLs
4. `main/glossary_urls.py` - Glossar-URLs
5. `main/context_processors.py` - Template-Variablen
6. `main/views.py` - Views inkl. `set_language_from_url()`
7. `templates/main/sitemap.html` - Sitemap-Template
8. `templates/include/base.html` - Base-Template mit Sprachwechsler

---

## Getestete und funktionierende URLs

### Deutsch (ge)
- ✅ `/ge/kroatien/nachrichten/`
- ✅ `/ge/kroatien/wichtige-adressen/`
- ✅ `/ge/kroatien/marktberichte/`
- ✅ `/ge/kroatien/immobilienmakler/`
- ✅ `/ge/kroatien/glossar/`
- ✅ `/ge/kroatien/experten-finder/`

### Englisch (en)
- ✅ `/en/croatia/news/`
- ✅ `/en/croatia/important-addresses/`
- ✅ `/en/croatia/market-reports/`
- ✅ `/en/croatia/real-estate-agents/`
- ✅ `/en/croatia/glossary/`
- ✅ `/en/croatia/expert-finder/`

### Norwegisch (no)
- ✅ `/no/kroatia/nyheter/`
- ✅ `/no/kroatia/viktige-adresser/`
- ✅ `/no/kroatia/markedsrapporter/`
- ✅ `/no/kroatia/eiendomsmeglere/`
- ✅ `/no/kroatia/ordliste/`
- ✅ `/no/kroatia/ekspert-soker/`

### Niederländisch (nl)
- ✅ `/nl/kroatie/nieuws/`
- ✅ `/nl/kroatie/belangrijke-adressen/`
- ✅ `/nl/kroatie/marktverslagen/`
- ✅ `/nl/kroatie/makelaars/`
- ✅ `/nl/kroatie/woordenlijst/`
- ✅ `/nl/kroatie/expert-zoeker/`

---

## Bekannte Fehler (404)

### Statische Seiten
- `/no/imprint/`
- `/no/agb/`
- `/no/cancellation-policy/`
- `/no/kroatia/registrering/`

### Sitemap mit Slash
- `/fr/sitemap/` (ohne Slash funktioniert: `/fr/sitemap`)

---

## Git Status

- **Branch:** `fix/url-i18n-architecture`
- **Letzter Commit:** Änderungen wurden NICHT committed
- **Uncommitted Changes:** `realstate/urls.py`, `main/urls.py`, `templates/main/sitemap.html`

### Befehle zum Committen:
```bash
cd ~/Desktop/real-estate-django-ALTmain
git add .
git commit -m "fix: URL architecture for all 12 languages - sitemap links working"
git push origin fix/url-i18n-architecture
```

---

## Nächste Schritte für den neuen Agenten

1. **ZUERST:** Uncommitted Changes committen (siehe oben)

2. **Statische Seiten fixen:**
   - In `realstate/urls.py` für alle 12 Sprachen hinzufügen:
   - `/xx/imprint/`, `/xx/agb/`, `/xx/cancellation-policy/`

3. **Registrierung fixen:**
   - Registrierungs-URLs für alle 12 Sprachen in `realstate/urls.py`

4. **Sitemap Slash-Varianten:**
   - Für alle 12 Sprachen `/xx/sitemap/` (mit Slash) hinzufügen

5. **Glossar-Detail Sprachwechsel:**
   - `set_language_from_url()` in `main/views.py` erweitern

---

## Warnung für neuen Agenten

⚠️ **WICHTIG:** Die Cloud-Umgebung ist NICHT synchron mit Niks lokalem Repo!
- Immer erst fragen was Nik lokal hat
- Befehle einzeln und kopierbar geben
- Nik ist Laie - keine komplexen Erklärungen

⚠️ **URL-Reihenfolge ist kritisch:**
- Spezifische URLs MÜSSEN VOR generischen `<str:category>/` Routes stehen
- Sonst werden alle URLs von der generischen Route abgefangen

⚠️ **Zwei URL-Dateien:**
- `realstate/urls.py` - Direkte URLs (ohne i18n)
- `main/urls.py` - App-URLs (werden über i18n_patterns eingebunden)
