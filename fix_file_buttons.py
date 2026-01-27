#!/usr/bin/env python3
"""Fügt kroatische File-Upload Buttons hinzu"""

filepath = "templates/main/professional_registration.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# CSS und JS für Custom File Inputs
custom_style = '''
<style>
/* Custom File Input - Kroatisch */
input[type="file"] {
    position: relative;
    width: 100%;
}
input[type="file"]::file-selector-button {
    background: linear-gradient(135deg, #003167 0%, #0066cc 100%);
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    margin-right: 15px;
    transition: all 0.3s ease;
}
input[type="file"]::file-selector-button:hover {
    background: linear-gradient(135deg, #002050 0%, #0055aa 100%);
}
/* Verstecke den Standard-Text und zeige eigenen */
.custom-file-wrapper {
    position: relative;
}
.custom-file-wrapper input[type="file"] {
    opacity: 0;
    position: absolute;
    width: 100%;
    height: 100%;
    cursor: pointer;
    z-index: 2;
}
.custom-file-btn {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    background: linear-gradient(135deg, #003167 0%, #0066cc 100%);
    color: white;
    border: none;
    padding: 12px 24px;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s ease;
}
.custom-file-btn:hover {
    background: linear-gradient(135deg, #002050 0%, #0055aa 100%);
}
.custom-file-name {
    margin-left: 15px;
    color: #666;
    font-style: italic;
}
</style>

'''

# JavaScript für File-Name Anzeige
custom_js = '''
<script>
document.addEventListener('DOMContentLoaded', function() {
    // Alle File-Inputs finden und wrappen
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        // Wrapper erstellen
        const wrapper = document.createElement('div');
        wrapper.className = 'custom-file-wrapper';
        wrapper.style.position = 'relative';
        wrapper.style.display = 'inline-block';
        wrapper.style.width = '100%';
        
        // Custom Button
        const btn = document.createElement('span');
        btn.className = 'custom-file-btn';
        btn.innerHTML = '<i class="fas fa-upload"></i> Odaberi datoteku';
        
        // Dateiname Anzeige
        const nameSpan = document.createElement('span');
        nameSpan.className = 'custom-file-name';
        nameSpan.textContent = 'Nije odabrana datoteka';
        
        // Original Input verstecken aber funktional lassen
        input.style.position = 'absolute';
        input.style.opacity = '0';
        input.style.width = '100%';
        input.style.height = '100%';
        input.style.cursor = 'pointer';
        input.style.zIndex = '2';
        input.style.left = '0';
        input.style.top = '0';
        
        // Parent Element
        const parent = input.parentNode;
        
        // Wrapper aufbauen
        wrapper.appendChild(input);
        wrapper.appendChild(btn);
        wrapper.appendChild(nameSpan);
        parent.appendChild(wrapper);
        
        // Event Listener für Dateiauswahl
        input.addEventListener('change', function() {
            if (this.files && this.files.length > 0) {
                nameSpan.textContent = this.files[0].name;
                nameSpan.style.color = '#28a745';
                nameSpan.style.fontStyle = 'normal';
            } else {
                nameSpan.textContent = 'Nije odabrana datoteka';
                nameSpan.style.color = '#666';
                nameSpan.style.fontStyle = 'italic';
            }
        });
    });
});
</script>
'''

# CSS nach {% block body %} einfügen
if '{% block body %}' in content and custom_style not in content:
    content = content.replace('{% block body %}', '{% block body %}' + custom_style)
    print("✅ CSS für Custom File Buttons hinzugefügt")

# JS vor {% endblock body %} oder {% endblock %} einfügen
if custom_js not in content:
    if '{% endblock body %}' in content:
        content = content.replace('{% endblock body %}', custom_js + '{% endblock body %}')
    elif '{% endblock %}' in content:
        # Finde das letzte {% endblock %}
        last_endblock = content.rfind('{% endblock %}')
        if last_endblock > 0:
            content = content[:last_endblock] + custom_js + content[last_endblock:]
    print("✅ JavaScript für Dateiname-Anzeige hinzugefügt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig! File-Buttons jetzt auf Kroatisch:")
print("   - 'Odaberi datoteku' (Datei auswählen)")
print("   - 'Nije odabrana datoteka' (Keine Datei ausgewählt)")
