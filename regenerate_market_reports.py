#!/usr/bin/env python3
import os, json, time
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

REGIONS = {
    'istrien': {'name_de': 'Istrien', 'name_en': 'Istria', 'cities': ['Pula', 'Rovinj', 'Poreč', 'Umag'], 'slug': 'istrien'},
    'kvarner': {'name_de': 'Kvarner', 'name_en': 'Kvarner', 'cities': ['Rijeka', 'Opatija', 'Krk', 'Rab'], 'slug': 'kvarner'},
    'dalmatien-nord': {'name_de': 'Nord-Dalmatien', 'name_en': 'Northern Dalmatia', 'cities': ['Zadar', 'Šibenik', 'Biograd'], 'slug': 'dalmatien-nord'},
    'dalmatien-mitte': {'name_de': 'Mittel-Dalmatien', 'name_en': 'Central Dalmatia', 'cities': ['Split', 'Trogir', 'Makarska', 'Hvar'], 'slug': 'dalmatien-mitte'},
    'dalmatien-sued': {'name_de': 'Süd-Dalmatien', 'name_en': 'Southern Dalmatia', 'cities': ['Dubrovnik', 'Korčula', 'Cavtat'], 'slug': 'dalmatien-sued'},
    'zagreb': {'name_de': 'Zagreb', 'name_en': 'Zagreb', 'cities': ['Zagreb', 'Samobor'], 'slug': 'zagreb'},
    'slavonien': {'name_de': 'Slavonien', 'name_en': 'Slavonia', 'cities': ['Osijek', 'Vukovar'], 'slug': 'slavonien'},
    'lika-gorski-kotar': {'name_de': 'Lika & Gorski Kotar', 'name_en': 'Lika', 'cities': ['Gospić', 'Plitvice'], 'slug': 'lika-gorski-kotar'},
}

HEADINGS = {
    'ge': {'title': '{region} Marktbericht {year}', 'summary': 'Zusammenfassung', 'price': 'Preisanalyse', 'supply': 'Angebot & Nachfrage', 'regional': 'Regionale Highlights', 'buyer': 'Käufer- & Investorenprofil', 'outlook': 'Ausblick', 'keydata': 'Wichtige Daten', 'updated': 'Letztes Update', 'instruction': 'Schreibe auf Deutsch.', 'lang_name': 'German'},
    'en': {'title': '{region} Market Report {year}', 'summary': 'Executive Summary', 'price': 'Price Analysis', 'supply': 'Supply & Demand', 'regional': 'Regional Highlights', 'buyer': 'Buyer & Investor Profile', 'outlook': 'Outlook', 'keydata': 'Key Data', 'updated': 'Last Updated', 'instruction': 'Write in English.', 'lang_name': 'English'},
    'hr': {'title': '{region} Tržišno Izvješće {year}', 'summary': 'Sažetak', 'price': 'Analiza Cijena', 'supply': 'Ponuda i Potražnja', 'regional': 'Regionalni Pregled', 'buyer': 'Profil Kupaca i Investitora', 'outlook': 'Prognoze', 'keydata': 'Ključni Podaci', 'updated': 'Zadnje Ažuriranje', 'instruction': 'Piši na hrvatskom.', 'lang_name': 'Croatian'},
    'fr': {'title': 'Rapport de Marché {region} {year}', 'summary': 'Résumé', 'price': 'Analyse des Prix', 'supply': 'Offre et Demande', 'regional': 'Points Régionaux', 'buyer': 'Profil Acheteurs', 'outlook': 'Perspectives', 'keydata': 'Données Clés', 'updated': 'Dernière MAJ', 'instruction': 'Écris en français.', 'lang_name': 'French'},
    'nl': {'title': '{region} Marktrapport {year}', 'summary': 'Samenvatting', 'price': 'Prijsanalyse', 'supply': 'Vraag en Aanbod', 'regional': 'Regionale Highlights', 'buyer': 'Kopersprofiel', 'outlook': 'Vooruitzichten', 'keydata': 'Belangrijke Data', 'updated': 'Laatst Bijgewerkt', 'instruction': 'Schrijf in het Nederlands.', 'lang_name': 'Dutch'},
    'pl': {'title': 'Raport Rynkowy {region} {year}', 'summary': 'Podsumowanie', 'price': 'Analiza Cen', 'supply': 'Podaż i Popyt', 'regional': 'Przegląd Regionalny', 'buyer': 'Profil Kupującego', 'outlook': 'Perspektywy', 'keydata': 'Kluczowe Dane', 'updated': 'Ostatnia Aktualizacja', 'instruction': 'Pisz po polsku.', 'lang_name': 'Polish'},
    'cz': {'title': 'Tržní Zpráva {region} {year}', 'summary': 'Shrnutí', 'price': 'Analýza Cen', 'supply': 'Nabídka a Poptávka', 'regional': 'Regionální Přehled', 'buyer': 'Profil Kupujících', 'outlook': 'Výhled', 'keydata': 'Klíčová Data', 'updated': 'Poslední Aktualizace', 'instruction': 'Piš česky.', 'lang_name': 'Czech'},
    'sk': {'title': 'Správa o Trhu {region} {year}', 'summary': 'Zhrnutie', 'price': 'Analýza Cien', 'supply': 'Ponuka a Dopyt', 'regional': 'Regionálny Prehľad', 'buyer': 'Profil Kupujúcich', 'outlook': 'Výhľad', 'keydata': 'Kľúčové Údaje', 'updated': 'Posledná Aktualizácia', 'instruction': 'Píš po slovensky.', 'lang_name': 'Slovak'},
    'ru': {'title': 'Обзор Рынка {region} {year}', 'summary': 'Резюме', 'price': 'Анализ Цен', 'supply': 'Спрос и Предложение', 'regional': 'Региональный Обзор', 'buyer': 'Профиль Покупателя', 'outlook': 'Прогноз', 'keydata': 'Ключевые Данные', 'updated': 'Последнее Обновление', 'instruction': 'Пиши по-русски.', 'lang_name': 'Russian'},
    'gr': {'title': 'Έκθεση Αγοράς {region} {year}', 'summary': 'Περίληψη', 'price': 'Ανάλυση Τιμών', 'supply': 'Προσφορά & Ζήτηση', 'regional': 'Περιφερειακά', 'buyer': 'Προφίλ Αγοραστή', 'outlook': 'Προοπτικές', 'keydata': 'Βασικά Στοιχεία', 'updated': 'Τελευταία Ενημέρωση', 'instruction': 'Γράψε στα ελληνικά.', 'lang_name': 'Greek'},
    'sw': {'title': '{region} Marknadsrapport {year}', 'summary': 'Sammanfattning', 'price': 'Prisanalys', 'supply': 'Utbud & Efterfrågan', 'regional': 'Regionala Höjdpunkter', 'buyer': 'Köparprofil', 'outlook': 'Utsikter', 'keydata': 'Nyckeldata', 'updated': 'Senast Uppdaterad', 'instruction': 'Skriv på svenska.', 'lang_name': 'Swedish'},
    'no': {'title': '{region} Markedsrapport {year}', 'summary': 'Sammendrag', 'price': 'Prisanalyse', 'supply': 'Tilbud & Etterspørsel', 'regional': 'Regionale Høydepunkter', 'buyer': 'Kjøperprofil', 'outlook': 'Utsikter', 'keydata': 'Nøkkeldata', 'updated': 'Sist Oppdatert', 'instruction': 'Skriv på norsk.', 'lang_name': 'Norwegian'},
}

def generate_report(region_key, lang, year=2025):
    h = HEADINGS[lang]
    region = REGIONS[region_key]
    region_name = region['name_de']
    
    prompt = f"""{h['instruction']}

Create a real estate market report for {region_name}, Croatia.

USE THESE EXACT HEADINGS (in {h['lang_name']}):

**{h['title'].format(region=region_name, year=year)}**

**{h['summary']}**
[3-4 sentences about market situation]

**{h['price']}**
• Average price/m²: €X,XXX-X,XXX
• Price range: low-high
• Trend vs last year

**{h['supply']}**
• Demand: domestic vs foreign
• Supply situation

**{h['regional']}**
Cities: {', '.join(region['cities'])}

**{h['buyer']}**
• Typical buyers
• Motivations

**{h['outlook']}**
[Short-term expectations]

**{h['keydata']}**
• Fact 1
• Fact 2
• Fact 3

**{h['updated']}: January 2025**

Use realistic Croatian prices: Coast €2,500-5,000/m², Zagreb €2,000-3,500/m², Inland €800-1,500/m²"""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000, temperature=0.3
        )
        return {'content': response.choices[0].message.content, 'region': region_key, 'region_name': region_name, 'year': year, 'slug': f"{region['slug']}-{year}"}
    except Exception as e:
        print(f"Error: {e}")
        return None

# Main
os.makedirs('main/market_reports_data', exist_ok=True)
total = len(REGIONS) * len(HEADINGS)
count = 0

for region_key in REGIONS:
    print(f"\n📊 {REGIONS[region_key]['name_de']}")
    for lang in HEADINGS:
        count += 1
        print(f"  [{count}/{total}] {lang}...", end=" ")
        report = generate_report(region_key, lang)
        if report:
            with open(f"main/market_reports_data/{region_key}_2025_{lang}.json", 'w') as f:
                json.dump(report, f, ensure_ascii=False, indent=2)
            print("✅")
        else:
            print("❌")
        time.sleep(1)

print(f"\n🎉 Fertig! {count} Berichte generiert.")
