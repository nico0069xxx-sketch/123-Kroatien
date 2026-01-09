"""
AI Content Generator for Agent Profiles
Generates professional descriptions in 12 languages using OpenAI GPT-4o
"""
from emergentintegrations.llm.openai import OpenAILLM

# Emergent LLM Key
EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"

# Language mapping
LANGUAGES = {
    'en': 'English',
    'de': 'German',
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

def generate_agent_description(agent, language_code):
    """
    Generate a professional description for an agent in a specific language.
    Uses synchronous API call.
    """
    language_name = LANGUAGES.get(language_code, 'English')
    
    # Build context from agent data
    agent_info = []
    if agent.first_name or agent.last_name:
        name = f"{agent.first_name or ''} {agent.last_name or ''}".strip()
        agent_info.append(f"Name: {name}")
    if agent.company_name:
        agent_info.append(f"Company: {agent.company_name}")
    if agent.city:
        agent_info.append(f"City: {agent.city}")
    if agent.country:
        agent_info.append(f"Country: {agent.country}")
    if agent.description:
        agent_info.append(f"Original description: {agent.description}")
    
    agent_context = "\n".join(agent_info) if agent_info else "Real estate professional"
    
    prompt = f"""Write a professional, SEO-optimized description for a real estate agent/company profile in {language_name}.

Agent Information:
{agent_context}

Requirements:
- Write 2-3 paragraphs (150-250 words)
- Professional and trustworthy tone
- Include keywords relevant to real estate services
- Highlight expertise and local market knowledge
- Make it engaging and personal
- Write ONLY in {language_name}, no other languages
- Do not include any markdown formatting, just plain text

Return ONLY the description text, nothing else."""

    try:
        llm = OpenAILLM(api_key=EMERGENT_LLM_KEY)
        response = llm.chat_completion(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"You are a professional copywriter specializing in real estate marketing. Write only in {language_name}."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.strip()
    except Exception as e:
        print(f"Error generating {language_name} description: {e}")
        return None


def generate_all_descriptions(agent):
    """
    Generate descriptions in all 12 languages for an agent.
    Returns dict with language_code: description pairs.
    """
    results = {}
    success_count = 0
    
    for lang_code in LANGUAGES.keys():
        print(f"Generating description in {LANGUAGES[lang_code]}...")
        description = generate_agent_description(agent, lang_code)
        if description:
            results[lang_code] = description
            success_count += 1
            print(f"  ✓ {LANGUAGES[lang_code]} done")
        else:
            print(f"  ✗ {LANGUAGES[lang_code]} failed")
    
    return results, success_count
