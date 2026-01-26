#!/usr/bin/env python3
"""Fügt die Länder-Flaggen Section hinzu"""

filepath = "templates/main/partner_landing.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Flaggen-Section nach der Info-Section einfügen (vor WHO CAN REGISTER)
flags_section = '''
<!-- COUNTRIES SECTION -->
<section class="py-5" style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);">
    <div class="container">
        <div class="row align-items-center">
            <div class="col-lg-5 mb-4 mb-lg-0">
                <h2 style="color: #003167;">Vaš profil u 12 europskih zemalja</h2>
                <p class="lead" style="color: #666;">
                    Međunarodni kupci iz cijele Europe pretražuju nekretnine u Hrvatskoj. 
                    Vaš profil automatski se prikazuje na njihovom jeziku.
                </p>
            </div>
            <div class="col-lg-7">
                <div style="display: flex; flex-wrap: wrap; gap: 12px; justify-content: center;">
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇩🇪 Njemačka</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇬🇧 Engleska</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇫🇷 Francuska</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇬🇷 Grčka</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇭🇷 Hrvatska</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇵🇱 Poljska</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇨🇿 Češka</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇷🇺 Rusija</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇸🇪 Švedska</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇳🇴 Norveška</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇸🇰 Slovačka</span>
                    <span style="background: white; padding: 12px 20px; border-radius: 10px; box-shadow: 0 2px 15px rgba(0,0,0,0.08); font-weight: 500; font-size: 0.95rem;">🇳🇱 Nizozemska</span>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- WHO CAN REGISTER -->'''

# Ersetze den Anfang der WHO CAN REGISTER Section
old_text = '<!-- WHO CAN REGISTER -->'
content = content.replace(old_text, flags_section)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Länder-Flaggen Section hinzugefügt!")
print("   - 12 Länder mit Flaggen-Emojis")
print("   - Ansprechendes Card-Design")
print("   - Kroatischer Text")
