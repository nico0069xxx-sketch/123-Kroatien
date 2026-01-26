# Automatische Listing-Übersetzung - Fertige Lösung

## Problem
Die Listing-Inhalte (Titel, Beschreibung) werden nur für DE, EN, FR angezeigt.
Für PL, CZ, SK, RU, SW, NO wird der deutsche Fallback gezeigt, weil die `_content` Felder leer sind.

## Lösung
Die View so ändern, dass sie automatisch übersetzt wenn eine Sprache besucht wird und die Übersetzung noch nicht existiert.

---

## Schritt 1: Backup erstellen

```bash
cd ~/Desktop/real-estate-django-ALTmain && cp main/views.py main/views.py.backup
```

---

## Schritt 2: Auto-Translate Script erstellen

```bash
cat > ~/Desktop/real-estate-django-ALTmain/fix_auto_translate.py << 'SCRIPT_END'
#!/usr/bin/env python3
"""
Fügt automatische Übersetzung zur home View hinzu.
Wenn ein Benutzer eine Sprache besucht und die Übersetzung fehlt,
wird sie automatisch generiert und in der DB gespeichert.
"""

filepath = "main/views.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Import für translation_service hinzufügen (falls nicht vorhanden)
if "from main.translation_service import" not in content:
    # Finde die Import-Sektion und füge hinzu
    import_line = "from main.translation_service import translate_text, LANGUAGES"
    
    # Nach "from django.utils import translation" einfügen
    old_import = "from django.utils import translation"
    new_import = old_import + "\n" + import_line
    content = content.replace(old_import, new_import)
    print("✅ Import hinzugefügt")

# 2. Hilfsfunktion für auto-translate hinzufügen
helper_function = '''
# Auto-translate Hilfsfunktion
def get_or_create_translation(listing, lang_code, field_name):
    """Holt Übersetzung aus DB oder erstellt sie mit OpenAI"""
    import json
    
    existing_content = getattr(listing, field_name, None)
    if existing_content:
        try:
            return json.loads(existing_content)
        except:
            pass
    
    # Keine Übersetzung vorhanden - erstelle eine
    lang_names = {
        'german_content': 'Deutsch', 'english_content': 'Englisch',
        'french_content': 'Französisch', 'greek_content': 'Griechisch',
        'croatian_content': 'Kroatisch', 'polish_content': 'Polnisch',
        'czech_content': 'Tschechisch', 'russian_content': 'Russisch',
        'swedish_content': 'Schwedisch', 'norway_content': 'Norwegisch',
        'slovak_content': 'Slowakisch', 'dutch_content': 'Niederländisch',
    }
    
    target_lang = lang_names.get(field_name, 'Englisch')
    
    try:
        # Übersetze Titel und Beschreibung
        translated_title = translate_text(listing.property_title or '', target_lang)
        translated_desc = translate_text(listing.property_description or '', target_lang)
        
        if translated_title and translated_desc:
            json_content = {
                "property_title": translated_title,
                "property_description": translated_desc,
                "property_type": listing.property_type,
                "property_status": listing.property_status,
                "address": listing.address,
                "bathrooms": float(listing.bathrooms) if listing.bathrooms else 0,
                "bedrooms": listing.bedrooms,
                "floors": listing.floors,
                "area": listing.area,
                "size": float(listing.size) if listing.size else 0,
                "property_price": listing.property_price
            }
            
            # In DB speichern für nächstes Mal
            setattr(listing, field_name, json.dumps(json_content, ensure_ascii=False))
            listing.save(update_fields=[field_name])
            print(f"✅ Übersetzung erstellt und gespeichert: {field_name}")
            
            return json_content
    except Exception as e:
        print(f"❌ Übersetzungsfehler für {field_name}: {e}")
    
    # Fallback auf get_json()
    return listing.get_json()

'''

# Prüfe ob die Funktion schon existiert
if "def get_or_create_translation" not in content:
    # Füge nach den Imports ein (vor der ersten View-Funktion)
    # Suche nach "def home(" und füge davor ein
    insert_pos = content.find("def home(")
    if insert_pos > 0:
        content = content[:insert_pos] + helper_function + "\n" + content[insert_pos:]
        print("✅ Hilfsfunktion hinzugefügt")

# 3. Die bestehende Logik in der home View ersetzen
# Alte Logik für jede Sprache ersetzen

replacements = [
    # Polish
    ('listing.json_content = json.loads(listing.polish_content) if listing.polish_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "pl", "polish_content")'),
    # Czech
    ('listing.json_content = json.loads(listing.czech_content) if listing.czech_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "cz", "czech_content")'),
    # Russian
    ('listing.json_content = json.loads(listing.russian_content) if listing.russian_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "ru", "russian_content")'),
    # Swedish
    ('listing.json_content = json.loads(listing.swedish_content) if listing.swedish_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "sw", "swedish_content")'),
    # Norwegian
    ('listing.json_content = json.loads(listing.norway_content) if listing.norway_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "no", "norway_content")'),
    # Slovak
    ('listing.json_content = json.loads(listing.slovak_content) if listing.slovak_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "sk", "slovak_content")'),
    # Dutch
    ('listing.json_content = json.loads(listing.dutch_content) if listing.dutch_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "nl", "dutch_content")'),
    # Greek
    ('listing.json_content = json.loads(listing.greek_content) if listing.greek_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "gr", "greek_content")'),
    # Croatian
    ('listing.json_content = json.loads(listing.croatian_content) if listing.croatian_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "hr", "croatian_content")'),
    # French
    ('listing.json_content = json.loads(listing.french_content) if listing.french_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "fr", "french_content")'),
    # English
    ('listing.json_content = json.loads(listing.english_content) if listing.english_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "en", "english_content")'),
    # German
    ('listing.json_content = json.loads(listing.german_content) if listing.german_content else listing.get_json()',
     'listing.json_content = get_or_create_translation(listing, "ge", "german_content")'),
]

replaced_count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        replaced_count += 1

print(f"✅ {replaced_count} Stellen ersetzt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ main/views.py wurde aktualisiert!")
print("   Übersetzungen werden jetzt automatisch erstellt wenn eine Sprache besucht wird.")
SCRIPT_END
```

---

## Schritt 3: Script ausführen

```bash
cd ~/Desktop/real-estate-django-ALTmain && python3 fix_auto_translate.py
```

---

## Schritt 4: Server neu starten und testen

```bash
cd ~/Desktop/real-estate-django-ALTmain && python3 manage.py runserver
```

Dann im Browser:
1. Geh auf `/pl/` (Polnisch) - die Übersetzung wird automatisch erstellt
2. Geh auf `/cz/` (Tschechisch) - die Übersetzung wird automatisch erstellt
3. usw.

Die Übersetzungen werden in der Datenbank gespeichert, sodass sie beim nächsten Besuch sofort geladen werden.

---

## Was wurde heute gelöst:

1. ✅ Dummy-Listings ausgeblendet (nur ID 1 "Villa am Meer" sichtbar)
2. ✅ Badge "Kaufen/Mieten" zeigt jetzt übersetzte Texte in allen 12 Sprachen
3. ✅ Filter-Übersetzungen hinzugefügt
4. 🔄 Automatische Listing-Übersetzung (dieses Script)

---

## Nächste Schritte (Backlog):

- Preisfilter korrigieren (Sale bis 15M€, Rent ab 300€)
- Weitere Glossar-Begriffe hinzufügen
- Schema.org auf anderen Seiten erweitern
