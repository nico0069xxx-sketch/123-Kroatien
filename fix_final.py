with open('templates/main/home.html', 'r') as f:
    content = f.read()

# Finde und ersetze den Event-Listener
old_js = '''document.addEventListener('DOMContentLoaded', function() {
    updatePriceOptions();
    
    // Nice-select click handler
    document.body.addEventListener('click', function(e) {
        if (e.target.classList.contains('option') || e.target.closest('.nice-select')) {
            setTimeout(function() {
                updatePriceOptions();
            }, 100);
        }
    });
});'''

new_js = '''document.addEventListener('DOMContentLoaded', function() {
    updatePriceOptions();
    
    // Finde das Nice-Select fuer property_status
    var statusSelect = document.getElementById('property_status');
    if (statusSelect) {
        var niceSelect = statusSelect.nextElementSibling;
        if (niceSelect && niceSelect.classList.contains('nice-select')) {
            var options = niceSelect.querySelectorAll('.option');
            options.forEach(function(opt) {
                opt.addEventListener('click', function() {
                    setTimeout(updatePriceOptions, 50);
                });
            });
        }
    }
});'''

content = content.replace(old_js, new_js)

with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Final Fix angewendet!')
