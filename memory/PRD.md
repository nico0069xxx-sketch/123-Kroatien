# 123-KROATIEN.EU - Projekt Status

## Original Problem Statement
Der Benutzer (Nik) entwickelt ein 12-sprachiges Django Real Estate Portal. Ziele:
- GEO (Generative Engine Optimization) für AI-Suchmaschinen
- Intelligenter Chatbot mit Glossar-Integration
- Saubere FAQ-Sektion

## Kommunikation
- **Sprache:** Deutsch, informell ("du")
- **Workflow:** Einzelne, kopierbare Bash-Befehle
- **System:** Mac M1, lokales Django-Projekt

---

## ✅ Erledigte Aufgaben (Diese Session)

### 1. Dummy-Listings ausgeblendet
- IDs 2, 3, 4, 5, 6, 7 auf `is_published=False` gesetzt
- Nur ID 1 ("Villa am Meer", Test Makler, 450.000€) wird angezeigt

### 2. Badge "Zu verkaufen" gefixt
- Problem: `{{listing.json_content.property_status}}` war leer
- Lösung: Template geändert auf Bedingung mit übersetzten Variablen
- Script: `fix_badge.py`

### 3. Filter-Übersetzungen hinzugefügt
- Neue Variablen: `filter_property_status`, `filter_for_sale`, `filter_For_Rent`
- Für alle 12 Sprachen in `main/context_processors.py`
- Script: `fix_filter_translations.py`

---

## 🔄 In Arbeit

### Automatische Listing-Übersetzung
- **Problem:** Listings werden nur für DE, EN, FR übersetzt. PL, CZ, SK, RU, SW, NO zeigen Deutsch.
- **Ursache:** Die `_content` Felder in der DB sind leer, der Fallback zeigt Deutsch.
- **Lösung:** View ändern für on-demand Übersetzung mit OpenAI
- **Script:** Vorbereitet in `/app/memory/SOLUTION_AUTO_TRANSLATE.md`
- **Status:** Script erstellt, wartet auf Ausführung durch Benutzer

---

## 📋 Backlog (Priorisiert)

### P1 - Hoch
- [ ] Preisfilter korrigieren: Sale bis 15M€, Rent ab 300€
- [ ] Auto-Translate Script ausführen und testen

### P2 - Mittel
- [ ] Glossar erweitern (weitere Begriffe)
- [ ] Schema.org auf anderen Seiten (RealEstateListing)
- [ ] `base.html` Schema mehrsprachig machen

### P3 - Niedrig (Technische Schulden)
- [ ] Django Migrations reparieren (sqlite3.OperationalError)
- [ ] Chatbot-Styling verbessern
- [ ] "White Listing" Feature für Premium-Objekte

---

## 🏗️ Architektur

### Dateien (Geändert in dieser Session)
- `main/context_processors.py` - Filter-Übersetzungen hinzugefügt
- `templates/main/home.html` - Badge gefixt

### Dateien (Vorbereitet für Änderung)
- `main/views.py` - Auto-Translate Logik (Script ready)

### Wichtige Modelle
- `listings.models.Listing` - Hauptmodell für Immobilien
  - `property_status`: "Zu verkaufen" / "Zu mieten"
  - `german_content`, `english_content`, etc.: JSON mit übersetzten Inhalten
  - `is_published`: Boolean für Sichtbarkeit

### Übersetzungs-System
- `main/translation_service.py` - OpenAI-basierte Übersetzung
- `main/templatetags/translate_filters.py` - Template-Filter für on-the-fly Übersetzung

---

## 🔑 Credentials (Im Projekt)
- OpenAI API Key: In `.env` als `OPENAI_API_KEY`
- Emergent LLM Key: Hardcoded in `listing_description_ai.py`

---

## ⚠️ Bekannte Probleme

### Fragile Migrations
- `makemigrations` riskant - DB Schema evtl. nicht synchron
- Workaround: `.update()` statt `.delete()` verwenden

### TextEdit Korruption
- Niks TextEdit-App kann Templates beschädigen
- Workaround: Python-Scripts für Dateiänderungen verwenden
