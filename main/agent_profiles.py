#!/usr/bin/env python3
"""
MAKLERPROFILE-MODUL - E-E-A-T KÖNIGSKLASSE EDITION
Generiert professionelle, vertrauenswürdige Maklerprofile für 123-Kroatien.
E-E-A-T = Experience, Expertise, Authoritativeness, Trustworthiness
"""

import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Sprach-Konfiguration
LANGUAGES = {
    'ge': {'instruction': 'Schreibe auf Deutsch.', 'country': 'kroatien'},
    'en': {'instruction': 'Write in English.', 'country': 'croatia'},
    'fr': {'instruction': 'Écris en français.', 'country': 'croatie'},
    'hr': {'instruction': 'Piši na hrvatskom.', 'country': 'hrvatska'},
    'gr': {'instruction': 'Γράψε στα ελληνικά.', 'country': 'kroatia'},
    'pl': {'instruction': 'Pisz po polsku.', 'country': 'chorwacja'},
    'cz': {'instruction': 'Piš česky.', 'country': 'chorvatsko'},
    'ru': {'instruction': 'Пиши по-русски.', 'country': 'horvatiya'},
    'sw': {'instruction': 'Skriv på svenska.', 'country': 'kroatien'},
    'no': {'instruction': 'Skriv på norsk.', 'country': 'kroatia'},
    'sk': {'instruction': 'Píš po slovensky.', 'country': 'chorvatsko'},
    'nl': {'instruction': 'Schrijf in het Nederlands.', 'country': 'kroatie'},
}

# =============================================================================
# MASTER-PROMPT: MAKLERPROFILE (E-E-A-T OPTIMIERT)
# =============================================================================

AGENT_PROFILE_PROMPT = """You are a professional real-estate profile editor
specialized in broker credibility, compliance and trust.

Your task is to create a NEUTRAL, FACT-BASED, PROFESSIONAL
real estate agent profile for the Croatian marketplace 123-Kroatien.

The profile must be suitable for:
- persistent HTML pages
- multilingual SEO
- AI citation
- chatbot answers

------------------------------------------------
LANGUAGE HANDLING
------------------------------------------------

{lang_instruction}

- Use professional real-estate terminology of the target language.
- Do NOT use promotional or emotional wording.
- The brand name "123-kroatien.eu" must NOT be translated.

------------------------------------------------
STRUCTURE (MANDATORY - FOLLOW EXACTLY)
------------------------------------------------

**{agent_name} – Immobilienmakler in {region}**

**Profil-Zusammenfassung**
[2-3 sentences: Professional background, core activity, regional focus]

**Unternehmensinformationen**
• Unternehmen: {company}
• Standort: {region}, Kroatien
• Gegründet: {year_established}

**Fachgebiete**
• Immobilientypen: [based on specialization]
• Kundentypen: [domestic, international, investors]
• Dienstleistungen: [buying, selling, consulting, property management]

**Regionale Spezialisierung**
{regions_covered}

**Sprachen**
{languages_spoken}

**Zertifizierungen & Lizenzen**
• [Licensing information if provided]
• Verifizierter Partner von 123-kroatien.eu

**Arbeitsweise**
[Neutral description of typical cooperation process]

**Letztes Update: {month_year}**

------------------------------------------------
STRICT RULES
------------------------------------------------

- No advertising language
- No claims like "best", "leading", "top", "premium"
- No guarantees or promises
- No calls to action
- No unverifiable statements
- Professional and neutral tone
- Focus on facts and qualifications

------------------------------------------------
OUTPUT FORMAT
------------------------------------------------

- Plain text with ** for headings
- Use • for bullet points
- No HTML tags
- Clear paragraph separation

------------------------------------------------
BEGIN PROFILE NOW
------------------------------------------------"""


def generate_agent_profile(agent_data, language='ge'):
    """
    Generiert ein E-E-A-T-optimiertes Maklerprofil.
    
    Args:
        agent_data: dict mit agent_name, company, region, languages_spoken, 
                   regions_covered, year_established, specialization
        language: Sprachcode (z.B. 'ge', 'en')
    
    Returns:
        dict mit 'content', 'slug', 'url'
    """
    lang_config = LANGUAGES.get(language)
    if not lang_config:
        raise ValueError(f"Unbekannte Sprache: {language}")
    
    month_year = datetime.now().strftime('%B %Y')
    
    # Prompt zusammenbauen
    prompt = AGENT_PROFILE_PROMPT.format(
        lang_instruction=lang_config['instruction'],
        agent_name=agent_data.get('agent_name', 'Unbekannt'),
        company=agent_data.get('company', 'Unbekannt'),
        region=agent_data.get('region', 'Kroatien'),
        year_established=agent_data.get('year_established', 'Nicht angegeben'),
        regions_covered=agent_data.get('regions_covered', 'Kroatien'),
        languages_spoken=agent_data.get('languages_spoken', 'Deutsch, Englisch, Kroatisch'),
        month_year=month_year
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional profile editor focused on credibility and trust."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        # Slug generieren
        slug = agent_data.get('agent_name', 'agent').lower()
        slug = slug.replace(' ', '-').replace('.', '').replace(',', '')
        
        # URL generieren
        url = f"https://123-kroatien.eu/{language}/{lang_config['country']}/makler/{slug}/"
        
        return {
            'content': content,
            'slug': slug,
            'url': url,
            'agent_name': agent_data.get('agent_name'),
            'company': agent_data.get('company'),
            'region': agent_data.get('region'),
            'language': language,
            'generated_at': datetime.now().isoformat(),
        }
        
    except Exception as e:
        print(f"Fehler bei Profil-Generierung: {e}")
        return None


def generate_profile_all_languages(agent_data):
    """Generiert ein Maklerprofil in allen 12 Sprachen."""
    profiles = {}
    
    for lang_code in LANGUAGES.keys():
        print(f"  🌍 {lang_code}...", end=" ")
        profile = generate_agent_profile(agent_data, lang_code)
        
        if profile:
            profiles[lang_code] = profile
            print("✅")
        else:
            print("❌")
        
        import time
        time.sleep(1)
    
    return profiles


# =============================================================================
# DEMO / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("👔 MAKLERPROFIL-GENERATOR - E-E-A-T TEST")
    print("=" * 60)
    
    # Test-Daten für einen Beispiel-Makler
    test_agent = {
        'agent_name': 'Marko Horvat',
        'company': 'Adriatic Real Estate d.o.o.',
        'region': 'Istrien',
        'year_established': '2010',
        'regions_covered': 'Pula, Rovinj, Poreč, Umag, Novigrad',
        'languages_spoken': 'Deutsch, Englisch, Kroatisch, Italienisch',
        'specialization': 'Villen, Apartments, Neubauprojekte'
    }
    
    print(f"\n👤 Generiere Profil für: {test_agent['agent_name']}")
    print("-" * 40)
    
    profile = generate_agent_profile(test_agent, 'ge')
    
    if profile:
        print(f"\n✅ URL: {profile['url']}\n")
        print(profile['content'])
    else:
        print("❌ Fehler")
