"""
AI Content Generator for Property Listings
Generates SEO-optimized descriptions in 12 languages using OpenAI GPT-4o
"""
import asyncio
import json
from emergentintegrations.llm.openai import LlmChat, UserMessage

EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"

# Language code to field name mapping
LANGUAGE_FIELDS = {
    'en': 'english_content',
    'ge': 'german_content',
    'de': 'german_content',  # alias
    'fr': 'french_content',
    'gr': 'greek_content',
    'hr': 'croatian_content',
    'pl': 'polish_content',
    'cz': 'czech_content',
    'ru': 'russian_content',
    'sw': 'swedish_content',
    'nb': 'norway_content',
    'no': 'norway_content',  # alias
    'sl': 'slovak_content',
    'sk': 'slovak_content',  # alias
    'nl': 'dutch_content',
}

LANGUAGE_NAMES = {
    'en': 'English',
    'ge': 'German',
    'de': 'German',
    'fr': 'French',
    'gr': 'Greek',
    'hr': 'Croatian',
    'pl': 'Polish',
    'cz': 'Czech',
    'ru': 'Russian',
    'sw': 'Swedish',
    'nb': 'Norwegian',
    'no': 'Norwegian',
    'sl': 'Slovak',
    'sk': 'Slovak',
    'nl': 'Dutch',
}


async def _generate_single_async(listing_context, language_name, session_id):
    """Generate listing content in a specific language - FAST version."""
    
    prompt = f"""Write a compelling real estate listing description in {language_name}.

Property:
{listing_context}

Write 2-3 paragraphs (100-150 words) that:
- Highlight key features
- Are emotionally engaging
- Use real estate keywords

Write ONLY in {language_name}. Return ONLY the description text, no titles or formatting."""

    try:
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=f"You are a real estate copywriter. Write only in {language_name}."
        ).with_model("openai", "gpt-4o-mini").with_params(temperature=0.7, max_tokens=400)
        
        response = await llm.send_message(UserMessage(text=prompt))
        return response.strip()
    except Exception as e:
        print(f"Error generating {language_name}: {e}")
        return None


def get_content_field(lang_code):
    """Get the model field name for a language code."""
    return LANGUAGE_FIELDS.get(lang_code, 'english_content')


def has_content(listing, lang_code):
    """Check if listing has content for the given language."""
    field = get_content_field(lang_code)
    content = getattr(listing, field, None)
    return bool(content and content.strip())


def get_content(listing, lang_code):
    """Get content for the given language."""
    field = get_content_field(lang_code)
    return getattr(listing, field, None)


def generate_single_language(listing, lang_code):
    """
    Generate content for a single language ON-DEMAND.
    Fast version using GPT-4o-mini (~3-5 seconds).
    Returns the generated content.
    """
    import uuid
    
    field = get_content_field(lang_code)
    lang_name = LANGUAGE_NAMES.get(lang_code, 'English')
    
    # Build context
    context_parts = []
    if listing.property_title:
        context_parts.append(f"Title: {listing.property_title}")
    if listing.property_description:
        context_parts.append(f"Description: {listing.property_description[:500]}")
    if listing.property_type:
        context_parts.append(f"Type: {listing.property_type}")
    if listing.city:
        context_parts.append(f"City: {listing.city}")
    if listing.country:
        context_parts.append(f"Country: {listing.country}")
    if listing.bedrooms:
        context_parts.append(f"Bedrooms: {listing.bedrooms}")
    if listing.bathrooms:
        context_parts.append(f"Bathrooms: {listing.bathrooms}")
    if listing.area:
        context_parts.append(f"Area: {listing.area} sqm")
    if listing.property_price:
        context_parts.append(f"Price: €{listing.property_price:,}")
    
    listing_context = "\n".join(context_parts)
    session_id = f"listing_{listing.id}_{lang_code}_{uuid.uuid4().hex[:8]}"
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            content = loop.run_until_complete(
                _generate_single_async(listing_context, lang_name, session_id)
            )
            
            if content:
                # Save to database
                setattr(listing, field, content)
                listing.save(update_fields=[field])
                print(f"✓ Generated {lang_name} for listing {listing.id}")
                return content
        finally:
            loop.close()
    except Exception as e:
        print(f"Error generating {lang_name}: {e}")
    
    return None


def get_or_generate_content(listing, lang_code):
    """
    Get existing content or generate on-demand.
    This is the main function to call from views.
    """
    # Check if content exists
    if has_content(listing, lang_code):
        return get_content(listing, lang_code)
    
    # Generate on-demand
    print(f"Generating on-demand content for listing {listing.id} in {lang_code}...")
    return generate_single_language(listing, lang_code)


# ============= ADMIN BULK GENERATION (for manual batch generation) =============

LANGUAGES_ALL = {
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


async def _generate_listing_content_async(listing_context, language_name, session_id):
    """Generate listing content - FULL version for batch."""
    
    prompt = f"""Write a compelling real estate listing description in {language_name}.

Property:
{listing_context}

Write 2-3 paragraphs (150-200 words) that:
- Highlight the best features
- Are emotionally engaging for buyers
- Include relevant real estate keywords for SEO
- Sound professional and trustworthy

Write ONLY in {language_name}. Return ONLY the description text."""

    try:
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=f"You are a real estate copywriter. Write only in {language_name}."
        ).with_model("openai", "gpt-4o-mini").with_params(temperature=0.7, max_tokens=500)
        
        response = await llm.send_message(UserMessage(text=prompt))
        return response.strip()
    except Exception as e:
        print(f"Error: {e}")
        return None


def generate_all_listing_content(listing):
    """Generate content in all 12 languages for a listing (batch mode)."""
    import uuid
    success_count = 0
    
    # Build context once
    context_parts = []
    if listing.property_title:
        context_parts.append(f"Title: {listing.property_title}")
    if listing.property_description:
        context_parts.append(f"Description: {listing.property_description[:500]}")
    if listing.property_type:
        context_parts.append(f"Type: {listing.property_type}")
    if listing.city:
        context_parts.append(f"City: {listing.city}")
    if listing.country:
        context_parts.append(f"Country: {listing.country}")
    if listing.bedrooms:
        context_parts.append(f"Bedrooms: {listing.bedrooms}")
    if listing.bathrooms:
        context_parts.append(f"Bathrooms: {listing.bathrooms}")
    if listing.area:
        context_parts.append(f"Area: {listing.area} sqm")
    if listing.property_price:
        context_parts.append(f"Price: €{listing.property_price:,}")
    
    listing_context = "\n".join(context_parts)
    
    for lang_code, (lang_name, field_name) in LANGUAGES_ALL.items():
        print(f"Generating {lang_name}...")
        session_id = f"listing_{listing.id}_{lang_code}_{uuid.uuid4().hex[:8]}"
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                content = loop.run_until_complete(
                    _generate_listing_content_async(listing_context, lang_name, session_id)
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
