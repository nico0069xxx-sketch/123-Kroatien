with open('templates/main/home.html', 'r') as f:
    content = f.read()

old_js = '''document.addEventListener('DOMContentLoaded', function() {
    updatePriceOptions();
});'''

new_js = '''document.addEventListener('DOMContentLoaded', function() {
    updatePriceOptions();
    
    // Watch for changes on the nice-select plugin
    var observer = new MutationObserver(function(mutations) {
        updatePriceOptions();
    });
    
    var statusSelect = document.getElementById('property_status');
    if (statusSelect) {
        observer.observe(statusSelect, { attributes: true, attributeFilter: ['value'] });
        
        // Also check periodically for nice-select changes
        var lastValue = statusSelect.value;
        setInterval(function() {
            if (statusSelect.value !== lastValue) {
                lastValue = statusSelect.value;
                updatePriceOptions();
            }
        }, 200);
    }
});'''

content = content.replace(old_js, new_js)

with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Event-Fix angewendet!')
