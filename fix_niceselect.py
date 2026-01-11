with open('templates/main/home.html', 'r') as f:
    content = f.read()

old_js = '''document.addEventListener('DOMContentLoaded', function() {
    updatePriceOptions();
});'''

new_js = '''document.addEventListener('DOMContentLoaded', function() {
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

content = content.replace(old_js, new_js)

with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Nice-Select Fix angewendet!')
