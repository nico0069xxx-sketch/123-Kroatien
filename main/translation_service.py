import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

LANGUAGES = {
    'german_content': 'Deutsch',
    'english_content': 'Englisch', 
    'french_content': 'Französisch',
    'greek_content': 'Griechisch',
    'croatian_content': 'Kroatisch',
    'polish_content': 'Polnisch',
    'czech_content': 'Tschechisch',
    'russian_content': 'Russisch',
    'swedish_content': 'Schwedisch',
    'norway_content': 'Norwegisch',
    'slovak_content': 'Slowakisch',
    'dutch_content': 'Niederländisch',
}

def translate_text(text, target_language):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Übersetze ins {target_language}. Nur die Übersetzung, nichts anderes."},
                {"role": "user", "content": text}
            ],
            max_tokens=500,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Fehler: {e}")
        return None

def translate_listing_to_all_languages(listing, source_text):
    import json
    results = {}
    
    for field_name, language_name in LANGUAGES.items():
        print(f"Übersetze nach {language_name}...")
        
        # Titel UND Beschreibung übersetzen
        translated_title = translate_text(listing.property_title, language_name)
        translated_desc = translate_text(source_text, language_name)
        
        if translated_title and translated_desc:
            json_content = json.dumps({
                "property_title": translated_title,
                "property_description": translated_desc,
                "property_type": listing.property_type,
                "property_status": listing.property_status,
                "address": listing.address,
                "bathrooms": listing.bathrooms,
                "bedrooms": listing.bedrooms,
                "floors": listing.floors,
                "area": listing.area,
                "property_price": listing.property_price
            })
            setattr(listing, field_name, json_content)
            results[language_name] = "✅"
        else:
            results[language_name] = "❌"
    
    listing.save()
    return results
