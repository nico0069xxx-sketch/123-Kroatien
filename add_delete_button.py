#!/usr/bin/env python3
"""Fügt Lösch-Button für hochgeladene Dateien hinzu"""

filepath = "templates/main/professional_registration.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Altes JavaScript durch neues mit Lösch-Button ersetzen
old_js = '''<script>
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
</script>'''

new_js = '''<script>
document.addEventListener('DOMContentLoaded', function() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(function(input) {
        const wrapper = document.createElement('div');
        wrapper.className = 'custom-file-wrapper';
        wrapper.style.position = 'relative';
        wrapper.style.display = 'inline-block';
        wrapper.style.width = '100%';
        
        const btn = document.createElement('span');
        btn.className = 'custom-file-btn';
        btn.innerHTML = '<i class="fas fa-upload"></i> Odaberi datoteku';
        
        const nameSpan = document.createElement('span');
        nameSpan.className = 'custom-file-name';
        nameSpan.textContent = 'Nije odabrana datoteka';
        
        // Lösch-Button erstellen (anfangs versteckt)
        const deleteBtn = document.createElement('span');
        deleteBtn.className = 'delete-file-btn';
        deleteBtn.innerHTML = '<i class="fas fa-times"></i>';
        deleteBtn.style.cssText = 'display:none; margin-left:10px; color:#dc3545; cursor:pointer; padding:5px 10px; border-radius:4px; background:#fff0f0; font-size:14px;';
        deleteBtn.title = 'Ukloni datoteku';
        
        input.style.cssText = 'position:absolute; opacity:0; width:100%; height:100%; cursor:pointer; z-index:2; left:0; top:0;';
        
        const parent = input.parentNode;
        
        wrapper.appendChild(input);
        wrapper.appendChild(btn);
        wrapper.appendChild(nameSpan);
        wrapper.appendChild(deleteBtn);
        parent.appendChild(wrapper);
        
        // Datei auswählen
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
        
        // Datei löschen
        deleteBtn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            input.value = '';
            nameSpan.textContent = 'Nije odabrana datoteka';
            nameSpan.style.color = '#666';
            nameSpan.style.fontStyle = 'italic';
            deleteBtn.style.display = 'none';
        });
    });
});
</script>'''

if old_js in content:
    content = content.replace(old_js, new_js)
    print("✅ Lösch-Button hinzugefügt!")
else:
    print("⚠️ Altes JS nicht gefunden - prüfe manuell")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Fertig! Jetzt kann man Dateien einzeln löschen.")
