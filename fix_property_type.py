#!/usr/bin/env python3
"""Fügt property_type Übersetzung zur get_or_create_translation Funktion hinzu"""

filepath = "main/views.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Property Type Mapping hinzufügen
old_code = '''    lang_names = {
        'german_content': 'Deutsch', 'english_content': 'Englisch','''

new_code = '''    # Property Type Übersetzungen
    property_type_translations = {
        'Deutsch': {'House': 'Haus', 'Apartment': 'Wohnung', 'Villa': 'Villa', 'Property': 'Grundstück', 'New Building': 'Neubau', 'Office': 'Büro'},
        'Englisch': {'House': 'House', 'Apartment': 'Apartment', 'Villa': 'Villa', 'Property': 'Property', 'New Building': 'New Building', 'Office': 'Office', 'Haus': 'House', 'Wohnung': 'Apartment', 'Grundstück': 'Property', 'Neubau': 'New Building', 'Büro': 'Office'},
        'Französisch': {'House': 'Maison', 'Apartment': 'Appartement', 'Villa': 'Villa', 'Property': 'Terrain', 'New Building': 'Neuf', 'Office': 'Bureau', 'Haus': 'Maison', 'Wohnung': 'Appartement'},
        'Griechisch': {'House': 'Σπίτι', 'Apartment': 'Διαμέρισμα', 'Villa': 'Βίλα', 'Property': 'Ακίνητο', 'New Building': 'Νεόδμητο', 'Office': 'Γραφείο', 'Haus': 'Σπίτι', 'Wohnung': 'Διαμέρισμα'},
        'Kroatisch': {'House': 'Kuća', 'Apartment': 'Stan', 'Villa': 'Vila', 'Property': 'Zemljište', 'New Building': 'Novogradnja', 'Office': 'Ured', 'Haus': 'Kuća', 'Wohnung': 'Stan'},
        'Polnisch': {'House': 'Dom', 'Apartment': 'Mieszkanie', 'Villa': 'Willa', 'Property': 'Działka', 'New Building': 'Nowe budownictwo', 'Office': 'Biuro', 'Haus': 'Dom', 'Wohnung': 'Mieszkanie'},
        'Tschechisch': {'House': 'Dům', 'Apartment': 'Byt', 'Villa': 'Vila', 'Property': 'Pozemek', 'New Building': 'Novostavba', 'Office': 'Kancelář', 'Haus': 'Dům', 'Wohnung': 'Byt'},
        'Russisch': {'House': 'Дом', 'Apartment': 'Квартира', 'Villa': 'Вилла', 'Property': 'Участок', 'New Building': 'Новостройка', 'Office': 'Офис', 'Haus': 'Дом', 'Wohnung': 'Квартира'},
        'Schwedisch': {'House': 'Hus', 'Apartment': 'Lägenhet', 'Villa': 'Villa', 'Property': 'Tomt', 'New Building': 'Nybygge', 'Office': 'Kontor', 'Haus': 'Hus', 'Wohnung': 'Lägenhet'},
        'Norwegisch': {'House': 'Hus', 'Apartment': 'Leilighet', 'Villa': 'Villa', 'Property': 'Tomt', 'New Building': 'Nybygg', 'Office': 'Kontor', 'Haus': 'Hus', 'Wohnung': 'Leilighet'},
        'Slowakisch': {'House': 'Dom', 'Apartment': 'Byt', 'Villa': 'Vila', 'Property': 'Pozemok', 'New Building': 'Novostavba', 'Office': 'Kancelária', 'Haus': 'Dom', 'Wohnung': 'Byt'},
        'Niederländisch': {'House': 'Huis', 'Apartment': 'Appartement', 'Villa': 'Villa', 'Property': 'Grond', 'New Building': 'Nieuwbouw', 'Office': 'Kantoor', 'Haus': 'Huis', 'Wohnung': 'Appartement'},
    }
    
    lang_names = {
        'german_content': 'Deutsch', 'english_content': 'Englisch','''

if old_code in content:
    content = content.replace(old_code, new_code)
    print("✅ Property Type Mapping hinzugefügt")

# Jetzt die Stelle finden wo json_content erstellt wird und property_type übersetzen
old_json = '''"property_type": listing.property_type,'''
new_json = '''"property_type": property_type_translations.get(target_lang, {}).get(listing.property_type, listing.property_type),'''

count = content.count(old_json)
if count > 0:
    content = content.replace(old_json, new_json)
    print(f"✅ {count} property_type Übersetzungen eingefügt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig! Property Types werden jetzt auch übersetzt.")
