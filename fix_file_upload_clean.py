#!/usr/bin/env python3
"""Komplett neues, sauberes File-Upload Script"""

filepath = "templates/main/professional_registration.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Altes File-Upload Script komplett entfernen
import re

# Entferne das alte Script (von <script> bis </script> das fileInputs enthält)
pattern = r'<script>\s*document\.addEventListener\(\'DOMContentLoaded\', function\(\) \{\s*const fileInputs = document\.querySelectorAll.*?</script>'
content = re.sub(pattern, '', content, flags=re.DOTALL)
print("✅ Altes Script entfernt")

# Entferne auch das alte CSS wenn vorhanden
old_css_pattern = r'/\* Custom File Input.*?</style>'
content = re.sub(old_css_pattern, '</style>', content, flags=re.DOTALL)

# Neues, einfaches CSS und JS
new_code = '''
<style>
/* Kroatische File-Buttons */
.hr-file-wrapper {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
    margin-top: 8px;
}
.hr-file-btn {
    background: linear-gradient(135deg, #003167 0%, #0066cc 100%);
    color: white;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s;
}
.hr-file-btn:hover {
    background: linear-gradient(135deg, #002050 0%, #0055aa 100%);
}
.hr-file-name {
    color: #666;
    font-style: italic;
}
.hr-file-name.selected {
    color: #28a745;
    font-style: normal;
}
.hr-delete-btn {
    display: none;
    background: #dc3545;
    color: white;
    border: none;
    padding: 8px 14px;
    border-radius: 6px;
    cursor: pointer;
    font-size: 13px;
}
.hr-delete-btn.visible {
    display: inline-flex;
    align-items: center;
    gap: 5px;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('input[type="file"]').forEach(function(input) {
        // Wrapper erstellen
        var wrapper = document.createElement('div');
        wrapper.className = 'hr-file-wrapper';
        
        // Label für Button
        var label = document.createElement('label');
        label.className = 'hr-file-btn';
        label.innerHTML = '<i class="fas fa-upload"></i> Odaberi datoteku';
        label.htmlFor = input.id;
        
        // Dateiname
        var nameEl = document.createElement('span');
        nameEl.className = 'hr-file-name';
        nameEl.textContent = 'Nije odabrana datoteka';
        
        // Lösch-Button
        var delBtn = document.createElement('button');
        delBtn.type = 'button';
        delBtn.className = 'hr-delete-btn';
        delBtn.innerHTML = '<i class="fas fa-times"></i> Ukloni';
        
        // Input verstecken
        input.style.display = 'none';
        
        // Nach dem Input einfügen
        input.parentNode.insertBefore(wrapper, input.nextSibling);
        wrapper.appendChild(label);
        wrapper.appendChild(nameEl);
        wrapper.appendChild(delBtn);
        
        // Change Event
        input.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                nameEl.textContent = this.files[0].name;
                nameEl.className = 'hr-file-name selected';
                delBtn.className = 'hr-delete-btn visible';
            }
        });
        
        // Delete Event
        delBtn.addEventListener('click', function() {
            input.value = '';
            nameEl.textContent = 'Nije odabrana datoteka';
            nameEl.className = 'hr-file-name';
            delBtn.className = 'hr-delete-btn';
        });
    });
});
</script>
'''

# Füge vor {% endblock %} ein
endblock_pos = content.rfind('{% endblock')
if endblock_pos > 0:
    content = content[:endblock_pos] + new_code + '\n' + content[endblock_pos:]
    print("✅ Neues sauberes Script hinzugefügt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig!")
