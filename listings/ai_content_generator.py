"""
AI Content Generator for Property Listings - ON-DEMAND VERSION
Generates SEO-optimized JSON descriptions for single languages on-the-fly
Uses GPT-4o-mini for fast, cost-effective generation
"""
import asyncio
import json
try:
    from emergentintegrations.llm.openai import LlmChat, UserMessage
except ImportError:
    LlmChat = None
    UserMessage = None

EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"

# Language code to field name mapping
LANGUAGE_FIELDS = {
    'en': 'english_content',
    'ge': 'german_content',
    'de': 'german_content',
    'fr': 'french_content',
    'gr': 'greek_content',
    'hr': 'croatian_content',
    'pl': 'polish_content',
    'cz': 'czech_content',
    'ru': 'russian_content',
    'sw': 'swedish_content',
    'nb': 'norway_content',
    'no': 'norway_content',
    'sl': 'slovak_content',
    'sk': 'slovak_content',
    'nl': 'dutch_content',
}

LANGUAGE_NAMES = {
    'en': 'English', 'ge': 'German', 'de': 'German', 'fr': 'French',
    'gr': 'Greek', 'hr': 'Croatian', 'pl': 'Polish', 'cz': 'Czech',
    'ru': 'Russian', 'sw': 'Swedish', 'nb': 'Norwegian', 'no': 'Norwegian',
    'sl': 'Slovak', 'sk': 'Slovak', 'nl': 'Dutch',
}


async def _generate_json_async(listing, language_name, session_id):
    """Generate listing JSON content in a specific language - FAST version."""
    
    prompt = f"""Create a JSON object for a real estate listing in {language_name}.

Original Property Data:
- Title: {listing.property_title or 'Property'}
- Description: {listing.property_description or 'Real estate property'}
- Type: {listing.property_type or 'Property'}
- City: {listing.city or ''}
- Country: {listing.country or 'Croatia'}
- Bedrooms: {listing.bedrooms or 0}
- Bathrooms: {listing.bathrooms or 0}
- Area: {listing.area or 0} sqm
- Price: {listing.property_price or 0} EUR

Generate this exact JSON structure with ALL values translated/written in {language_name}:
{{
    "property_title": "translated attractive title",
    "property_description": "compelling 2-3 paragraph description (150-200 words)",
    "property_type": "translated property type",
    "property_price": {listing.property_price or 0}
}}

Requirements:
- Write property_title, property_description, and property_type in {language_name}
- Make the description engaging and SEO-friendly
- Keep property_price as a number
- Return ONLY valid JSON, no markdown, no explanation"""

    try:
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=f"You are a real estate copywriter. Return only valid JSON. Write text in {language_name}."
        ).with_model("openai", "gpt-4o-mini").with_params(temperature=0.7, max_tokens=600)
        
        response = await llm.send_message(UserMessage(text=prompt))
        
        # Clean up response
        content = response.strip()
        if content.startswith("```"):
            lines = content.split("\n")
            content = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
            if content.startswith("json"):
                content = content[4:].strip()
        
        # Validate JSON
        json.loads(content)
        return content
    except Exception as e:
        print(f"Error generating {language_name}: {e}")
        return None


def get_field_for_language(lang_code):
    """Get the model field name for a language code."""
    return LANGUAGE_FIELDS.get(lang_code, 'english_content')


def has_content_for_language(listing, lang_code):
    """Check if listing has content for the given language."""
    field = get_field_for_language(lang_code)
    content = getattr(listing, field, None)
    return bool(content and content.strip())


def generate_on_demand(listing, lang_code):
    """
    Generate content for a single language ON-DEMAND.
    Fast version using GPT-4o-mini (~3-5 seconds).
    Saves to database and returns the JSON string.
    """
    import uuid
    
    field = get_field_for_language(lang_code)
    lang_name = LANGUAGE_NAMES.get(lang_code, 'English')
    
    print(f"[AI] Generating {lang_name} content for listing {listing.id}...")
    
    session_id = f"listing_{listing.id}_{lang_code}_{uuid.uuid4().hex[:8]}"
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            content = loop.run_until_complete(
                _generate_json_async(listing, lang_name, session_id)
            )
            
            if content:
                # Save to database
                setattr(listing, field, content)
                listing.save(update_fields=[field])
                print(f"[AI] ✓ Generated and saved {lang_name} content")
                return content
        finally:
            loop.close()
    except Exception as e:
        print(f"[AI] ✗ Error generating {lang_name}: {e}")
    
    return None


def get_or_generate_json(listing, lang_code):
    """
    Get existing JSON content or generate on-demand.
    Returns parsed JSON dict or None.
    """
    field = get_field_for_language(lang_code)
    existing_content = getattr(listing, field, None)
    
    # If content exists, parse and return it
    if existing_content and existing_content.strip():
        try:
            return json.loads(existing_content)
        except json.JSONDecodeError:
            print(f"[AI] Invalid JSON in {field}, regenerating...")
    
    # Generate on-demand
    new_content = generate_on_demand(listing, lang_code)
    if new_content:
        try:
            return json.loads(new_content)
        except json.JSONDecodeError:
            pass
    
    # Fallback to original data
    return None


# ============= ADMIN BULK GENERATION =============

def generate_all_listing_content(listing):
    """Generate content in all 12 languages for a listing (batch mode for admin)."""
    import uuid
    success_count = 0
    
    all_languages = {
        'en': ('English', 'english_content'),
        'de': ('German', 'german_content'),
        'fr': ('French', 'french_content'),
        'gr': ('Greek', 'greek_content'),
        'hr': ('Croatian', 'croatian_content'),
        'pl': ('Polish', 'polish_content'),
        'cz': ('Czech', 'czech_content'),
        'ru': ('Russian', 'russian_content'),
        'sw': ('Swedish', 'swedish_content'),
        'no': ('Norwegian', 'norway_content'),
        'sk': ('Slovak', 'slovak_content'),
        'nl': ('Dutch', 'dutch_content'),
    }
    
    for lang_code, (lang_name, field_name) in all_languages.items():
        print(f"Generating {lang_name}...")
        session_id = f"listing_{listing.id}_{lang_code}_{uuid.uuid4().hex[:8]}"
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                content = loop.run_until_complete(
                    _generate_json_async(listing, lang_name, session_id)
                )
                if content:
                    setattr(listing, field_name, content)
                    success_count += 1
                    print(f"  ✓ {lang_name} done")
                else:
                    print(f"  ✗ {lang_name} failed")
            finally:
                loop.close()
        except Exception as e:
            print(f"  ✗ {lang_name} error: {e}")
    
    listing.save()
    return success_count
