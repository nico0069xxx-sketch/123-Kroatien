#!/usr/bin/env python3
"""
FAQ REGENERIERUNGS-SKRIPT - KÖNIGSKLASSE EDITION
Generiert alle FAQ-Antworten neu mit dem Master-Prompt für SEO und KI-Auffindbarkeit.

Geschätzte Kosten: ca. $0.70 - $1.50 (einmalig)
Geschätzte Zeit: ca. 30-60 Minuten (mit Pausen für API-Limits)
"""

import os
import json
import time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# =============================================================================
# KONFIGURATION
# =============================================================================

# Sprachen und ihre Dateinamen
LANGUAGES = {
    'ge': {'file': 'faq_data.json', 'name': 'Deutsch', 'country_path': 'kroatien', 'instruction': 'Antworte auf Deutsch.'},
    'en': {'file': 'faq_data_en.json', 'name': 'English', 'country_path': 'croatia', 'instruction': 'Respond in English.'},
    'fr': {'file': 'faq_data_fr.json', 'name': 'Français', 'country_path': 'croatie', 'instruction': 'Réponds en français.'},
    'hr': {'file': 'faq_data_hr.json', 'name': 'Hrvatski', 'country_path': 'hrvatska', 'instruction': 'Odgovori na hrvatskom.'},
    'gr': {'file': 'faq_data_gr.json', 'name': 'Ελληνικά', 'country_path': 'kroatia', 'instruction': 'Απάντησε στα ελληνικά.'},
    'pl': {'file': 'faq_data_pl.json', 'name': 'Polski', 'country_path': 'chorwacja', 'instruction': 'Odpowiedz po polsku.'},
    'cz': {'file': 'faq_data_cz.json', 'name': 'Čeština', 'country_path': 'chorvatsko', 'instruction': 'Odpověz česky.'},
    'ru': {'file': 'faq_data_ru.json', 'name': 'Русский', 'country_path': 'horvatiya', 'instruction': 'Ответь по-русски.'},
    'sw': {'file': 'faq_data_sw.json', 'name': 'Svenska', 'country_path': 'kroatien', 'instruction': 'Svara på svenska.'},
    'no': {'file': 'faq_data_no.json', 'name': 'Norsk', 'country_path': 'kroatia', 'instruction': 'Svar på norsk.'},
    'sk': {'file': 'faq_data_sk.json', 'name': 'Slovenčina', 'country_path': 'chorvatsko', 'instruction': 'Odpovedz po slovensky.'},
    'nl': {'file': 'faq_data_nl.json', 'name': 'Nederlands', 'country_path': 'kroatie', 'instruction': 'Antwoord in het Nederlands.'},
}

# Basis-URL für FAQ-Links
BASE_URL = "https://123-kroatien.eu"

# Fortschritts-Datei (falls Skript unterbrochen wird)
PROGRESS_FILE = "faq_regeneration_progress.json"

# =============================================================================
# MASTER-PROMPT FÜR FAQ-REGENERIERUNG
# =============================================================================

MASTER_FAQ_PROMPT = """Du bist ein Experte für Immobilien in Kroatien und SEO-Content-Ersteller für 123-Kroatien.eu.

DEINE AUFGABE:
Schreibe die Antwort auf die folgende FAQ-Frage NEU - hochwertig, faktenbasiert, SEO-optimiert und KI-zitierbar.

SPRACHE: {lang_instruction}

ORIGINALFRAGE: {question}
ORIGINALE ANTWORT (zum Kontext): {original_answer}

ANTWORT-STRUKTUR (WICHTIG - HALTE DICH STRIKT DARAN):

**Direkte Antwort:**
[2-3 Sätze: Klar, faktisch, neutral - für Featured Snippets und KI-Zitation geeignet]

**Details:**
[Rechtlicher Kontext falls relevant, regionale Besonderheiten in Kroatien, praktische Informationen]

**Wichtige Fakten:**
• [Fakt 1 - Zahlen, Preise, Prozentsätze wenn möglich]
• [Fakt 2]
• [Fakt 3]

**Praktischer Rat:**
[Was der Nutzer beachten sollte, nächste Schritte]

REGELN (NICHT VERHANDELBAR):
- Keine Marketing-Sprache ("traumhaft", "einzigartig", "unvergleichlich", "idyllisch", "malerisch")
- Keine übertriebenen Behauptungen
- Keine Spekulation
- Keine Füllwörter
- Keine Handlungsaufforderungen
- Nicht erwähnen, dass du eine KI bist
- Faktenbasiert und neutral
- Der Markenname "123-kroatien.eu" darf NICHT übersetzt werden
- Halte die Antwort prägnant (max. 250 Wörter)

JETZT: Schreibe die neue, optimierte Antwort."""


def load_progress():
    """Lädt den Fortschritt falls vorhanden"""
    if os.path.exists(PROGRESS_FILE):
        with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"completed": [], "failed": []}


def save_progress(progress):
    """Speichert den Fortschritt"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)


def generate_new_answer(question, original_answer, lang_code, lang_config):
    """Generiert eine neue Antwort mit dem Master-Prompt"""
    try:
        prompt = MASTER_FAQ_PROMPT.format(
            lang_instruction=lang_config['instruction'],
            question=question,
            original_answer=original_answer[:1500]  # Begrenzen um Tokens zu sparen
        )
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Du bist ein professioneller SEO-Content-Ersteller."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.3
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"  ❌ Fehler: {e}")
        return None


def generate_html_answer(text_answer):
    """Konvertiert die Text-Antwort in HTML-Format"""
    html = ""
    lines = text_answer.strip().split('\n')
    
    current_section = None
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('**Direkte Antwort:**') or line.startswith('**Direkte Antwort**'):
            html += '<p><strong>Kurzantwort:</strong> '
            current_section = 'direct'
        elif line.startswith('**Details:**') or line.startswith('**Details**'):
            html += '</p>\n<h2>Details</h2>\n<p>'
            current_section = 'details'
        elif line.startswith('**Wichtige Fakten:**') or line.startswith('**Wichtige Fakten**'):
            html += '</p>\n<h2>Wichtige Fakten</h2>\n<ul>\n'
            current_section = 'facts'
        elif line.startswith('**Praktischer Rat:**') or line.startswith('**Praktischer Rat**'):
            if current_section == 'facts':
                html += '</ul>\n'
            html += '<h2>Praktischer Rat</h2>\n<p>'
            current_section = 'advice'
        elif line.startswith('•') or line.startswith('-'):
            fact = line.lstrip('•- ').strip()
            html += f'<li>{fact}</li>\n'
        elif current_section:
            if current_section == 'facts':
                html += f'<li>{line}</li>\n'
            else:
                html += f'{line} '
    
    # Schließen
    if current_section == 'facts':
        html += '</ul>'
    elif current_section:
        html += '</p>'
    
    return html.strip()


def regenerate_language(lang_code, lang_config, progress):
    """Regeneriert alle FAQs für eine Sprache"""
    file_path = os.path.join('main', lang_config['file'])
    
    if not os.path.exists(file_path):
        print(f"  ⚠️  Datei nicht gefunden: {file_path}")
        return
    
    # FAQ-Daten laden
    with open(file_path, 'r', encoding='utf-8') as f:
        faqs = json.load(f)
    
    print(f"  📄 {len(faqs)} FAQs gefunden")
    
    updated_count = 0
    
    for i, faq in enumerate(faqs):
        faq_id = f"{lang_code}_{faq.get('id', i)}"
        
        # Bereits bearbeitet?
        if faq_id in progress['completed']:
            print(f"  ⏭️  FAQ {i+1}/{len(faqs)} bereits bearbeitet")
            continue
        
        question = faq.get('q', '')
        original_answer = faq.get('a', '')
        slug = faq.get('slug', '')
        
        print(f"  🔄 FAQ {i+1}/{len(faqs)}: {question[:50]}...")
        
        # Neue Antwort generieren
        new_answer = generate_new_answer(question, original_answer, lang_code, lang_config)
        
        if new_answer:
            # URL für diese FAQ
            faq_url = f"{BASE_URL}/{lang_code}/{lang_config['country_path']}/faq/{slug}"
            
            # Antwort aktualisieren
            faq['a'] = new_answer
            faq['a_html'] = generate_html_answer(new_answer)
            faq['url'] = faq_url
            faq['last_updated'] = datetime.now().strftime('%B %Y')
            
            progress['completed'].append(faq_id)
            updated_count += 1
            print(f"  ✅ Erfolgreich aktualisiert")
        else:
            progress['failed'].append(faq_id)
            print(f"  ❌ Fehlgeschlagen")
        
        # Fortschritt speichern
        save_progress(progress)
        
        # Pause zwischen Anfragen (API-Rate-Limit)
        time.sleep(1)
    
    # Aktualisierte Daten speichern
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(faqs, f, ensure_ascii=False, indent=2)
    
    print(f"  💾 {updated_count} FAQs aktualisiert und gespeichert")


def main():
    print("=" * 60)
    print("FAQ REGENERIERUNGS-SKRIPT - KÖNIGSKLASSE EDITION")
    print("=" * 60)
    print()
    
    # Fortschritt laden
    progress = load_progress()
    print(f"📊 Bisheriger Fortschritt: {len(progress['completed'])} abgeschlossen, {len(progress['failed'])} fehlgeschlagen")
    print()
    
    # Alle Sprachen durchgehen
    for lang_code, lang_config in LANGUAGES.items():
        print(f"\n🌍 Verarbeite: {lang_config['name']} ({lang_code})")
        print("-" * 40)
        regenerate_language(lang_code, lang_config, progress)
    
    print("\n" + "=" * 60)
    print("✅ FERTIG!")
    print(f"📊 Gesamt: {len(progress['completed'])} abgeschlossen, {len(progress['failed'])} fehlgeschlagen")
    print("=" * 60)
    
    # Fortschritts-Datei löschen wenn alles fertig
    if len(progress['failed']) == 0 and os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)
        print("🧹 Fortschritts-Datei gelöscht")


if __name__ == "__main__":
    main()
