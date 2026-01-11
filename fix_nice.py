with open('templates/main/home.html', 'r') as f:
    content = f.read()

old_func = '''function updatePriceOptions() {
    var status = document.getElementById('property_status');
    if (!status) return;
    var priceFrom = document.getElementById('price_from');
    var priceTo = document.getElementById('price_to');
    if (!priceFrom || !priceTo) return;
    priceFrom.innerHTML = '';
    priceTo.innerHTML = '';
    var fromOptions = (status.value === 'Rent') ? rentPricesFrom : salePricesFrom;
    var toOptions = (status.value === 'Rent') ? rentPricesTo : salePricesTo;
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
}'''

new_func = '''function updatePriceOptions() {
    var status = document.getElementById('property_status');
    if (!status) return;
    var priceFrom = document.getElementById('price_from');
    var priceTo = document.getElementById('price_to');
    if (!priceFrom || !priceTo) return;
    priceFrom.innerHTML = '';
    priceTo.innerHTML = '';
    var fromOptions = (status.value === 'Rent') ? rentPricesFrom : salePricesFrom;
    var toOptions = (status.value === 'Rent') ? rentPricesTo : salePricesTo;
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
    if (typeof jQuery !== 'undefined') {
        jQuery(priceFrom).niceSelect('update');
        jQuery(priceTo).niceSelect('update');
    }
}'''

content = content.replace(old_func, new_func)

with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Nice-Select Update hinzugefuegt!')
