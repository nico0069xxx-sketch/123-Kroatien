import json
import os
from django.shortcuts import render

def get_lang_text(obj, lang, fallback='de'):
    """Holt Text in der richtigen Sprache"""
    if isinstance(obj, dict):
        return obj.get(lang, obj.get(fallback, obj.get('de', '')))
    return obj

def important_addresses(request, country='kroatien'):
    # Sprache aus Session ermitteln (wie in content_views.py)
    lang = request.session.get('site_language', 'ge')
    
    # Mapping für Sprachcodes
    lang_map = {
        'ge': 'de', 'en': 'en', 'hr': 'hr', 'fr': 'fr',
        'nl': 'nl', 'pl': 'pl', 'cz': 'cz', 'sk': 'sk',
        'ru': 'ru', 'gr': 'gr', 'sw': 'sw', 'no': 'no'
    }
    content_lang = lang_map.get(lang, 'de')
    
    # JSON laden
    json_path = os.path.join(os.path.dirname(__file__), 'important_addresses.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Übersetzungen
    trans = {}
    for key, values in data['translations'].items():
        trans[key] = get_lang_text(values, content_lang)
    
    # Kategorien mit übersetzten Namen
    categories = []
    for cat in data['categories']:
        category = {
            'id': cat['id'],
            'icon': cat['icon'],
            'name': trans.get(f"category_{cat['id']}", cat['id']),
            'addresses': []
        }
        for addr in cat['addresses']:
            address = {
                'name': get_lang_text(addr.get('name', {}), content_lang),
                'address': addr.get('address', ''),
                'phone': addr.get('phone', ''),
                'url': addr.get('url', ''),
                'description': get_lang_text(addr.get('description', {}), content_lang) if addr.get('description') else ''
            }
            category['addresses'].append(address)
        categories.append(category)
    
    # Country name je nach Sprache
    country_names = {
        'ge': 'kroatien', 'en': 'croatia', 'hr': 'hrvatska', 'fr': 'croatie',
        'nl': 'kroatie', 'pl': 'chorwacja', 'cz': 'chorvatsko', 'sk': 'chorvatsko',
        'ru': 'horvatiya', 'gr': 'kroatia', 'sw': 'kroatien', 'no': 'kroatia'
    }
    
    context = {
        'categories': categories,
        'trans': trans,
        'language': lang,
        'country_name': country_names.get(lang, 'kroatien'),
    }
    
    return render(request, 'main/important_addresses.html', context)
