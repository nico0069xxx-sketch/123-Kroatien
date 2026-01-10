# 123-Kroatien.eu - Projektdokumentation fuer Agents

## Stand: Januar 2026

## Was wurde implementiert

### 1. FAQ-System (FERTIG)
- 60 Fragen x 12 Sprachen = 720 FAQs
- Dateien: main/faq_data.json, main/faq_data_{lang}.json
- Uebersetzte Ueberschriften in allen Sprachen
- URLs: /{lang}/{land}/faq/{slug}/

### 2. Marktberichte (FERTIG)
- 8 Regionen x 12 Sprachen = 96 Berichte
- Dateien: main/market_reports_data/{region}_{year}_{lang}.json
- Views: main/content_views.py
- URLs mit uebersetzten Slugs (z.B. /hr/hrvatska/trzisna-izvjesca/)

### 3. Professional-System (IN ARBEIT)
- Models erstellt: main/professional_models.py
- Views erstellt: main/professional_views.py
- Templates erstellt: professional_list.html, professional_detail.html
- URLs fuer alle 5 Kategorien in 12 Sprachen

Kategorien:
- Immobilienmakler (real_estate_agent)
- Bauunternehmen (construction_company)
- Rechtsanwaelte (lawyer)
- Steuerberater (tax_advisor)
- Architekten (architect)

NOCH ZU TUN:
- Registrierungsformulare (nur DE/HR)
- Admin-Panel Konfiguration
- Testdaten erstellen
- Content-Generierung mit OpenAI

## Wichtige Dateien

main/
- views.py (FAQ, Haupt-Views)
- content_views.py (Marktberichte)
- professional_views.py (Professionals)
- professional_models.py (Datenmodelle)
- urls.py (alle URLs)
- faq_data*.json (FAQ Daten)
- market_reports_data/ (Marktberichte)

templates/main/
- faq.html, faq_detail.html
- market_report_list.html, market_report_detail.html
- professional_list.html, professional_detail.html

## Technische Regeln

1. Template-Block heisst 'body' nicht 'content'
2. Base-Template: include/base.html
3. Farben: #003167 (Blau), #c41e3a (Rot)
4. URL-Sprache hat Vorrang vor Session-Sprache

## Sprach-Mappings

COUNTRY_NAMES = {
    ge: kroatien, en: croatia, hr: hrvatska, fr: croatie,
    nl: kroatie, pl: chorwacja, cz: chorvatsko, sk: chorvatsko,
    ru: horvatiya, gr: kroatia, sw: kroatien, no: kroatia
}

COUNTRY_TO_LANG = {
    kroatien: ge, croatia: en, hrvatska: hr, croatie: fr,
    kroatie: nl, chorwacja: pl, chorvatsko: cz, horvatiya: ru,
    kroatia: gr
}

## Koenigsklasse-Regeln (WICHTIG)

- Keine Werbung, keine Superlative
- Neutral, faktisch, professionell
- Keine rechtlichen/steuerlichen Ratschlaege
- 123-Kroatien.eu NIEMALS uebersetzen
- Alle URLs mit uebersetzten Slugs
- Disclaimer Pflicht auf allen Seiten
