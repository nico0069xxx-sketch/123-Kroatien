#!/usr/bin/env python3
"""
MARKTBERICHTE-MODUL - KÖNIGSKLASSE EDITION
Generiert SEO-optimierte, KI-zitierbare Immobilien-Marktberichte für Kroatien.
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key) if api_key else None

# =============================================================================
# KONFIGURATION: REGIONEN IN KROATIEN
# =============================================================================

REGIONS = {
    'istrien': {
        'name_de': 'Istrien',
        'name_en': 'Istria',
        'name_hr': 'Istra',
        'cities': ['Pula', 'Rovinj', 'Poreč', 'Umag', 'Novigrad', 'Labin'],
        'slug': 'istrien',
    },
    'kvarner': {
        'name_de': 'Kvarner',
        'name_en': 'Kvarner',
        'name_hr': 'Kvarner',
        'cities': ['Rijeka', 'Opatija', 'Crikvenica', 'Krk', 'Rab', 'Lošinj'],
        'slug': 'kvarner',
    },
    'dalmatien-nord': {
        'name_de': 'Nord-Dalmatien',
        'name_en': 'Northern Dalmatia',
        'name_hr': 'Sjeverna Dalmacija',
        'cities': ['Zadar', 'Šibenik', 'Biograd', 'Nin', 'Vodice'],
        'slug': 'dalmatien-nord',
    },
    'dalmatien-mitte': {
        'name_de': 'Mittel-Dalmatien',
        'name_en': 'Central Dalmatia',
        'name_hr': 'Srednja Dalmacija',
        'cities': ['Split', 'Trogir', 'Makarska', 'Omiš', 'Brač', 'Hvar'],
        'slug': 'dalmatien-mitte',
    },
    'dalmatien-sued': {
        'name_de': 'Süd-Dalmatien',
        'name_en': 'Southern Dalmatia',
        'name_hr': 'Južna Dalmacija',
        'cities': ['Dubrovnik', 'Korčula', 'Pelješac', 'Mljet', 'Cavtat'],
        'slug': 'dalmatien-sued',
    },
    'zagreb': {
        'name_de': 'Zagreb & Umgebung',
        'name_en': 'Zagreb & Surroundings',
        'name_hr': 'Zagreb i okolica',
        'cities': ['Zagreb', 'Samobor', 'Velika Gorica', 'Zaprešić'],
        'slug': 'zagreb',
    },
    'slavonien': {
        'name_de': 'Slavonien',
        'name_en': 'Slavonia',
        'name_hr': 'Slavonija',
        'cities': ['Osijek', 'Vukovar', 'Đakovo', 'Vinkovci', 'Slavonski Brod'],
        'slug': 'slavonien',
    },
    'lika-gorski-kotar': {
        'name_de': 'Lika & Gorski Kotar',
        'name_en': 'Lika & Gorski Kotar',
        'name_hr': 'Lika i Gorski kotar',
        'cities': ['Gospić', 'Delnice', 'Plitvice', 'Otočac'],
        'slug': 'lika-gorski-kotar',
    },
}

# Sprach-Konfiguration
LANGUAGES = {
    'ge': {'instruction': 'Schreibe auf Deutsch.', 'country': 'kroatien', 'report': 'Marktbericht'},
    'en': {'instruction': 'Write in English.', 'country': 'croatia', 'report': 'Market Report'},
    'fr': {'instruction': 'Écris en français.', 'country': 'croatie', 'report': 'Rapport de Marché'},
    'hr': {'instruction': 'Piši na hrvatskom.', 'country': 'hrvatska', 'report': 'Tržišno Izvješće'},
    'gr': {'instruction': 'Γράψε στα ελληνικά.', 'country': 'kroatia', 'report': 'Έκθεση Αγοράς'},
    'pl': {'instruction': 'Pisz po polsku.', 'country': 'chorwacja', 'report': 'Raport Rynkowy'},
    'cz': {'instruction': 'Piš česky.', 'country': 'chorvatsko', 'report': 'Tržní Zpráva'},
    'ru': {'instruction': 'Пиши по-русски.', 'country': 'horvatiya', 'report': 'Обзор Рынка'},
    'sw': {'instruction': 'Skriv på svenska.', 'country': 'kroatien', 'report': 'Marknadsrapport'},
    'no': {'instruction': 'Skriv på norsk.', 'country': 'kroatia', 'report': 'Markedsrapport'},
    'sk': {'instruction': 'Píš po slovensky.', 'country': 'chorvatsko', 'report': 'Správa o Trhu'},
    'nl': {'instruction': 'Schrijf in het Nederlands.', 'country': 'kroatie', 'report': 'Marktrapport'},
}

# =============================================================================
# MASTER-PROMPT: MARKTBERICHTE (KÖNIGSKLASSE)
# =============================================================================

MARKET_REPORT_PROMPT = """You are a senior real-estate market analyst and editor
specialized in the Croatian property market.

Your task is to create a DATA-DRIVEN, NEUTRAL, AI-CITABLE
real estate market report for the portal 123-Kroatien.

The content must be suitable for:
- persistent HTML publication
- multilingual SEO (hreflang compatible)
- AI citation (Google AI Overviews, ChatGPT, Perplexity)
- chatbot retrieval (RAG)

------------------------------------------------
LANGUAGE HANDLING
------------------------------------------------

{lang_instruction}

- Do NOT translate word-by-word.
- Localize terminology and buyer perspective for the target language.
- Maintain factual equivalence across all languages.
- The brand name "123-kroatien.eu" must NOT be translated.

------------------------------------------------
STRUCTURE (MANDATORY - FOLLOW EXACTLY)
------------------------------------------------

1. H1:
   "{region_name} {report_word} {year}"

2. Executive Summary (3–4 sentences):
   - Neutral overview of market situation
   - Price trend direction
   - Demand level

3. Price Analysis:
   - Average price per m² (use realistic 2024/2025 data for Croatia)
   - Price range (low / high)
   - Trend compared to previous year

4. Supply & Demand:
   - Buyer demand (domestic vs foreign)
   - Supply situation
   - Time on market (if applicable)

5. Regional Highlights:
   - Key subregions or cities: {cities}
   - Differences within the region

6. Buyer & Investor Profile:
   - Typical buyers
   - Main motivations (living, vacation, investment)

7. Outlook:
   - Short-term expectations (neutral, no speculation)
   - Factors influencing the market

8. Key Data (Bullet Points):
   - Structured facts only
   - Use • for bullet points

9. Last Updated:
   "Last updated: {month_year}"

------------------------------------------------
STRICT RULES
------------------------------------------------

- No marketing language
- No sales claims
- No calls to action
- No speculation or predictions without basis
- No reference to being an AI
- Use clear, verifiable wording
- Use realistic price data for Croatian real estate market 2024/2025:
  * Istria/Dalmatia coast: €2,500-5,000+/m²
  * Zagreb: €2,000-3,500/m²
  * Slavonia/inland: €800-1,500/m²

------------------------------------------------
OUTPUT FORMAT
------------------------------------------------

- Plain text with clear paragraph separation
- Use ** for headings (e.g., **Executive Summary**)
- Use • for bullet points
- No HTML tags

------------------------------------------------
BEGIN REPORT NOW
------------------------------------------------"""


def generate_market_report(region_key, language='ge', year=None):
    """
    Generiert einen Marktbericht für eine Region und Sprache.
    
    Args:
        region_key: Schlüssel der Region (z.B. 'istrien')
        language: Sprachcode (z.B. 'ge', 'en')
        year: Jahr für den Bericht (Standard: aktuelles Jahr)
    
    Returns:
        dict mit 'content', 'title', 'slug', 'url'
    """
    if year is None:
        year = datetime.now().year
    
    if region_key not in REGIONS:
        raise ValueError(f"Unbekannte Region: {region_key}")
    
    if language not in LANGUAGES:
        raise ValueError(f"Unbekannte Sprache: {language}")
    
    region = REGIONS[region_key]
    lang_config = LANGUAGES[language]
    
    # Region-Name in passender Sprache (Fallback auf Deutsch)
    region_name = region.get(f'name_{language[:2]}', region['name_de'])
    if language == 'ge':
        region_name = region['name_de']
    elif language == 'en':
        region_name = region['name_en']
    elif language == 'hr':
        region_name = region['name_hr']
    else:
        region_name = region['name_de']  # Fallback
    
    month_year = datetime.now().strftime('%B %Y')
    
    # Prompt zusammenbauen
    prompt = MARKET_REPORT_PROMPT.format(
        lang_instruction=lang_config['instruction'],
        region_name=region_name,
        report_word=lang_config['report'],
        year=year,
        cities=', '.join(region['cities']),
        month_year=month_year
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-16k",  # Größeres Kontextfenster für längere Berichte
            messages=[
                {"role": "system", "content": "You are a professional real estate market analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        # URL generieren
        slug = f"{region['slug']}-{year}"
        url = f"https://123-kroatien.eu/{language}/{lang_config['country']}/marktbericht/{slug}/"
        
        # Titel extrahieren (erste Zeile oder H1)
        lines = content.strip().split('\n')
        title = lines[0].replace('**', '').replace('#', '').strip()
        
        return {
            'content': content,
            'title': title,
            'slug': slug,
            'url': url,
            'region': region_key,
            'region_name': region_name,
            'language': language,
            'year': year,
            'generated_at': datetime.now().isoformat(),
            'last_updated': month_year
        }
        
    except Exception as e:
        print(f"Fehler bei Marktbericht-Generierung: {e}")
        return None


def generate_all_reports_for_region(region_key, year=None):
    """Generiert Marktberichte für eine Region in allen 12 Sprachen."""
    reports = {}
    
    for lang_code in LANGUAGES.keys():
        print(f"  🌍 Generiere {lang_code}...")
        report = generate_market_report(region_key, lang_code, year)
        if report:
            reports[lang_code] = report
        
        # Pause für API-Rate-Limit
        import time
        time.sleep(1)
    
    return reports


def generate_all_reports(year=None):
    """Generiert alle Marktberichte für alle Regionen und Sprachen."""
    all_reports = {}
    
    for region_key in REGIONS.keys():
        print(f"\n📊 Region: {REGIONS[region_key]['name_de']}")
        print("-" * 40)
        all_reports[region_key] = generate_all_reports_for_region(region_key, year)
    
    return all_reports


def save_reports_to_json(reports, output_dir='main/market_reports'):
    """Speichert alle Berichte als JSON-Dateien."""
    os.makedirs(output_dir, exist_ok=True)
    
    for region_key, lang_reports in reports.items():
        for lang_code, report in lang_reports.items():
            filename = f"{region_key}_{report['year']}_{lang_code}.json"
            filepath = os.path.join(output_dir, filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            
            print(f"  💾 Gespeichert: {filename}")


def convert_to_html(content):
    """Konvertiert den Plain-Text-Bericht in HTML."""
    html = ""
    lines = content.strip().split('\n')
    
    in_list = False
    
    for line in lines:
        line = line.strip()
        if not line:
            if in_list:
                html += "</ul>\n"
                in_list = False
            html += "\n"
            continue
        
        # Überschriften
        if line.startswith('**') and line.endswith('**'):
            if in_list:
                html += "</ul>\n"
                in_list = False
            heading = line.strip('*').strip()
            # H1 für Titel, H2 für Unterüberschriften
            if 'Marktbericht' in heading or 'Market Report' in heading or 'Rapport' in heading:
                html += f"<h1>{heading}</h1>\n"
            else:
                html += f"<h2>{heading}</h2>\n"
        
        # Aufzählungspunkte
        elif line.startswith('•') or line.startswith('-'):
            if not in_list:
                html += "<ul>\n"
                in_list = True
            item = line.lstrip('•- ').strip()
            html += f"<li>{item}</li>\n"
        
        # Normaler Absatz
        else:
            if in_list:
                html += "</ul>\n"
                in_list = False
            # Fett-Text konvertieren
            import re
            line = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', line)
            html += f"<p>{line}</p>\n"
    
    if in_list:
        html += "</ul>\n"
    
    return html


# =============================================================================
# DEMO / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("MARKTBERICHT-GENERATOR - TEST")
    print("=" * 60)
    
    # Test: Ein Bericht für Istrien auf Deutsch
    print("\n📊 Generiere Marktbericht für Istrien (Deutsch)...")
    report = generate_market_report('istrien', 'ge', 2025)
    
    if report:
        print(f"\n✅ Titel: {report['title']}")
        print(f"📍 URL: {report['url']}")
        print(f"\n--- INHALT ---\n")
        print(report['content'])
    else:
        print("❌ Fehler bei der Generierung")
