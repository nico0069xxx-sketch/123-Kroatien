#!/usr/bin/env python3
"""
Fügt Smart-Search URL zu urls.py hinzu
"""

with open("main/urls.py", "r", encoding="utf-8") as f:
    content = f.read()

# Prüfen ob URL schon existiert
if "smart-search" not in content:
    # Vor der letzten ] einfügen
    new_url = "    path('api/smart-search/', views.smart_search, name='smart_search'),\n"
    
    # Finde die letzte ] in urlpatterns
    last_bracket = content.rfind("]")
    if last_bracket != -1:
        content = content[:last_bracket] + new_url + content[last_bracket:]
        
        with open("main/urls.py", "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Smart-Search URL hinzugefügt!")
    else:
        print("❌ Konnte urlpatterns nicht finden")
else:
    print("⚠️  Smart-Search URL existiert bereits")
