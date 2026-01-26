#!/usr/bin/env python3
"""Fügt die neuen Platform-Box Übersetzungen zur Datenbank hinzu"""
import os
import sys
import django

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
django.setup()

from pages.models import Translation
from main.translation_service import translate_text

# Deutsche Basis-Texte
TITLE_DE = "Verifizierte Makler finden"
TEXT_DE = "Diese Plattform ermöglicht das gezielte Auffinden geprüfter und verifizierter Immobilienmakler in Kroatien. Ergänzend stellt sie strukturierte Marktberichte, relevante Informationen und professionelle Adressen mit Bezug auf den kroatischen Immobilienmarkt bereit."

LANGUAGES = {
    'german_content': ('Deutsch', TITLE_DE, TEXT_DE),
    'english_content': 'Englisch',
    'french_content': 'Französisch',
    'greek_content': 'Griechisch',
    'polish_content': 'Polnisch',
    'czech_content': 'Tschechisch',
    'russian_content': 'Russisch',
    'swedish_content': 'Schwedisch',
    'norway_content': 'Norwegisch',
    'slovak_content': 'Slowakisch',
    'dutch_content': 'Niederländisch',
}

def create_translation(name, page='home'):
    """Erstellt oder aktualisiert eine Translation"""
    obj, created = Translation.objects.get_or_create(name=name, defaults={'page': page})
    if created:
        print(f"✅ Erstellt: {name}")
    return obj

# Titel Translation
print("\\n📝 Erstelle home_platform_title...")
title_trans = create_translation('home_platform_title')
title_trans.german_content = TITLE_DE

# Text Translation  
print("📝 Erstelle home_platform_text...")
text_trans = create_translation('home_platform_text')
text_trans.german_content = TEXT_DE

# Übersetze in alle Sprachen
for field, lang_name in LANGUAGES.items():
    if field == 'german_content':
        continue  # Deutsch ist schon gesetzt
    if isinstance(lang_name, tuple):
        continue
        
    print(f"🌍 Übersetze nach {lang_name}...")
    
    # Titel übersetzen
    translated_title = translate_text(TITLE_DE, lang_name)
    if translated_title:
        setattr(title_trans, field, translated_title)
        print(f"   ✅ Titel: {translated_title[:40]}...")
    
    # Text übersetzen
    translated_text = translate_text(TEXT_DE, lang_name)
    if translated_text:
        setattr(text_trans, field, translated_text)
        print(f"   ✅ Text übersetzt")

title_trans.save()
text_trans.save()

print("\\n🎉 Fertig! Neue Übersetzungen wurden zur Datenbank hinzugefügt.")
