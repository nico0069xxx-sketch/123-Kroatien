"""
Glossar Auto-Link Template Filter
Verlinkt automatisch Glossar-Begriffe in Texten.

Verwendung im Template:
{% load glossary_links %}
{{ listing.description|glossary_autolink:language }}
"""

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import escape
import re

register = template.Library()

# Glossar-Begriffe mit ihren Slugs (für alle Sprachen)
# Diese Liste kann später aus der Datenbank geladen werden
GLOSSARY_TERMS = {
    "ge": {
        # Begriff: (slug, kurze Definition für Tooltip)
        "Grundbuch": ("grundbuch", "Öffentliches Register für Grundstücke"),
        "Kaufvertrag": ("kaufvertrag", "Rechtsgültiger Vertrag beim Immobilienkauf"),
        "Notar": ("notar", "Amtsperson für Beurkundungen"),
        "Makler": ("makler", "Vermittler zwischen Käufer und Verkäufer"),
        "Provision": ("provision", "Vergütung für den Makler"),
        "Grunderwerbsteuer": ("grunderwerbsteuer", "Steuer beim Immobilienkauf"),
        "Eigentumsübertragung": ("eigentumsuebertragung", "Rechtliche Übertragung des Eigentums"),
        "OIB": ("oib", "Kroatische Steueridentifikationsnummer"),
        "Bauland": ("bauland", "Grundstück mit Baugenehmigung"),
        "Wohnfläche": ("wohnflaeche", "Nutzbare Fläche einer Immobilie"),
        "Neubau": ("neubau", "Neu errichtetes Gebäude"),
        "Altbau": ("altbau", "Historisches Gebäude"),
        "Meerblick": ("meerblick", "Sicht auf das Meer"),
        "Energieausweis": ("energieausweis", "Dokument zur Energieeffizienz"),
        "Hypothek": ("hypothek", "Grundpfandrecht zur Kreditsicherung"),
        "Kataster": ("kataster", "Amtliches Verzeichnis von Grundstücken"),
        "Baugenehmigung": ("baugenehmigung", "Behördliche Erlaubnis zum Bauen"),
        "Quadratmeter": ("quadratmeter", "Maßeinheit für Flächen"),
        "Terrasse": ("terrasse", "Außenbereich einer Wohnung"),
        "Pool": ("pool", "Schwimmbecken"),
    },
    "en": {
        "Land Registry": ("land-registry", "Public register for properties"),
        "Purchase Agreement": ("purchase-agreement", "Legal contract for property purchase"),
        "Notary": ("notary", "Public official for certifications"),
        "Real Estate Agent": ("real-estate-agent", "Intermediary between buyer and seller"),
        "Commission": ("commission", "Fee for the agent"),
        "Property Tax": ("property-tax", "Tax on property purchase"),
        "OIB": ("oib", "Croatian tax identification number"),
        "Building Land": ("building-land", "Land with building permit"),
        "Living Space": ("living-space", "Usable area of a property"),
        "New Build": ("new-build", "Newly constructed building"),
        "Sea View": ("sea-view", "View of the sea"),
        "Energy Certificate": ("energy-certificate", "Document on energy efficiency"),
        "Mortgage": ("mortgage", "Land charge for loan security"),
        "Cadastre": ("cadastre", "Official register of land parcels"),
        "Building Permit": ("building-permit", "Official permission to build"),
    },
    "hr": {
        "Zemljišna knjiga": ("zemljisna-knjiga", "Javni registar nekretnina"),
        "Kupoprodajni ugovor": ("kupoprodajni-ugovor", "Pravni ugovor o kupnji"),
        "Javni bilježnik": ("javni-biljeznk", "Službena osoba za ovjere"),
        "Agent za nekretnine": ("agent-za-nekretnine", "Posrednik između kupca i prodavatelja"),
        "Provizija": ("provizija", "Naknada za agenta"),
        "Porez na promet nekretnina": ("porez-na-promet-nekretnina", "Porez pri kupnji nekretnine"),
        "OIB": ("oib", "Hrvatski osobni identifikacijski broj"),
        "Građevinsko zemljište": ("gradevinsko-zemljiste", "Zemljište s građevinskom dozvolom"),
        "Stambena površina": ("stambena-povrsina", "Korisna površina nekretnine"),
        "Novogradnja": ("novogradnja", "Novoizgrađena zgrada"),
        "Pogled na more": ("pogled-na-more", "Pogled na more"),
        "Energetski certifikat": ("energetski-certifikat", "Dokument o energetskoj učinkovitosti"),
        "Hipoteka": ("hipoteka", "Založno pravo za osiguranje kredita"),
        "Katastar": ("katastar", "Službeni registar zemljišnih čestica"),
        "Građevinska dozvola": ("gradevinska-dozvola", "Službena dozvola za gradnju"),
    },
}

# URL-Pfade für Glossar pro Sprache
GLOSSARY_BASE_URLS = {
    "ge": "/ge/kroatien/glossar/",
    "en": "/en/croatia/glossary/",
    "hr": "/hr/hrvatska/pojmovnik/",
    "fr": "/fr/croatie/glossaire/",
    "nl": "/nl/kroatie/woordenlijst/",
    "pl": "/pl/chorwacja/slownik/",
    "cz": "/cz/chorvatsko/glosar/",
    "sk": "/sk/chorvatsko/slovnik/",
    "ru": "/ru/horvatiya/glossarij/",
    "gr": "/gr/kroatia/glossari/",
    "sw": "/sw/kroatien/ordlista/",
    "no": "/no/kroatia/ordliste/",
}


@register.filter(name='glossary_autolink')
def glossary_autolink(text, language='ge'):
    """
    Ersetzt Glossar-Begriffe im Text durch Links.
    
    Verwendung:
    {{ description|glossary_autolink:"ge" }}
    {{ description|glossary_autolink:language }}
    """
    if not text:
        return text
    
    # Hole Begriffe für die aktuelle Sprache (fallback zu Deutsch)
    terms = GLOSSARY_TERMS.get(language, GLOSSARY_TERMS.get('ge', {}))
    base_url = GLOSSARY_BASE_URLS.get(language, GLOSSARY_BASE_URLS['ge'])
    
    # Text escapen für Sicherheit
    escaped_text = escape(text)
    
    # Begriffe nach Länge sortieren (längste zuerst, um Teilmatches zu vermeiden)
    sorted_terms = sorted(terms.keys(), key=len, reverse=True)
    
    # Set um bereits verlinkte Begriffe zu tracken (nur 1x pro Begriff verlinken)
    linked_terms = set()
    
    for term in sorted_terms:
        if term.lower() in linked_terms:
            continue
            
        slug, tooltip = terms[term]
        
        # Case-insensitive Suche, aber nur ganze Wörter
        pattern = r'\b(' + re.escape(term) + r')\b'
        
        def replace_first(match):
            if term.lower() in linked_terms:
                return match.group(0)  # Bereits verlinkt, nicht ersetzen
            linked_terms.add(term.lower())
            matched_term = match.group(1)
            return f'<a href="{base_url}{slug}/" class="glossary-link" title="{tooltip}" data-toggle="tooltip">{matched_term}</a>'
        
        # Nur das erste Vorkommen ersetzen
        escaped_text = re.sub(pattern, replace_first, escaped_text, count=1, flags=re.IGNORECASE)
    
    return mark_safe(escaped_text)


@register.filter(name='glossary_highlight')
def glossary_highlight(text, language='ge'):
    """
    Markiert Glossar-Begriffe ohne sie zu verlinken (für Previews).
    
    Verwendung:
    {{ description|glossary_highlight:"ge" }}
    """
    if not text:
        return text
    
    terms = GLOSSARY_TERMS.get(language, GLOSSARY_TERMS.get('ge', {}))
    escaped_text = escape(text)
    
    for term in terms.keys():
        pattern = r'\b(' + re.escape(term) + r')\b'
        escaped_text = re.sub(
            pattern, 
            r'<mark class="glossary-term">\1</mark>', 
            escaped_text, 
            count=1, 
            flags=re.IGNORECASE
        )
    
    return mark_safe(escaped_text)
