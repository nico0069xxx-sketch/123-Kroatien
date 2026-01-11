with open('templates/main/home.html', 'r') as f:
    content = f.read()

# Altes JavaScript komplett ersetzen
old_js = """const salePricesFrom = [
    {value: '', label: 'Preis von'},
    {value: '50000', label: '50.000 EUR'},
    {value: '100000', label: '100.000 EUR'},
    {value: '150000', label: '150.000 EUR'},
    {value: '200000', label: '200.000 EUR'},
    {value: '300000', label: '300.000 EUR'},
    {value: '500000', label: '500.000 EUR'},
    {value: '750000', label: '750.000 EUR'},
    {value: '1000000', label: '1.000.000 EUR'}
];
const salePricesTo = [
    {value: '', label: 'Preis bis'},
    {value: '100000', label: '100.000 EUR'},
    {value: '200000', label: '200.000 EUR'},
    {value: '300000', label: '300.000 EUR'},
    {value: '500000', label: '500.000 EUR'},
    {value: '750000', label: '750.000 EUR'},
    {value: '1000000', label: '1.000.000 EUR'},
    {value: '1500000', label: '1.500.000 EUR'},
    {value: '2000000', label: '2.000.000 EUR'},
    {value: '5000000', label: '5.000.000 EUR+'}
];"""

new_js = """const salePricesFrom = [
    {value: '', label: 'Preis von'},
    {value: '50000', label: '50.000 EUR'},
    {value: '100000', label: '100.000 EUR'},
    {value: '200000', label: '200.000 EUR'},
    {value: '300000', label: '300.000 EUR'},
    {value: '500000', label: '500.000 EUR'},
    {value: '750000', label: '750.000 EUR'},
    {value: '1000000', label: '1.000.000 EUR'},
    {value: '2000000', label: '2.000.000 EUR'},
    {value: '3000000', label: '3.000.000 EUR'},
    {value: '5000000', label: '5.000.000 EUR'},
    {value: '10000000', label: '10.000.000 EUR'}
];
const salePricesTo = [
    {value: '', label: 'Preis bis'},
    {value: '100000', label: '100.000 EUR'},
    {value: '200000', label: '200.000 EUR'},
    {value: '300000', label: '300.000 EUR'},
    {value: '500000', label: '500.000 EUR'},
    {value: '750000', label: '750.000 EUR'},
    {value: '1000000', label: '1.000.000 EUR'},
    {value: '2000000', label: '2.000.000 EUR'},
    {value: '3000000', label: '3.000.000 EUR'},
    {value: '5000000', label: '5.000.000 EUR'},
    {value: '7500000', label: '7.500.000 EUR'},
    {value: '10000000', label: '10.000.000 EUR'},
    {value: '15000000', label: '15.000.000 EUR'}
];"""

content = content.replace(old_js, new_js)

with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Kaufpreise aktualisiert!')
