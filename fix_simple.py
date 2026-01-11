with open('templates/main/home.html', 'r') as f:
    content = f.read()

import re
pattern = r"document\.addEventListener\('DOMContentLoaded'.*?\}\);"
replacement = '''document.addEventListener('DOMContentLoaded', function() {
    updatePriceOptions();
    var lastStatus = '';
    setInterval(function() {
        var el = document.getElementById('property_status');
        if (el && el.value !== lastStatus) {
            lastStatus = el.value;
            updatePriceOptions();
        }
    }, 300);
});'''

content = re.sub(pattern, replacement, content, flags=re.DOTALL)

with open('templates/main/home.html', 'w') as f:
    f.write(content)

print('Fix angewendet!')
