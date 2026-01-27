# 123-Kroatien.eu - Projekt-Dokumentation

## Übersicht
Mehrsprachiges Immobilienportal (12 Sprachen) für den kroatischen Markt mit KI-Features.

## Sprachen
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

## Implementierte Features

### Session Januar 2025

#### Registrierung & Navigation
- ✅ Alte `/accounts/register` Route entfernt
- ✅ Footer-Links auf Partner-Landing umgeleitet (HR → postanite-partner, andere → partner-werden)
- ✅ CTA-Button auf HR-Homepage gefixt

#### Chatbot
- ✅ Neuer Button "Frag unseren Experten" (Pill-Form, 12 Sprachen)
- ✅ Bounce-Animation
- ✅ Glossar-Integration (39 Begriffe)

#### KI-Suche
- ✅ Neuer Titel "KI - Immobilien in Kroatien finden" (12 Sprachen)
- ✅ Typewriter-Animation mit Beispielen (12 Sprachen)
- ✅ Inline-Fehlermeldung in Rot (kein Layout-Sprung)

#### UI/Design
- ✅ CSS-Fix: myCard Icons zentriert
- ✅ HR CTA-Button: Umlaufender Lichtpunkt-Animation

#### Performance
- ✅ Automatische Bildkomprimierung bei Upload (WebP, max 1920x1080, 82%)
- ✅ XML-Import mit Bild-Download und Komprimierung (OpenImmo + Simple XML)
- ✅ Bestehende Bilder komprimiert: **23 MB → 2 MB** (90% gespart)

## Architektur

### Technologie
- **Backend:** Django (Python)
- **Datenbank:** SQLite (dev), PostgreSQL (prod)
- **Bildverarbeitung:** Pillow (automatische Komprimierung zu WebP)

### Wichtige Dateien
- `listings/image_utils.py` - Bildkomprimierung
- `main/xml_import.py` - XML-Import (OpenImmo + Simple)
- `main/chatbot.py` - KI-Chatbot mit Glossar
- `main/context_processors.py` - Übersetzungen

### Übersetzungssystem
- **UI-Texte:** `pages.models.Translation` (name, page, 12 Sprachfelder)
- **Listing-Inhalte:** JSON-Felder pro Sprache im Listing-Model
- **On-Demand:** OpenAI-Übersetzung wenn Übersetzung fehlt

## Offene Punkte

### P1 (Hoch)
- XML-Import testen mit echtem Makler-Feed

### P2 (Mittel)
- Glossar erweitern
- Fragile Django Migrations (technische Schulden)

### P3 (Niedrig)
- Automatische Sitemap-Aktualisierung bei neuen Listings
- base.html Schema mehrsprachig machen

## Credentials
- Projekt läuft lokal auf Mac M1
- GitHub: github.com/nico0069xxx-sketch/123-Kroatien
- OpenAI API Key in `.env`

## Workflow
1. Immer Branch erstellen: `git checkout -b feature/beschreibung`
2. Nie direkt auf main arbeiten
3. Nach Änderungen: `git add . && git commit -m "..." && git push`
4. Merge: `git checkout main && git merge feature/... && git push origin main`
