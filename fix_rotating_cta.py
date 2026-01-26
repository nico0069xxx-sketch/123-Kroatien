#!/usr/bin/env python3
"""Ändert das Template für wechselnde CTA-Texte"""

filepath = "templates/main/home.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Alten CTA-Bereich ersetzen
old_cta = '''<div class="col-lg-9">
                    <h2 class="text-uppercase text-light">{{StartJourney}}</h2>
                    <p class="text-capitalize text-light">{{ReliableTransparent}}
                    </p>
                </div>'''

new_cta = '''<div class="col-lg-9">
                    <h2 class="text-uppercase text-light">{{StartJourney}}</h2>
                    <p class="text-capitalize text-light" id="rotating-cta-text" style="min-height: 50px; transition: opacity 0.5s ease;">{{ReliableTransparent}}</p>
                </div>
                <script>
                (function() {
                    const texts = [
                        "{{ReliableTransparent|escapejs}}",
                        "{{cta_rotating_1|escapejs}}",
                        "{{cta_rotating_2|escapejs}}",
                        "{{cta_rotating_3|escapejs}}",
                        "{{cta_rotating_4|escapejs}}",
                        "{{cta_rotating_5|escapejs}}",
                        "{{cta_rotating_6|escapejs}}",
                        "{{cta_rotating_7|escapejs}}",
                        "{{cta_rotating_8|escapejs}}",
                        "{{cta_rotating_9|escapejs}}",
                        "{{cta_rotating_10|escapejs}}",
                        "{{cta_rotating_11|escapejs}}",
                        "{{cta_rotating_12|escapejs}}"
                    ];
                    let currentIndex = 0;
                    const element = document.getElementById('rotating-cta-text');
                    
                    function rotateText() {
                        element.style.opacity = '0';
                        setTimeout(() => {
                            currentIndex = (currentIndex + 1) % texts.length;
                            element.textContent = texts[currentIndex];
                            element.style.opacity = '1';
                        }, 500);
                    }
                    
                    setInterval(rotateText, 5000);
                })();
                </script>'''

if old_cta in content:
    content = content.replace(old_cta, new_cta)
    print("✅ CTA-Bereich für wechselnde Texte aktualisiert!")
else:
    print("❌ CTA-Bereich nicht gefunden - manuell prüfen")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template gespeichert!")
