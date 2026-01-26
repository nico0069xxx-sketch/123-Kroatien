#!/usr/bin/env python3
"""
1. CTA Banner nur für HR anzeigen
2. Erste Box: HR-Version vs. internationale Version
"""

filepath = "templates/main/home.html"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. CTA Banner nur für HR
old_cta = '<!-- DIENSTLEISTER CTA BANNER -->\n    <section class="cta-professionals">'
new_cta = '<!-- DIENSTLEISTER CTA BANNER -->\n    {% if language == "hr" %}\n    <section class="cta-professionals">'

if old_cta in content:
    content = content.replace(old_cta, new_cta)
    print("✅ CTA Banner Start: {% if language == 'hr' %} hinzugefügt")

# CTA Banner Ende
old_cta_end = '<!-- END CTA BANNER -->'
new_cta_end = '{% endif %}\n    <!-- END CTA BANNER -->'

if old_cta_end in content and '{% endif %}\n    <!-- END CTA BANNER -->' not in content:
    content = content.replace(old_cta_end, new_cta_end)
    print("✅ CTA Banner Ende: {% endif %} hinzugefügt")

# 2. Erste Icon-Box: HR vs. International
old_box1 = '''<div class="col-md-6 col-lg-4">
                    <!-- CARD IMAGE -->
                    <div class="myCard">
                        <div class="iconDiv">
                            <i class="fa fa-comments-o myIcon" aria-hidden="true"></i>
                        </div>
                        <h6 class="mb-4">{{home_register_free}}</h6>
                        <p class="">{{home_register_text}}</p>
                    </div>
                </div>'''

new_box1 = '''<div class="col-md-6 col-lg-4">
                    <!-- CARD IMAGE -->
                    <div class="myCard">
                        <div class="iconDiv">
                            <i class="fa fa-comments-o myIcon" aria-hidden="true"></i>
                        </div>
                        {% if language == "hr" %}
                        <h6 class="mb-4">{{home_register_free}}</h6>
                        <p class="">{{home_register_text}}</p>
                        {% else %}
                        <h6 class="mb-4">{{home_platform_title}}</h6>
                        <p class="">{{home_platform_text}}</p>
                        {% endif %}
                    </div>
                </div>'''

if old_box1 in content:
    content = content.replace(old_box1, new_box1)
    print("✅ Erste Box: HR vs. International hinzugefügt")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Template aktualisiert!")
