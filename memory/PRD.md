# 123-KROATIEN.EU - AGENT BRIEFING
## BASELINE: ca2afa9 on main (28. Januar 2026)
## GITHUB: https://github.com/nico0069xxx-sketch/123-Kroatien

### USER: Nik (duzen, Deutsch, Mac M1, Laie)
### PROJEKT: Django Monolith, 12 Sprachen, SQLite/PostgreSQL

### SPRACH-SLUGS
ge=kroatien, en=croatia, hr=hrvatska, fr=croatie, nl=kroatie
pl=chorwacja, cz=chorvatsko, sk=chorvatsko, ru=horvatiya
gr=kroatia, sw=kroatien, no=kroatia

### IMPLEMENTIERT (28.01.2026)
- GEO/SEO: llms.txt, robots.txt, humans.txt, security.txt
- Schemas: Speakable, RealEstateListing, ItemList, BreadcrumbList
- OG-Tags + og-image.jpg (1200x630px)
- Exposé: QR-Code, Share, Druck, 12 Sprachen, Rate-Limiting
- Context Processors: breadcrumbs, og_meta, property_labels, country_name, status, expose_label

### WICHTIGE DATEIEN
- realstate/urls.py (Norwegisch explizit!)
- main/context_processors.py (Übersetzungen)
- main/expose_views.py
- templates/include/base.html

### OFFEN
P1: XML-Import testen
P2: Glossar, LocalBusiness Schema
P3: White Listing, 123-mallorca.eu
