#!/usr/bin/env python3
"""Fügt automatische Übersetzung zur View hinzu"""

filepath = "main/views.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Import hinzufügen
if "from main.translation_service import" not in content:
    old_import = "from django.utils import translation"
    new_import = old_import + "\nfrom main.translation_service import translate_text"
    content = content.replace(old_import, new_import)
    print("✅ Import hinzugefügt")

# Hilfsfunktion hinzufügen
helper_function = '''
def get_or_create_translation(listing, lang_code, field_name):
    """Holt Übersetzung aus DB oder erstellt sie mit OpenAI"""
    import json
    existing = getattr(listing, field_name, None)
    if existing:
        try:
            return json.loads(existing)
        except:
            pass
    
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
            setattr(listing, field_name, json.dumps(json_content, ensure_ascii=False))
            listing.save(update_fields=[field_name])
            print(f"✅ Übersetzung erstellt: {field_name}")
            return json_content
    except Exception as e:
        print(f"❌ Fehler: {e}")
    return listing.get_json()

'''

if "def get_or_create_translation" not in content:
    pos = content.find("def home(")
    if pos > 0:
        content = content[:pos] + helper_function + "\n" + content[pos:]
        print("✅ Hilfsfunktion hinzugefügt")

# Ersetze die alte Logik
replacements = [
    ('json.loads(listing.polish_content) if listing.polish_content else listing.get_json()',
     'get_or_create_translation(listing, "pl", "polish_content")'),
    ('json.loads(listing.czech_content) if listing.czech_content else listing.get_json()',
     'get_or_create_translation(listing, "cz", "czech_content")'),
    ('json.loads(listing.russian_content) if listing.russian_content else listing.get_json()',
     'get_or_create_translation(listing, "ru", "russian_content")'),
    ('json.loads(listing.swedish_content) if listing.swedish_content else listing.get_json()',
     'get_or_create_translation(listing, "sw", "swedish_content")'),
    ('json.loads(listing.norway_content) if listing.norway_content else listing.get_json()',
     'get_or_create_translation(listing, "no", "norway_content")'),
    ('json.loads(listing.slovak_content) if listing.slovak_content else listing.get_json()',
     'get_or_create_translation(listing, "sk", "slovak_content")'),
    ('json.loads(listing.dutch_content) if listing.dutch_content else listing.get_json()',
     'get_or_create_translation(listing, "nl", "dutch_content")'),
    ('json.loads(listing.greek_content) if listing.greek_content else listing.get_json()',
     'get_or_create_translation(listing, "gr", "greek_content")'),
    ('json.loads(listing.croatian_content) if listing.croatian_content else listing.get_json()',
     'get_or_create_translation(listing, "hr", "croatian_content")'),
    ('json.loads(listing.french_content) if listing.french_content else listing.get_json()',
     'get_or_create_translation(listing, "fr", "french_content")'),
    ('json.loads(listing.english_content) if listing.english_content else listing.get_json()',
     'get_or_create_translation(listing, "en", "english_content")'),
    ('json.loads(listing.german_content) if listing.german_content else listing.get_json()',
     'get_or_create_translation(listing, "ge", "german_content")'),
]

count = 0
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        count += 1

print(f"✅ {count} Stellen ersetzt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig! Übersetzungen werden jetzt automatisch erstellt.")
