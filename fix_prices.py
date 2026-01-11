# Datei lesen
with open('templates/main/home.html', 'r') as f:
    content = f.read()

# Alte Kaufpreise durch neue bis 15 Mio ersetzen
content = content.replace("'1000000', label: '1.000.000 EUR'}\n];", "'1000000', label: '1.000.000 EUR'},\n    {value: '1500000', label: '1.500.000 EUR'},\n    {value: '2000000', label: '2.000.000 EUR'},\n    {value: '3000000', label: '3.000.000 EUR'},\n    {value: '5000000', label: '5.000.000 EUR'},\n    {value: '7500000', label: '7.500.000 EUR'},\n    {value: '10000000', label: '10.000.000 EUR'},\n    {value: '15000000', label: '15.000.000 EUR'}\n];")

# Datei schreiben
with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Fertig! Preise wurden aktualisiert.')
