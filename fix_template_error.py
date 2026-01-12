#!/usr/bin/env python3
"""
Repariert den Template-Fehler
"""

with open("templates/main/home.html", "r", encoding="utf-8") as f:
    content = f.read()

# Kaputte default-Filter reparieren
fixes = [
    ('{{ smart_search_title|default:"{{ smart_search_title }}" }}', '{{ smart_search_title }}'),
    ('{{ smart_search_placeholder|default:"{{ smart_search_placeholder }}" }}', '{{ smart_search_placeholder }}'),
    ('{{ smart_search_loading|default:"{{ smart_search_loading }}" }}', '{{ smart_search_loading }}'),
    ('|default:"{{ smart_search_title }}"', ''),
    ('|default:"{{ smart_search_placeholder }}"', ''),
    ('|default:"{{ smart_search_loading }}"', ''),
    # Falls der ursprüngliche default noch da ist
    ('{{ smart_search_title|default:" }}', '{{ smart_search_title }}'),
]

for old, new in fixes:
    if old in content:
        content = content.replace(old, new)
        print(f"✅ Repariert: {old[:40]}...")

with open("templates/main/home.html", "w", encoding="utf-8") as f:
    f.write(content)

print("\n🎉 Template repariert!")
