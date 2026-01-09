"""
AI Content Generator for Property Listings
Generates SEO-optimized descriptions in 12 languages using OpenAI GPT-4o
"""
import asyncio
import json
from emergentintegrations.llm.openai import LlmChat, UserMessage

EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"

LANGUAGES = {
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
    """Generate listing content in a specific language."""
    
    prompt = f"""Generate an SEO-optimized real estate listing description in {language_name}.

Property Information:
{listing_context}

Create a JSON response with these fields:
- "title": Catchy property title (max 80 chars)
- "description": Engaging property description (150-250 words)
- "highlights": 5-6 key property highlights as a list

Requirements:
- Write in {language_name} ONLY
- Be professional and appealing to buyers
- Include relevant real estate keywords for SEO
- Highlight the best features
- Make it emotionally engaging

Return ONLY valid JSON, no markdown, no explanation."""

    try:
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=f"You are a real estate copywriter. Write only in {language_name}. Return only valid JSON."
        ).with_model("openai", "gpt-4o").with_params(temperature=0.7, max_tokens=800)
        
        response = await llm.send_message(UserMessage(text=prompt))
        return response.strip()
    except Exception as e:
        print(f"Error generating {language_name}: {e}")
        return None


def generate_listing_content(listing, lang_code):
    """Generate content for a single language."""
    import uuid
    
    lang_name, field_name = LANGUAGES.get(lang_code, ('English', 'english_content'))
    
    # Build context
    context_parts = []
    if listing.property_title:
        context_parts.append(f"Original Title: {listing.property_title}")
    if listing.property_description:
        context_parts.append(f"Original Description: {listing.property_description}")
    if listing.property_type:
        context_parts.append(f"Type: {listing.property_type}")
    if listing.property_status:
        context_parts.append(f"Status: {listing.property_status}")
    if listing.city:
        context_parts.append(f"City: {listing.city}")
    if listing.country:
        context_parts.append(f"Country: {listing.country}")
    if listing.location:
        context_parts.append(f"Location: {listing.location}")
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
            result = loop.run_until_complete(
                _generate_listing_content_async(listing_context, lang_name, session_id)
            )
            return result, field_name
        finally:
            loop.close()
    except Exception as e:
        print(f"Error for {lang_name}: {e}")
        return None, field_name


def generate_all_listing_content(listing):
    """Generate content in all 12 languages for a listing."""
    success_count = 0
    
    for lang_code in LANGUAGES.keys():
        lang_name, field_name = LANGUAGES[lang_code]
        print(f"Generating {lang_name}...")
        
        content, field = generate_listing_content(listing, lang_code)
        
        if content:
            # Try to parse as JSON, store as-is if parsing fails
            try:
                # Clean up potential markdown
                clean_content = content
                if clean_content.startswith("```"):
                    clean_content = clean_content.split("```")[1]
                    if clean_content.startswith("json"):
                        clean_content = clean_content[4:]
                
                # Validate it's valid JSON
                json.loads(clean_content)
                setattr(listing, field, clean_content)
            except json.JSONDecodeError:
                # Store raw content if not valid JSON
                setattr(listing, field, content)
            
            success_count += 1
            print(f"  ✓ {lang_name} done")
        else:
            print(f"  ✗ {lang_name} failed")
    
    listing.save()
    return success_count
