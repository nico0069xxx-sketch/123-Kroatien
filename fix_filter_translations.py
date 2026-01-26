#!/usr/bin/env python3
"""Fügt fehlende filter_property_status, filter_for_sale, filter_For_Rent Übersetzungen hinzu"""

import re

# Neue Übersetzungen für alle 12 Sprachen
NEW_TRANSLATIONS = {
    "ge": '''        "filter_property_status": "Kaufen/Mieten",
        "filter_for_sale": "Kaufen",
        "filter_For_Rent": "Mieten",''',
    "en": '''        "filter_property_status": "Buy/Rent",
        "filter_for_sale": "Buy",
        "filter_For_Rent": "Rent",''',
    "hr": '''        "filter_property_status": "Kupi/Najam",
        "filter_for_sale": "Kupi",
        "filter_For_Rent": "Najam",''',
    "fr": '''        "filter_property_status": "Acheter/Louer",
        "filter_for_sale": "Acheter",
        "filter_For_Rent": "Louer",''',
    "nl": '''        "filter_property_status": "Kopen/Huren",
        "filter_for_sale": "Kopen",
        "filter_For_Rent": "Huren",''',
    "pl": '''        "filter_property_status": "Kupno/Wynajem",
        "filter_for_sale": "Kupno",
        "filter_For_Rent": "Wynajem",''',
    "cz": '''        "filter_property_status": "Koupit/Pronájem",
        "filter_for_sale": "Koupit",
        "filter_For_Rent": "Pronájem",''',
    "sk": '''        "filter_property_status": "Kúpiť/Prenájom",
        "filter_for_sale": "Kúpiť",
        "filter_For_Rent": "Prenájom",''',
    "ru": '''        "filter_property_status": "Купить/Аренда",
        "filter_for_sale": "Купить",
        "filter_For_Rent": "Аренда",''',
    "gr": '''        "filter_property_status": "Αγορά/Ενοικίαση",
        "filter_for_sale": "Αγορά",
        "filter_For_Rent": "Ενοικίαση",''',
    "sw": '''        "filter_property_status": "Köpa/Hyra",
        "filter_for_sale": "Köpa",
        "filter_For_Rent": "Hyra",''',
    "no": '''        "filter_property_status": "Kjøpe/Leie",
        "filter_for_sale": "Kjøpe",
        "filter_For_Rent": "Leie",''',
}

filepath = "main/context_processors.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Für jede Sprache: Nach "filter_price_to" die neuen Zeilen einfügen
for lang, new_lines in NEW_TRANSLATIONS.items():
    # Pattern: "filter_price_to": "...", innerhalb des Sprach-Blocks
    # Wir suchen nach dem Muster und fügen danach die neuen Zeilen ein
    pattern = rf'("{lang}":\s*\{{[^}}]*"filter_price_to":\s*"[^"]*",)'
    
    def replacer(match):
        return match.group(1) + "\n" + new_lines
    
    content = re.sub(pattern, replacer, content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Übersetzungen hinzugefügt für: filter_property_status, filter_for_sale, filter_For_Rent")
print("   Alle 12 Sprachen wurden aktualisiert!")
