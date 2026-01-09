# Real Estate Django - Projekt Dokumentation

## Projektübersicht
Kroatische Immobilien-Plattform mit 12-Sprachen-Support und KI-generiertem Content.

**Besitzer:** Nik (jorgallmannsberger)
**Kommunikation:** Deutsch (informell, "du")
**Technisches Level:** Laie - braucht jeden Befehl einzeln, einfach und kopierbar

---

## KRITISCH: Lokale Entwicklungsumgebung

### Ordner-Struktur beim User
```
~/Desktop/
├── real-estate-django-ALTmain/     # ← HAUPTPROJEKT (hier arbeitet der User!)
├── real-estate-django-ALTmain 2/   # Backup
└── restore_from_ssd/
    └── real-estate-django-main/    # Alter Restore (NICHT AKTUELL)
```

### Cloud vs. Lokal - UNTERSCHIEDLICHE ORDNERNAMEN!
- **Cloud (Emergent):** `/app/real-estate-django-main/`
- **Lokal beim User:** `~/Desktop/real-estate-django-ALTmain/`

**WICHTIG:** Der Sync zwischen Cloud und Lokal funktioniert NICHT automatisch!
Dateien müssen manuell übertragen werden.

---

## Dateien zum User übertragen - WORKFLOW

### Methode: Zip-Download (EMPFOHLEN)

1. **Dateien in Zip packen:**
```bash
cd /app && mkdir -p update_folder/[app_name]
cp real-estate-django-main/[app]/[file.py] update_folder/[app_name]/
cd update_folder && zip -r ../update.zip .
cd .. && rm -rf update_folder
cp update.zip frontend/public/
```

2. **Download-URL generieren:**
```
https://[preview-url]/update.zip
```

3. **Befehle für User (EINZELN, EINFACH):**
```bash
# 1. Download
cd ~/Desktop && curl -o update.zip https://[preview-url]/update.zip

# 2. Entpacken
unzip update.zip -d temp_folder

# 3. Kopieren
cp temp_folder/[app_name]/* real-estate-django-ALTmain/[app_name]/

# 4. Aufräumen
rm -rf temp_folder update.zip
```

### WICHTIG für User-Befehle:
- KEINE langen Multi-Line Commands (Terminal hängt!)
- KEINE heredocs (`<< 'EOF'`)
- KEINE komplexen sed/awk Befehle
- Immer `python3` statt `python`
- Immer `pip3` statt `pip`

---

## Projekt-Architektur

### Django Apps
```
real-estate-django-ALTmain/
├── accounts/           # User/Agent Management
│   ├── models.py       # Agent Model (mit 12 Beschreibungsfeldern)
│   ├── admin.py        # Agent Admin mit KI-Action
│   └── ai_content_generator.py  # KI für Agents
│
├── main/               # Hauptapp
│   ├── models.py       # StaticContent Model
│   ├── professional_models.py  # Professional, ProfessionalContent
│   ├── admin.py        # Professional Admin mit KI-Action
│   └── ai_content_generator.py  # KI für Professionals
│
├── listings/           # Immobilien-Inserate
├── pages/              # Statische Seiten, Translations
├── contacts/           # Kontaktformulare
└── realtors/           # (Legacy, nicht aktiv verwendet)
```

### Wichtige Models

#### 1. Agent (accounts/models.py)
```python
class Agent:
    # Basis-Daten
    user, first_name, last_name, email, company_name, city, country
    
    # KI-generierte Beschreibungen (12 Sprachen)
    description_en, description_de, description_fr, description_gr,
    description_hr, description_pl, description_cz, description_ru,
    description_sw, description_no, description_sk, description_nl
```

#### 2. Professional (main/professional_models.py)
```python
class Professional:
    # = "Registrierung" im Admin
    name, professional_type, email, city, region
    # Types: real_estate_agent, construction_company, lawyer, tax_advisor, architect

class ProfessionalContent:
    # Mehrsprachige KI-Inhalte
    professional (FK), language
    profile_summary, areas_of_activity, typical_situations
    working_approach, meta_title, meta_description, verification_statement
```

#### 3. Translation (pages/models.py)
```python
class Translation:
    # Statische UI-Übersetzungen
    name, page
    english_content, german_content, french_content, greek_content,
    croatian_content, polish_content, czech_content, russian_content,
    swedish_content, norway_content, slovak_content, dutch_content
```

---

## KI-Content-Generierung

### Technologie
- **Library:** `emergentintegrations`
- **Model:** OpenAI GPT-4o
- **API Key:** `sk-emergent-113674f2aA7337d756` (Emergent Universal Key)

### Installation
```bash
pip3 install emergentintegrations --extra-index-url https://d33sy5i8bnduwe.cloudfront.net/simple/
```

### Verwendung im Admin
1. Gehe zu Admin Panel (`/admin/`)
2. Wähle Einträge aus (Agent oder Registrierung)
3. Aktion: "KI-Content generieren (12 Sprachen)"
4. Ausführen

### Code-Struktur (ai_content_generator.py)
```python
from emergentintegrations.llm.openai import LlmChat, UserMessage

async def _generate_content_async(...):
    llm = LlmChat(
        api_key=EMERGENT_LLM_KEY,
        session_id=session_id,
        system_message=system_message
    ).with_model("openai", "gpt-4o").with_params(temperature=0.7, max_tokens=1500)
    
    response = await llm.send_message(UserMessage(text=prompt))
    return response

def generate_content_sync(professional):
    # Wrapper für Django's sync context
    loop = asyncio.new_event_loop()
    result = loop.run_until_complete(_generate_content_async(...))
    loop.close()
    return result
```

---

## 12 Unterstützte Sprachen

| Code | Sprache | Django Code |
|------|---------|-------------|
| ge | Deutsch | ge |
| en | Englisch | en |
| fr | Französisch | fr |
| gr | Griechisch | gr |
| hr | Kroatisch | hr |
| pl | Polnisch | pl |
| cz | Tschechisch | cz |
| ru | Russisch | ru |
| sw | Schwedisch | sw |
| no | Norwegisch | no |
| sk | Slowakisch | sk |
| nl | Niederländisch | nl |

---

## Bekannte Issues & Lösungen

### 1. Terminal hängt bei langen Befehlen
**Lösung:** Kurze, einzelne Befehle verwenden

### 2. `pip` nicht gefunden
**Lösung:** `pip3` verwenden

### 3. `python` nicht gefunden
**Lösung:** `python3` verwenden

### 4. Async-Fehler mit Django ORM
**Lösung:** Neuen Event Loop erstellen:
```python
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
try:
    result = loop.run_until_complete(async_function())
finally:
    loop.close()
```

### 5. Dateien kommen nicht beim User an
**Lösung:** Cloud und Lokal sind NICHT gesynct - Zip-Download verwenden

---

## Migrations nach Model-Änderungen

```bash
cd ~/Desktop/real-estate-django-ALTmain
python3 manage.py makemigrations [app_name]
python3 manage.py migrate
```

---

## Server starten/stoppen

```bash
# Starten
cd ~/Desktop/real-estate-django-ALTmain
python3 manage.py runserver

# Stoppen
Ctrl+C
```

---

## Erledigte Features (Stand: Januar 2026)

- [x] Multilingual Navigation (12 Sprachen)
- [x] TOTP 2-Faktor-Authentifizierung
- [x] GDPR Cookie Banner
- [x] XML Interface für Listings
- [x] SEO-optimierte URLs
- [x] KI-Content für Agents (12 Sprachen)
- [x] KI-Content für Professionals/Registrierungen (12 Sprachen)
- [x] Automatische Sprachanzeige auf Professional-Profilseiten (URL-basiert)
- [x] Übersetzte Überschriften auf Professional-Detailseiten (alle 12 Sprachen)

---

## Offene Tasks

### 🔴 P0 - Kritisch
- [ ] Font Awesome Icons auf Homepage fixen (zwei `static/` Ordner verursachen Pfad-Probleme)

### 🟠 P1 - Wichtig  
- [ ] Language Switcher Bug: Leitet auf Homepage statt aktuelle Seite um

### 🟡 P2 - Blockiert
- [ ] Email-Benachrichtigungen fixen (Gmail Credentials benötigt)

### 📌 Zukünftig
- [ ] KI Smart-Search Feature
- [ ] Übersetzungssysteme im Code refactoren

---

## Bekannte Bugs (Stand: Juni 2025)

### Bug 1: Font Awesome Icons fehlen
- **Problem:** Icons wie `fa-comments-o` werden auf Homepage nicht angezeigt
- **Ursache:** Zwei separate `static/` Ordner (`static/` und `realstate/static/`) mit falschen Pfaden
- **Fix:** `STATICFILES_DIRS` in `settings.py` korrigieren + `collectstatic` ausführen

### Bug 2: Language Switcher Redirect
- **Problem:** Von `/de/property-details/2/` wird man bei Sprachwechsel auf `/hr/` statt `/hr/property-details/2/` geleitet
- **Fix:** Regex in `set_language_from_url` View in `main/views.py` anpassen

---

## Kontakt & Support

Bei Problemen: User kommuniziert auf Deutsch, braucht einfache Schritt-für-Schritt Anleitungen.
