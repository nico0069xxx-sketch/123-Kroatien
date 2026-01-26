#!/usr/bin/env python3
"""Fügt die wechselnden CTA-Texte zur Datenbank hinzu"""
import os
import sys
import django

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
django.setup()

from pages.models import Translation
from main.translation_service import translate_text

# Die 12 neuen deutschen Texte
ROTATING_TEXTS = [
    "Hier finden Sie strukturierte Informationen zu Immobilien in Kroatien – nach Regionen, Objektarten und Marktüberblicken.",
    "Vergleichen Sie Immobilien in Kroatien auf einer neutralen Plattform mit regionalen Marktinformationen.",
    "Diese Plattform bietet einen Überblick über Immobilienangebote und professionelle Anbieter in Kroatien.",
    "Immobilien in Kroatien verstehen: Regionen, Preise, Anbieter und Marktstruktur auf einen Blick.",
    "Finden Sie Immobilien in Kroatien mit transparenter Darstellung nach Lage, Kategorie und Anbieter.",
    "Internationale Käufer nutzen diese Plattform zur Orientierung im kroatischen Immobilienmarkt.",
    "Informationen zu Immobilien in Kroatien – mehrsprachig, strukturiert und sachlich aufbereitet.",
    "Dieses Portal dient als Referenz für Immobilien, Anbieter und Marktberichte in Kroatien.",
    "Suchen Sie Immobilien in Kroatien auf Basis von Regionen, Daten und professionellen Anbietern.",
    "Plattform für die Immobilienrecherche in Kroatien – ohne Vermittlung, ohne Verkaufsdruck.",
    "Kroatien Immobilien: Marktüberblicke, Anbieterprofile und regionale Informationen an einem Ort.",
    "Für Käufer, die Immobilien in Kroatien vergleichen und den Markt fundiert verstehen möchten.",
]

LANGUAGES = {
    'english_content': 'Englisch',
    'french_content': 'Französisch',
    'greek_content': 'Griechisch',
    'croatian_content': 'Kroatisch',
    'polish_content': 'Polnisch',
    'czech_content': 'Tschechisch',
    'russian_content': 'Russisch',
    'swedish_content': 'Schwedisch',
    'norway_content': 'Norwegisch',
    'slovak_content': 'Slowakisch',
    'dutch_content': 'Niederländisch',
}

print("📝 Erstelle wechselnde CTA-Texte...\\n")

for i, text_de in enumerate(ROTATING_TEXTS, 1):
    name = f"cta_rotating_{i}"
    print(f"\\n[{i}/12] {name}")
    print(f"   DE: {text_de[:50]}...")
    
    obj, created = Translation.objects.get_or_create(name=name, defaults={'page': 'home'})
    obj.german_content = text_de
    
    for field, lang_name in LANGUAGES.items():
        print(f"   🌍 {lang_name}...", end=" ")
        translated = translate_text(text_de, lang_name)
        if translated:
            setattr(obj, field, translated)
            print("✅")
        else:
            print("❌")
    
    obj.save()
    print(f"   💾 Gespeichert!")

print("\\n🎉 Alle 12 wechselnden Texte wurden erstellt und übersetzt!")
