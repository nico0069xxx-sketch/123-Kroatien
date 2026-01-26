#!/usr/bin/env python3
"""Fixt das property_status Badge im home.html Template"""

filepath = "templates/main/home.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Ersetze das Badge - von json_content.property_status zu einer Bedingung
old_badge = '<div class="info" style="background-color: #db0000;"> {{listing.json_content.property_status}}'
new_badge = '''<div class="info" style="background-color: #db0000;">{% if listing.property_status == "Zu verkaufen" or listing.property_status == "Sale" %}{{filter_for_sale}}{% elif listing.property_status == "Zu mieten" or listing.property_status == "Rent" %}{{filter_For_Rent}}{% else %}{{listing.property_status}}{% endif %}'''

content = content.replace(old_badge, new_badge)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Badge gefixt! Zeigt jetzt übersetzte Status an.")
