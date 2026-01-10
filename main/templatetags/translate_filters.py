from django import template
from pages.models import Translation
import openai
import os
from dotenv import load_dotenv

load_dotenv()

register = template.Library()

translation_cache = {}

LANG_MAP = {
    'ge': 'German', 'en': 'English', 'hr': 'Croatian', 'fr': 'French',
    'gr': 'Greek', 'pl': 'Polish', 'cz': 'Czech', 'ru': 'Russian',
    'se': 'Swedish', 'sw': 'Swedish', 'no': 'Norwegian', 'sk': 'Slovak', 'nl': 'Dutch'
}

def get_lang(context):
    request = context.get('request')
    if request:
        url_lang = getattr(request, 'LANGUAGE_CODE', None)
        session_lang = request.session.get('site_language', None)
        return url_lang or session_lang or 'ge'
    return 'ge'

def get_translation_content(trans, lang):
    if lang == 'en': return trans.english_content
    elif lang == 'ge': return trans.german_content
    elif lang == 'hr': return trans.croatian_content
    elif lang == 'fr': return trans.french_content
    elif lang == 'gr': return trans.greek_content
    elif lang == 'pl': return trans.polish_content
    elif lang == 'cz': return trans.czech_content
    elif lang == 'ru': return trans.russian_content
    elif lang == 'se' or lang == 'sw': return trans.swedish_content
    elif lang == 'no': return trans.norway_content
    elif lang == 'sk': return trans.slovak_content
    elif lang == 'nl': return trans.dutch_content
    else: return trans.german_content

@register.simple_tag(takes_context=True)
def translate_type(context, value):
    if not value:
        return value
    lang = get_lang(context)
    name = f"type_{value}"
    try:
        trans = Translation.objects.get(name=name)
        return get_translation_content(trans, lang) or value
    except Translation.DoesNotExist:
        return value

@register.simple_tag(takes_context=True)
def translate_status(context, value):
    if not value:
        return value
    lang = get_lang(context)
    name = f"status_{value}"
    try:
        trans = Translation.objects.get(name=name)
        return get_translation_content(trans, lang) or value
    except Translation.DoesNotExist:
        return value

@register.simple_tag(takes_context=True)
def translate_title(context, value):
    if not value:
        return value
    lang = get_lang(context)
    if lang == 'ge':
        return value
    cache_key = f"{value}_{lang}"
    if cache_key in translation_cache:
        return translation_cache[cache_key]
    target_lang = LANG_MAP.get(lang, 'English')
    try:
        api_key = os.environ.get('OPENAI_API_KEY')
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"Translate the following German real estate title to {target_lang}. Only return the translation, nothing else."},
                {"role": "user", "content": value}
            ],
            max_tokens=100
        )
        translated = response.choices[0].message.content.strip()
        translation_cache[cache_key] = translated
        return translated
    except Exception as e:
        print(f"Translation error: {e}")
        return value
