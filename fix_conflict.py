#!/usr/bin/env python3
"""Löst den Merge-Konflikt in realstate/urls.py"""

filepath = "realstate/urls.py"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Ersetze den Konflikt-Bereich mit der korrekten Kombination
conflict_block = '''<<<<<<< HEAD
from main.views import set_language_from_url, news_page, sitemap as html_sitemap, imprint, agb, cancellation_policy, home
from main.xml_views import rss_listings, xml_sitemap, robots_txt
=======
from main.views import set_language_from_url, news_page, sitemap as html_sitemap, imprint, agb, cancellation_policy
from main.xml_views import rss_listings, xml_sitemap, robots_txt, llms_txt
>>>>>>> origin/main'''

resolved_code = '''from main.views import set_language_from_url, news_page, sitemap as html_sitemap, imprint, agb, cancellation_policy, home
from main.xml_views import rss_listings, xml_sitemap, robots_txt, llms_txt'''

content = content.replace(conflict_block, resolved_code)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ Konflikt gelöst!")
