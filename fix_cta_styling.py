#!/usr/bin/env python3
"""Passt das CTA-Styling an"""

filepath = "templates/main/home.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Überschrift: Wortabstand vergrößern
old_h2 = '<h2 class="text-uppercase text-light">{{StartJourney}}</h2>'
new_h2 = '<h2 class="text-uppercase text-light" style="letter-spacing: 3px; word-spacing: 8px;">{{StartJourney}}</h2>'

if old_h2 in content:
    content = content.replace(old_h2, new_h2)
    print("✅ Überschrift: Wortabstand vergrößert")

# 2. Wechselnder Text: Größer + KEINE Großbuchstaben (text-capitalize entfernt)
old_p = '<p class="text-capitalize text-light" id="rotating-cta-text" style="min-height: 50px; transition: opacity 0.5s ease;">'
new_p = '<p class="text-light" id="rotating-cta-text" style="min-height: 50px; transition: opacity 0.5s ease; font-size: 1.25rem;">'

if old_p in content:
    content = content.replace(old_p, new_p)
    print("✅ Wechselnder Text: Größer + normale Schrift (kein capitalize)")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Styling aktualisiert!")
