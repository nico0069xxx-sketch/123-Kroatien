#!/usr/bin/env python3
"""Passt das Timing der wechselnden Texte an"""

filepath = "templates/main/home.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Übergang sanfter: 0.5s -> 1.2s
old_transition = 'transition: opacity 0.5s ease;'
new_transition = 'transition: opacity 1.2s ease;'

if old_transition in content:
    content = content.replace(old_transition, new_transition)
    print("✅ Übergang sanfter (1.2 Sekunden)")

# 2. setTimeout im JS auch anpassen: 500 -> 1200
old_timeout = 'setTimeout(() => {'
new_timeout = 'setTimeout(() => {'
# Das bleibt gleich, aber die Zeit muss angepasst werden
content = content.replace('}, 500);', '}, 1200);')
print("✅ JS Timeout angepasst")

# 3. Intervall länger: 5000 -> 9000 (9 Sekunden)
content = content.replace('setInterval(rotateText, 5000);', 'setInterval(rotateText, 9000);')
print("✅ Anzeigedauer: 9 Sekunden")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig!")
