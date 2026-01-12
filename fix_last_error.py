#!/usr/bin/env python3

with open("templates/main/home.html", "r", encoding="utf-8") as f:
    content = f.read()

# Den kaputten placeholder fixen
old = "{{ smart_search_placeholder|default:'{{ smart_search_placeholder }}' }}"
new = "{{ smart_search_placeholder }}"

content = content.replace(old, new)

with open("templates/main/home.html", "w", encoding="utf-8") as f:
    f.write(content)

print("✅ Letzter Fehler behoben!")
