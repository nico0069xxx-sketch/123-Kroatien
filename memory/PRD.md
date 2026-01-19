# 123-Kroatien.eu - Immobilienportal PRD

## Original Problem Statement
Der Benutzer (Nik) betreibt ein Django-basiertes Immobilienportal "123-Kroatien.eu" für kroatische Immobilien, das deutsche Kunden ansprechen soll. Das Portal unterstützt 12 Sprachen über ein Translation-System.

## Was in dieser Session erledigt wurde

### ✅ Abgeschlossen:
1. **Social Media Dokumentation (Gruppe B)** - Trilingualer Abschnitt in `templates/professional_portal/anleitung.html` hinzugefügt
2. **Logo-Fix** - `professional.logo` → `professional.company_logo` in 4 Dateien korrigiert
3. **Moderne Property Detail Page** - Neues Template `templates/main/single-detail-modern.html` erstellt mit:
   - Swipe-Galerie für Mobile
   - Thumbnail-Leiste für Desktop
   - Lightbox für Vollbild
   - 8er Specs-Grid (Schlafzimmer, Bad, Fläche, etc.)
   - Kontaktformular
   - Makler-Info
   - OpenStreetMap Karte
   - Responsive Design

### ❌ KRITISCHES PROBLEM - Übersetzungen funktionieren nicht

**Problem:** Die Übersetzungsvariablen werden im neuen Template nicht korrekt angezeigt. Obwohl die Sprache auf Französisch gestellt ist, erscheinen viele Labels auf Deutsch.

**Was NICHT übersetzt wird:**
- Hero: Standort fehlt komplett (Split, Kroatien sollte angezeigt werden)
- "Zurueck" → sollte "Retour" sein
- "ETAGEN" → sollte "Étages" sein
- "OBJEKTART" → sollte "Type de bien" sein
- "STATUS" → sollte "Statut" sein
- "NAME" → sollte "Nom" sein
- "TELEFON" → sollte "Téléphone" sein
- "NACHRICHT" → sollte "Message" sein
- "Senden" → sollte "Envoyer" sein

**Technische Details:**

1. **Übersetzungen existieren in der DB:**
   ```
   label_floors: page='property details', FR='Étages'
   label_garage: page='property details', FR='Garage'
   label_property_type: page='property details', FR='Type de bien'
   label_property_status: page='property details', FR='Statut'
   nav_back: page='property details', FR='Retour'
   contact_name: page='contact', FR='Nom'
   contact_phone: page='contact', FR='Téléphone'
   contact_message: page='contact', FR='Message'
   btn_send_message: page='contact', FR='Envoyer'
   ```

2. **Context Processor (`main/context_processors.py`):**
   - Lädt Übersetzungen aus `pages.models.Translation`
   - Wurde aktualisiert um auch `page='contact'` zu laden
   - Zeile 82: `translations = Translation.objects.filter(page=page) | ... | Translation.objects.filter(page='contact')`

3. **Template (`templates/main/single-detail-modern.html`):**
   - Verwendet Variablen wie `{{ label_floors|default:"Etagen" }}`
   - Die Fallback-Werte werden angezeigt, nicht die DB-Übersetzungen

**Mögliche Ursachen:**
1. Die lokale Datei des Benutzers ist nicht synchron mit den Änderungen
2. Der Context Processor wird nicht für diese View aufgerufen
3. Die Variable-Namen im Template stimmen nicht exakt mit den DB-Namen überein
4. Cache-Problem

**Debug-Vorschläge für nächsten Agenten:**
1. Prüfe ob Context Processor in `realstate/settings.py` unter `TEMPLATES['OPTIONS']['context_processors']` eingetragen ist
2. Prüfe in der View `main/views.py` ob der Context korrekt übergeben wird
3. Teste mit: `{{ label_floors }}` ohne default um zu sehen ob Variable leer ist
4. Prüfe die exakten Variablennamen in der View mit Debug-Output

## Dateistruktur

### Wichtige Dateien:
- `/app/real-estate-django-main/` - Projektroot
- `main/context_processors.py` - Übersetzungslogik
- `main/views.py` - Views inkl. property_details
- `pages/models.py` - Translation Model
- `templates/main/single-detail-modern.html` - Neues Property Template
- `templates/main/single-detail.html` - Altes Property Template (funktioniert!)

### Git-Status:
- Branch: `feature/modern-property-detail` (nicht gepusht)
- Baseline: `9ec9d9a on main`

## Benutzer-Kontext
- Nik arbeitet auf Mac M1 mit Terminal/Safari
- Verwendet `DEBUG=true python3 manage.py runserver`
- Lokal unter `~/Desktop/real-estate-django-ALTmain`
- Alle Befehle als einfache Copy-Paste Terminal-Befehle geben

## Credentials
- Admin: `/nik-verwaltung-2026/` - User: `Nik` / `Admin1234!`
- Gruppe A (Makler): `/accounts/login` - User: `Nik` / `Admin1234!`
- Gruppe B (Professional): `/accounts/login` - User: `archtiket` / `Architekt!123456789`

## Nächste Schritte
1. **PRIORITÄT 1:** Übersetzungsproblem lösen
2. Standort (city, country) im Hero-Bild anzeigen
3. Alle Labels komplett übersetzen
4. Template committen und pushen
5. PR erstellen und mergen

## Sprache
Der Benutzer kommuniziert auf **Deutsch (informell "du")**.
