#!/usr/bin/env python3
"""
Korrigiert die Smart-Search URL im JavaScript
"""

with open("templates/main/home.html", "r", encoding="utf-8") as f:
    content = f.read()

# URL korrigieren - Sprach-Prefix hinzufügen
old_url = "fetch('/api/smart-search/'"
new_url = "fetch('/ge/api/smart-search/'"

if old_url in content:
    content = content.replace(old_url, new_url)
    with open("templates/main/home.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ URL korrigiert!")
else:
    print("⚠️  URL bereits korrigiert oder nicht gefunden")
