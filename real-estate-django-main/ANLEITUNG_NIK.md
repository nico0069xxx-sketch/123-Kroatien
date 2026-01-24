# ANLEITUNG FÜR NIK - Sitemap Fix

## Status: Bereit zum Testen

Ich habe alle Änderungen auf dem Dev-Server vorbereitet. Hier ist was du tun musst:

---

## Problem 1: Header-Sprachumschalter funktioniert nicht

Der sed-Befehl hat die Funktion auf eine Zeile komprimiert, aber möglicherweise gibt es noch Reste der alten Funktion.

### Lösung:

```bash
cd ~/Desktop/real-estate-django-ALTmain

# Prüfe wie die Funktion aktuell aussieht:
grep -A10 "function changelanguage" templates/include/base.html
```

Die Funktion sollte so aussehen (NUR EINE ZEILE):
```javascript
function changelanguage(value) { window.location.href = "/set-language/" + value + "/"; }
```

Falls die alte Funktion noch teilweise da ist, lösche die alten Zeilen manuell mit nano.

---

## Problem 2: Dienstleister nicht übersetzt

Die sitemap.html auf deinem Mac hat noch `{{ dropdown_realtor }}` etc., die nicht für alle Sprachen existieren.

### Lösung:

Ersetze in `templates/main/sitemap.html` den Dienstleister-Block.

**SUCHE nach:**
```html
<li><a href="/{{ language }}/{{ country_name }}/{{ url_realtor }}/">{{ dropdown_realtor }}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_contractor }}/">{{ dropdown_contractor }}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_lawyer }}/">{{ dropdown_lawyer }}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_tax_advisor }}/">{{ dropdown_tax_advisor }}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_architect }}/">{{ dropdown_architect }}</a></li>
```

**ERSETZE durch:**
```html
<li><a href="/{{ language }}/{{ country_name }}/{{ url_realtor }}/">{% if language == 'hr' %}Agent za nekretnine{% elif language == 'en' %}Real Estate Agent{% elif language == 'fr' %}Agent immobilier{% elif language == 'nl' %}Makelaar{% elif language == 'pl' %}Agent nieruchomości{% elif language == 'cz' %}Realitní makléř{% elif language == 'sk' %}Realitný maklér{% elif language == 'ru' %}Риэлтор{% elif language == 'gr' %}Μεσίτης{% elif language == 'sw' %}Fastighetsmäklare{% elif language == 'no' %}Eiendomsmegler{% else %}Immobilienmakler{% endif %}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_contractor }}/">{% if language == 'hr' %}Građevinar{% elif language == 'en' %}Building Contractor{% elif language == 'fr' %}Entrepreneur{% elif language == 'nl' %}Aannemer{% elif language == 'pl' %}Wykonawca{% elif language == 'cz' %}Stavitel{% elif language == 'sk' %}Staviteľ{% elif language == 'ru' %}Подрядчик{% elif language == 'gr' %}Κατασκευαστής{% elif language == 'sw' %}Byggentreprenör{% elif language == 'no' %}Byggentreprenør{% else %}Bauunternehmer{% endif %}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_lawyer }}/">{% if language == 'hr' %}Odvjetnik{% elif language == 'en' %}Lawyer{% elif language == 'fr' %}Avocat{% elif language == 'nl' %}Advocaat{% elif language == 'pl' %}Prawnik{% elif language == 'cz' %}Právník{% elif language == 'sk' %}Právnik{% elif language == 'ru' %}Адвокат{% elif language == 'gr' %}Δικηγόρος{% elif language == 'sw' %}Advokat{% elif language == 'no' %}Advokat{% else %}Rechtsanwalt{% endif %}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_tax_advisor }}/">{% if language == 'hr' %}Porezni savjetnik{% elif language == 'en' %}Tax Advisor{% elif language == 'fr' %}Conseiller fiscal{% elif language == 'nl' %}Belastingadviseur{% elif language == 'pl' %}Doradca podatkowy{% elif language == 'cz' %}Daňový poradce{% elif language == 'sk' %}Daňový poradca{% elif language == 'ru' %}Налоговый консультант{% elif language == 'gr' %}Φοροτεχνικός{% elif language == 'sw' %}Skatterådgivare{% elif language == 'no' %}Skatterådgiver{% else %}Steuerberater{% endif %}</a></li>
<li><a href="/{{ language }}/{{ country_name }}/{{ url_architect }}/">{% if language == 'hr' %}Arhitekt{% elif language == 'en' %}Architect{% elif language == 'fr' %}Architecte{% elif language == 'nl' %}Architect{% elif language == 'pl' %}Architekt{% elif language == 'cz' %}Architekt{% elif language == 'sk' %}Architekt{% elif language == 'ru' %}Архитектор{% elif language == 'gr' %}Αρχιτέκτονας{% elif language == 'sw' %}Arkitekt{% elif language == 'no' %}Arkitekt{% else %}Architekt{% endif %}</a></li>
```

---

## Testen

```bash
python3 manage.py runserver
```

1. Öffne http://127.0.0.1:8000/sitemap
2. Wechsle die Sprache OBEN im Header → Header, Footer UND Inhalt sollten wechseln
3. Wechsle die Sprache UNTEN auf der Sitemap → Sollte genauso funktionieren
4. Prüfe: Sind die Dienstleister (Immobilienmakler, etc.) jetzt übersetzt?

---

## Git Commit (wenn alles funktioniert)

```bash
git add templates/include/base.html templates/main/sitemap.html
git commit -m "fix: Sitemap 12-Sprachen-Übersetzungen + Header-Sprachumschalter"
git push origin fix/sitemap-all-languages
```
