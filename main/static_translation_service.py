from main.models import StaticContent
from main.translation_service import translate_text

LANGUAGES = {
    'english': 'Englisch',
    'french': 'Französisch', 
    'greek': 'Griechisch',
    'croatian': 'Kroatisch',
    'polish': 'Polnisch',
    'czech': 'Tschechisch',
    'russian': 'Russisch',
    'swedish': 'Schwedisch',
    'norwegian': 'Norwegisch',
    'slovak': 'Slowakisch',
    'dutch': 'Niederländisch',
}

def translate_static_content(content_obj):
    """Übersetzt einen StaticContent in alle Sprachen"""
    source_text = content_obj.german
    if not source_text:
        return {'error': 'Kein deutscher Text vorhanden'}
    
    results = {}
    for field_name, lang_name in LANGUAGES.items():
        print(f"  → {lang_name}...")
        translated = translate_text(source_text, lang_name)
        if translated:
            setattr(content_obj, field_name, translated)
            results[lang_name] = "✅"
        else:
            results[lang_name] = "❌"
    
    content_obj.save()
    return results

def translate_all_static_content():
    """Übersetzt alle statischen Inhalte"""
    contents = StaticContent.objects.all()
    for content in contents:
        print(f"Übersetze: {content.key}")
        translate_static_content(content)
    print("Fertig!")
