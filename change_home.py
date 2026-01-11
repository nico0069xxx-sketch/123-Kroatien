import re

# Datei lesen
with open('templates/main/home.html', 'r') as f:
    content = f.read()

# Aenderung 1: property_status ID und onchange hinzufuegen
old1 = 'name="property_status" class="wide select_option"'
new1 = 'name="property_status" id="property_status" class="wide select_option" onchange="updatePriceOptions()"'
content = content.replace(old1, new1)

# Aenderung 2: Preis-Schieberegler ersetzen
old2 = '''                    <div class="col-12 col-lg-3 col-md-3">
                        <div class="form-group">
                            <div class="filter__price">
                                <input class="price-range" type="text" name="my_range" value=""/>
                            </div>
                        </div>
                    </div>'''

new2 = '''                    <div class="col-6 col-lg-3 col-md-3">
                        <div class="form-group">
                            <select class="wide select_option" name="price_from" id="price_from">
                                <option value="">Preis von</option>
                                <option value="50000">50.000 EUR</option>
                                <option value="100000">100.000 EUR</option>
                                <option value="150000">150.000 EUR</option>
                                <option value="200000">200.000 EUR</option>
                                <option value="300000">300.000 EUR</option>
                                <option value="500000">500.000 EUR</option>
                                <option value="750000">750.000 EUR</option>
                                <option value="1000000">1.000.000 EUR</option>
                            </select>
                        </div>
                    </div>
                    <div class="col-6 col-lg-3 col-md-3">
                        <div class="form-group">
                            <select class="wide select_option" name="price_to" id="price_to">
                                <option value="">Preis bis</option>
                                <option value="100000">100.000 EUR</option>
                                <option value="200000">200.000 EUR</option>
                                <option value="300000">300.000 EUR</option>
                                <option value="500000">500.000 EUR</option>
                                <option value="750000">750.000 EUR</option>
                                <option value="1000000">1.000.000 EUR</option>
                                <option value="1500000">1.500.000 EUR</option>
                                <option value="2000000">2.000.000 EUR</option>
                                <option value="5000000">5.000.000 EUR+</option>
                            </select>
                        </div>
                    </div>'''

content = content.replace(old2, new2)

# Aenderung 3: JavaScript am Ende hinzufuegen
js_code = '''
{% block js %}
<script>
const salePricesFrom = [
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
    {value: '8000', label: '8.000 EUR/Monat+'}
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
{% endblock js %}'''

if '{% block js %}' not in content:
    content = content.replace('{% endblock body %}', '{% endblock body %}' + js_code)

# Datei schreiben
with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Fertig! home.html wurde aktualisiert.')
