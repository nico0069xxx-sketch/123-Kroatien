#!/usr/bin/env python3
"""Fixt die ZATVORENO Checkboxen"""

filepath = "templates/main/professional_registration.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS für Checkboxen hinzufügen
checkbox_css = '''
/* Fix für ZATVORENO Checkboxen */
td input[type="checkbox"] {
    width: 20px;
    height: 20px;
    cursor: pointer;
    accent-color: #003167;
}
'''

# Füge CSS zum bestehenden Style-Block hinzu
if 'ZATVORENO Checkboxen' not in content:
    # Finde den </style> Tag und füge davor ein
    content = content.replace('</style>', checkbox_css + '</style>', 1)
    print("✅ Checkbox-CSS hinzugefügt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig!")
