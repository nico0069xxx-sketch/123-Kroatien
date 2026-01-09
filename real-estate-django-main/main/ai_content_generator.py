"""
AI Content Generator for Professional Profiles
Generates professional descriptions in 12 languages using OpenAI GPT-4o
"""
import asyncio
from emergentintegrations.llm.openai import LlmChat, UserMessage

# Emergent LLM Key
EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"

# Language mapping
LANGUAGES = {
    'ge': 'German',
    'en': 'English',
    'fr': 'French',
    'gr': 'Greek',
    'hr': 'Croatian',
    'pl': 'Polish',
    'cz': 'Czech',
    'ru': 'Russian',
    'sw': 'Swedish',
    'no': 'Norwegian',
    'sk': 'Slovak',
    'nl': 'Dutch',
}


async def _generate_content_async(professional_context, language_code, language_name, professional_type, session_id):
    """Internal async function to generate professional content."""
    
    prompt = f"""Generate comprehensive professional profile content in {language_name} for a {professional_type} in Croatia.

Professional Information:
{professional_context}

Generate the following sections:

1. PROFILE_SUMMARY: A professional 2-3 paragraph summary (150-250 words) highlighting expertise, experience, and unique value proposition.

2. AREAS_OF_ACTIVITY: List 5-7 main service areas or specializations as bullet points.

3. TYPICAL_SITUATIONS: Describe 3-4 typical client situations where this professional can help.

4. WORKING_APPROACH: Explain the professional's working method and client approach (1-2 paragraphs).

5. META_TITLE: SEO-optimized page title (max 60 characters).

6. META_DESCRIPTION: SEO-optimized meta description (max 160 characters).

7. VERIFICATION_STATEMENT: A short trust/verification statement about credentials.

Format your response EXACTLY like this:
PROFILE_SUMMARY:
[content here]

AREAS_OF_ACTIVITY:
[content here]

TYPICAL_SITUATIONS:
[content here]

WORKING_APPROACH:
[content here]

META_TITLE:
[content here]

META_DESCRIPTION:
[content here]

VERIFICATION_STATEMENT:
[content here]

Write ALL content in {language_name} only. Be professional, SEO-friendly, and engaging."""

    try:
        system_message = f"You are an expert content writer for professional service providers in the real estate industry in Croatia. Write only in {language_name}."
        
        llm = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=session_id,
            system_message=system_message
        ).with_model("openai", "gpt-4o").with_params(temperature=0.7, max_tokens=1500)
        
        user_msg = UserMessage(text=prompt)
        response = await llm.send_message(user_msg)
        return response.strip()
    except Exception as e:
        print(f"Error generating {language_name} content: {e}")
        return None


def parse_generated_content(response_text):
    """Parse the structured response into a dictionary."""
    sections = {
        'profile_summary': '',
        'areas_of_activity': '',
        'typical_situations': '',
        'working_approach': '',
        'meta_title': '',
        'meta_description': '',
        'verification_statement': '',
    }
    
    if not response_text:
        return sections
    
    current_section = None
    current_content = []
    
    for line in response_text.split('\n'):
        line_upper = line.strip().upper()
        
        if 'PROFILE_SUMMARY' in line_upper and ':' in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'profile_summary'
            current_content = []
        elif 'AREAS_OF_ACTIVITY' in line_upper and ':' in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'areas_of_activity'
            current_content = []
        elif 'TYPICAL_SITUATIONS' in line_upper and ':' in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'typical_situations'
            current_content = []
        elif 'WORKING_APPROACH' in line_upper and ':' in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'working_approach'
            current_content = []
        elif 'META_TITLE' in line_upper and ':' in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'meta_title'
            current_content = []
        elif 'META_DESCRIPTION' in line_upper and ':' in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'meta_description'
            current_content = []
        elif 'VERIFICATION_STATEMENT' in line_upper and ':' in line:
            if current_section:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = 'verification_statement'
            current_content = []
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


def generate_content_for_language(professional, language_code):
    """Generate content for a single language."""
    import uuid
    language_name = LANGUAGES.get(language_code, 'English')
    
    # Build context
    prof_info = []
    prof_info.append(f"Name: {professional.name}")
    prof_info.append(f"Type: {professional.get_professional_type_display()}")
    prof_info.append(f"City: {professional.city}")
    prof_info.append(f"Region: {professional.get_region_display()}")
    
    if professional.company_name:
        prof_info.append(f"Company: {professional.company_name}")
    if professional.website:
        prof_info.append(f"Website: {professional.website}")
    if professional.languages_spoken:
        prof_info.append(f"Languages: {professional.languages_spoken}")
    if professional.service_regions:
        prof_info.append(f"Service Regions: {professional.service_regions}")
    
    # Type-specific info
    if professional.professional_type == 'real_estate_agent' and hasattr(professional, 'agent_profile'):
        profile = professional.agent_profile
        if profile.property_focus:
            prof_info.append(f"Property Focus: {profile.property_focus}")
        if profile.years_active:
            prof_info.append(f"Years Active: {profile.years_active}")
    elif professional.professional_type == 'construction_company' and hasattr(professional, 'construction_profile'):
        profile = professional.construction_profile
        if profile.project_types:
            prof_info.append(f"Project Types: {profile.project_types}")
    elif professional.professional_type == 'lawyer' and hasattr(professional, 'lawyer_profile'):
        profile = professional.lawyer_profile
        if profile.practice_areas:
            prof_info.append(f"Practice Areas: {profile.practice_areas}")
    elif professional.professional_type == 'tax_advisor' and hasattr(professional, 'tax_profile'):
        profile = professional.tax_profile
        if profile.core_services:
            prof_info.append(f"Core Services: {profile.core_services}")
    elif professional.professional_type == 'architect' and hasattr(professional, 'architect_profile'):
        profile = professional.architect_profile
        if profile.planning_focus:
            prof_info.append(f"Planning Focus: {profile.planning_focus}")
    
    professional_context = "\n".join(prof_info)
    session_id = f"prof_{professional.id}_{language_code}_{uuid.uuid4().hex[:8]}"
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(
                _generate_content_async(
                    professional_context,
                    language_code,
                    language_name,
                    professional.get_professional_type_display(),
                    session_id
                )
            )
            return parse_generated_content(result)
        finally:
            loop.close()
    except Exception as e:
        print(f"Error for {language_name}: {e}")
        return None


def generate_content_sync(professional):
    """
    Generate content in all 12 languages for a professional.
    Returns list of results with status for each language.
    This is the main function called from admin.py
    """
    from main.professional_models import ProfessionalContent
    
    results = []
    
    for lang_code, lang_name in LANGUAGES.items():
        print(f"Generating content in {lang_name}...")
        
        try:
            content = generate_content_for_language(professional, lang_code)
            
            if content and content.get('profile_summary'):
                # Create or update ProfessionalContent
                prof_content, created = ProfessionalContent.objects.update_or_create(
                    professional=professional,
                    language=lang_code,
                    defaults={
                        'profile_summary': content.get('profile_summary', ''),
                        'areas_of_activity': content.get('areas_of_activity', ''),
                        'typical_situations': content.get('typical_situations', ''),
                        'working_approach': content.get('working_approach', ''),
                        'meta_title': content.get('meta_title', '')[:200],
                        'meta_description': content.get('meta_description', '')[:300],
                        'verification_statement': content.get('verification_statement', ''),
                    }
                )
                action = "Created" if created else "Updated"
                print(f"  ✓ {lang_name} {action}")
                results.append({'language': lang_code, 'status': 'success'})
            else:
                print(f"  ✗ {lang_name} - no content generated")
                results.append({'language': lang_code, 'status': 'failed'})
        except Exception as e:
            print(f"  ✗ {lang_name} - error: {e}")
            results.append({'language': lang_code, 'status': 'failed', 'error': str(e)})
    
    return results
