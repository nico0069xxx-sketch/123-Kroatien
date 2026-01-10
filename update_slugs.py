from openai import OpenAI
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
base_path = "/Users/jorgallmannsberger/Desktop/real-estate-django-ALTmain/main/"

files = {
    "en": "faq_data_en.json",
    "hr": "faq_data_hr.json", 
    "fr": "faq_data_fr.json",
    "gr": "faq_data_gr.json",
    "pl": "faq_data_pl.json",
    "cz": "faq_data_cz.json",
    "ru": "faq_data_ru.json",
    "sw": "faq_data_sw.json",
    "no": "faq_data_no.json",
    "sk": "faq_data_sk.json",
    "nl": "faq_data_nl.json"
}

for lang, filename in files.items():
    filepath = base_path + filename
    with open(filepath, 'r', encoding='utf-8') as f:
        faqs = json.load(f)
    print(f"\n--- {lang.upper()} ({len(faqs)} FAQs) ---")
    for i, faq in enumerate(faqs):
        q = faq['q'][:60]
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Create URL slug (max 50 chars, only a-z 0-9 hyphens, no spaces) for: {q}"}],
            temperature=0.3
        )
        slug = re.sub(r'[^a-z0-9-]', '', response.choices[0].message.content.strip().lower().replace(' ', '-'))[:55]
        faq['slug'] = slug
        if i % 10 == 0:
            print(f"  {i+1}/{len(faqs)}: {slug[:35]}...")
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(faqs, f, ensure_ascii=False, indent=2)
    print(f"  {lang.upper()} FERTIG!")

print("\n=== ALLE SPRACHEN FERTIG! ===")
