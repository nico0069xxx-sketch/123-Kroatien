#!/usr/bin/env python3
"""Fixt das Springen beim Textwechsel"""

filepath = "templates/main/home.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Feste Höhe statt min-height, damit nichts springt
old_style = 'style="min-height: 50px; transition: opacity 1.2s ease; font-size: 1.25rem;"'
new_style = 'style="height: 80px; overflow: hidden; transition: opacity 1.2s ease; font-size: 1.25rem; display: flex; align-items: center;"'

if old_style in content:
    content = content.replace(old_style, new_style)
    print("✅ Feste Höhe gesetzt - kein Springen mehr!")
else:
    print("❌ Style nicht gefunden, versuche Alternative...")
    # Alternative
    old_alt = 'min-height: 50px;'
    new_alt = 'height: 80px; overflow: hidden; display: flex; align-items: center;'
    content = content.replace(old_alt, new_alt)
    print("✅ Alternative angewendet")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig!")
