#!/usr/bin/env python3
"""Fixt Lösch-Button und fügt Dateiformat-Hinweise hinzu"""

filepath = "templates/main/professional_registration.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. DATEIFORMAT-HINWEISE hinzufügen
# Profilna slika
if '{{ form.profile_image }}' in content and 'JPG, PNG, WEBP</small>' not in content:
    content = content.replace(
        '{{ form.profile_image }}',
        '{{ form.profile_image }}\n                  <small class="text-muted d-block mt-1">JPG, PNG, WEBP</small>'
    )
    print("✅ Hinweis bei Profilna slika hinzugefügt")

# Logo tvrtke  
if '{{ form.company_logo }}' in content and 'SVG</small>' not in content:
    content = content.replace(
        '{{ form.company_logo }}',
        '{{ form.company_logo }}\n                  <small class="text-muted d-block mt-1">JPG, PNG, SVG</small>'
    )
    print("✅ Hinweis bei Logo tvrtke hinzugefügt")

# 2. LÖSCH-BUTTON FIX - Button außerhalb des Wrappers platzieren
old_js_start = '''<script>
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');'''

new_js = '''<script>
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        // Container für alles
        const container = document.createElement('div');
        container.style.cssText = 'display:flex; align-items:center; gap:10px; flex-wrap:wrap;';
        
        // Wrapper nur für Input + Button
        const wrapper = document.createElement('div');
        wrapper.style.cssText = 'position:relative; display:inline-block;';
        
        const btn = document.createElement('span');
        btn.className = 'custom-file-btn';
        btn.innerHTML = '<i class="fas fa-upload"></i> Odaberi datoteku';
        
        input.style.cssText = 'position:absolute; opacity:0; width:100%; height:100%; cursor:pointer; z-index:2; left:0; top:0;';
        
        wrapper.appendChild(btn);
        wrapper.appendChild(input);
        
        // Dateiname (außerhalb wrapper)
        const nameSpan = document.createElement('span');
        nameSpan.className = 'custom-file-name';
        nameSpan.textContent = 'Nije odabrana datoteka';
        nameSpan.style.cssText = 'color:#666; font-style:italic;';
        
        // Lösch-Button (außerhalb wrapper - wichtig!)
        const deleteBtn = document.createElement('button');
        deleteBtn.type = 'button';
        deleteBtn.innerHTML = '<i class="fas fa-times"></i> Ukloni';
        deleteBtn.style.cssText = 'display:none; padding:8px 12px; background:#dc3545; color:white; border:none; border-radius:6px; cursor:pointer; font-size:13px;';
        
        const parent = input.parentNode;
        
        container.appendChild(wrapper);
        container.appendChild(nameSpan);
        container.appendChild(deleteBtn);
        parent.appendChild(container);
        
        input.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                nameSpan.textContent = this.files[0].name;
                nameSpan.style.color = '#28a745';
                nameSpan.style.fontStyle = 'normal';
                deleteBtn.style.display = 'inline-block';
            } else {
                nameSpan.textContent = 'Nije odabrana datoteka';
                nameSpan.style.color = '#666';
                nameSpan.style.fontStyle = 'italic';
                deleteBtn.style.display = 'none';
            }
        });
        
        deleteBtn.addEventListener('click', function() {
            input.value = '';
            nameSpan.textContent = 'Nije odabrana datoteka';
            nameSpan.style.color = '#666';
            nameSpan.style.fontStyle = 'italic';
            this.style.display = 'none';
        });
    });
});
</script>'''

# Finde und ersetze das komplette alte Script
import re
old_script_pattern = r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{\s*const fileInputs = document\.querySelectorAll\(\'input\[type="file"\]\'\);.*?</script>'

content = re.sub(old_script_pattern, new_js, content, flags=re.DOTALL)
print("✅ JavaScript für Lösch-Button gefixt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig!")
