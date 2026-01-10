# 123-Kroatien.eu - Projektdokumentation

## Uebersicht
Internationale Immobilienplattform fuer Kroatien mit 12 Sprachen und KI/SEO-Optimierung.

## Koenigsklasse-Standards
- Keine Werbung, keine Superlatives
- Neutral, faktisch, professionell
- Keine rechtlichen/steuerlichen Ratschlaege
- Mehrsprachig mit uebersetzten URLs (SEO-Slugs)
- Compliance-konform

## Sprachen (12)
ge, en, hr, fr, nl, pl, cz, sk, ru, gr, sw, no

## URL-Struktur
Format: /{sprache}/{land}/{kategorie}/
Beispiel: /ge/kroatien/immobilienmakler/
         /hr/hrvatska/agencije-za-nekretnine/

## Implementierte Features

### 1. FAQ-System
- 60 Fragen x 12 Sprachen = 720 FAQs
- Uebersetzte Ueberschriften (Kurzantwort, Details, etc.)
- Dateien: main/faq_data.json, main/faq_data_{lang}.json
- Views: main/views.py (faq_detail)

### 2. Marktberichte
- 8 Regionen x 12 Sprachen = 96 Berichte
- Dateien: main/market_reports_data/{region}_{year}_{lang}.json
- Views: main/content_views.py

Regionen: Istrien, Kvarner, Nord-Dalmatien, Mittel-Dalmatien,
Sued-Dalmatien, Zagreb, Slavonien, Lika und Gorski Kotar

### 3. Professional-System
5 Kategorien:
- Immobilienmakler (real_estate_agent)
- Bauunternehmen (construction_company)
- Rechtsanwaelte (lawyer)
- Steuerberater (tax_advisor)
- Architekten (architect)

Models: main/professional_models.py
Views: main/professional_views.py
Templates: templates/main/professional_list.html, professional_detail.html

Registrierung nur DE/HR (fuer kroatische Anbieter)
Anzeige in allen 12 Sprachen (fuer internationale Kaeufer)

## Wichtige Mappings

### Laender-Namen (COUNTRY_NAMES)
ge: kroatien, en: croatia, hr: hrvatska, fr: croatie

### Spracherkennung
1. URL-Land hat Vorrang (fuer korrekte SEO)
2. Fallback: Session-Sprache
3. Default: ge (Deutsch)

## Technische Hinweise
- Django 4.2.1
- Template-Block: block body (nicht content)
- Base-Template: include/base.html
- Farben: #003167 (Blau), #c41e3a (Rot)

Zuletzt aktualisiert: Januar 2025
