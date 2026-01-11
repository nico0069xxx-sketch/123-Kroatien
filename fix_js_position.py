with open('templates/main/home.html', 'r') as f:
    content = f.read()

# JavaScript aus block js extrahieren
js_code = '''<script>
const salePricesFrom = [
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
];
const rentPricesFrom = [
    {value: '', label: 'Preis von'},
    {value: '300', label: '300 EUR/Monat'},
    {value: '500', label: '500 EUR/Monat'},
    {value: '750', label: '750 EUR/Monat'},
    {value: '1000', label: '1.000 EUR/Monat'},
    {value: '1500', label: '1.500 EUR/Monat'},
    {value: '2000', label: '2.000 EUR/Monat'},
    {value: '3000', label: '3.000 EUR/Monat'}
];
const rentPricesTo = [
    {value: '', label: 'Preis bis'},
    {value: '500', label: '500 EUR/Monat'},
    {value: '750', label: '750 EUR/Monat'},
    {value: '1000', label: '1.000 EUR/Monat'},
    {value: '1500', label: '1.500 EUR/Monat'},
    {value: '2000', label: '2.000 EUR/Monat'},
    {value: '3000', label: '3.000 EUR/Monat'},
    {value: '5000', label: '5.000 EUR/Monat'},
    {value: '8000', label: '8.000 EUR/Monat'}
];
function updatePriceOptions() {
    var status = document.getElementById('property_status').value;
    var priceFrom = document.getElementById('price_from');
    var priceTo = document.getElementById('price_to');
    priceFrom.innerHTML = '';
    priceTo.innerHTML = '';
    var fromOptions = (status === 'Rent') ? rentPricesFrom : salePricesFrom;
    var toOptions = (status === 'Rent') ? rentPricesTo : salePricesTo;
    fromOptions.forEach(function(opt) {
        var option = document.createElement('option');
        option.value = opt.value;
        option.textContent = opt.label;
        priceFrom.appendChild(option);
    });
    toOptions.forEach(function(opt) {
        var option = document.createElement('option');
        option.value = opt.value;
        option.textContent = opt.label;
        priceTo.appendChild(option);
    });
}
document.addEventListener('DOMContentLoaded', function() {
    updatePriceOptions();
});
</script>
{% endblock body %}'''

# Ersetze nur {% endblock body %}
content = content.replace('{% endblock body %}', js_code)

# Entferne den alten block js
import re
content = re.sub(r'\{% block js %\}.*?\{% endblock js %\}', '', content, flags=re.DOTALL)

with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('JavaScript verschoben!')
