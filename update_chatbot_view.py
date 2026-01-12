#!/usr/bin/env python3
"""
Aktualisiert die Chatbot API View für Smart-Search
"""

# Zuerst prüfen wir wo die chatbot_api View ist
import os

# Suche in views.py nach chatbot_api
views_path = "main/views.py"

with open(views_path, "r", encoding="utf-8") as f:
    content = f.read()

# Prüfen ob chatbot_api existiert
if "def chatbot_api" in content:
    print("📍 chatbot_api gefunden in views.py")
    
    # Prüfen ob bereits erweitert
    if "get_chatbot_response_with_search" in content:
        print("⚠️  Chatbot View bereits erweitert")
    else:
        # Import hinzufügen
        old_import = "from main.chatbot import extract_search_criteria, is_property_search, smart_search_response"
        new_import = "from main.chatbot import extract_search_criteria, is_property_search, smart_search_response, get_chatbot_response_with_search"
        
        if old_import in content:
            content = content.replace(old_import, new_import)
            print("✅ Import erweitert")
        elif "from main.chatbot import" in content:
            # Anderen Import erweitern
            content = content.replace(
                "from main.chatbot import get_chatbot_response",
                "from main.chatbot import get_chatbot_response, get_chatbot_response_with_search, is_property_search, extract_search_criteria"
            )
            print("✅ Import erweitert (Alternative)")
        
        with open(views_path, "w", encoding="utf-8") as f:
            f.write(content)
        print("✅ Views.py aktualisiert!")
else:
    print("❌ chatbot_api nicht in views.py gefunden")
    
# Jetzt suchen wir in anderen Dateien
for filename in os.listdir("main"):
    if filename.endswith(".py"):
        filepath = f"main/{filename}"
        with open(filepath, "r", encoding="utf-8") as f:
            if "def chatbot_api" in f.read():
                print(f"📍 chatbot_api gefunden in: {filepath}")
