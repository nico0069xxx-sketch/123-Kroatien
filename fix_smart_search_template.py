#!/usr/bin/env python3
"""
Aktualisiert Smart-Search Template für Übersetzungen
"""

with open("templates/main/home.html", "r", encoding="utf-8") as f:
    content = f.read()

# Hardcoded Texte durch Template-Variablen ersetzen
replacements = [
    ('KI-Immobiliensuche', '{{ smart_search_title }}'),
    ("Beschreibe deine Traumimmobilie... z.B. Haus am Meer mit Pool unter 500.000€", '{{ smart_search_placeholder }}'),
    ('Suche läuft...', '{{ smart_search_loading }}'),
]

for old, new in replacements:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Ersetzt: {old[:30]}...")

with open("templates/main/home.html", "w", encoding="utf-8") as f:
    f.write(content)

print("\n🎉 Template aktualisiert!")
