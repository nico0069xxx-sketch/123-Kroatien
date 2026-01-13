# -*- coding: utf-8 -*-
"""
Views fuer KI-Matching Seite
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

from .ki_matching import get_professional_matches


def matching_page(request):
    """KI-Matching Seite"""
    lang = request.session.get('site_language', 'ge')
    
    # Texte je nach Sprache
    texte = {
        'ge': {
            'title': 'Experten-Finder',
            'subtitle': 'Beschreiben Sie Ihr Anliegen und wir finden den passenden Experten fuer Sie.',
            'placeholder': 'z.B. Ich suche ein Haus in Istrien und brauche einen Anwalt fuer den Kaufvertrag...',
            'button': 'Experten finden',
            'loading': 'Suche laeuft...',
            'no_results': 'Leider keine passenden Experten gefunden.',
            'results_title': 'Passende Experten',
            'contact': 'Kontaktieren',
            'website': 'Webseite',
        },
        'hr': {
            'title': 'Pronalazac strucnjaka',
            'subtitle': 'Opisite svoj zahtjev i mi cemo pronaci pravog strucnjaka za vas.',
            'placeholder': 'npr. Trazim kucu u Istri i trebam odvjetnika za kupoprodajni ugovor...',
            'button': 'Pronadi strucnjake',
            'loading': 'Pretraga u tijeku...',
            'no_results': 'Nazalost, nema odgovarajucih strucnjaka.',
            'results_title': 'Odgovarajuci strucnjaci',
            'contact': 'Kontaktiraj',
            'website': 'Web stranica',
        },
        'en': {
            'title': 'Expert Finder',
            'subtitle': 'Describe your needs and we will find the right expert for you.',
            'placeholder': 'e.g. I am looking for a house in Istria and need a lawyer for the purchase contract...',
            'button': 'Find experts',
            'loading': 'Searching...',
            'no_results': 'Sorry, no matching experts found.',
            'results_title': 'Matching experts',
            'contact': 'Contact',
            'website': 'Website',
        },
    }
    
    return render(request, 'main/matching.html', {
        'lang': lang,
        'texte': texte.get(lang, texte['ge']),
    })


@require_POST
def matching_api(request):
    """API-Endpoint fuer KI-Matching"""
    try:
        data = json.loads(request.body)
        anfrage = data.get('anfrage', '')
        
        if not anfrage or len(anfrage) < 10:
            return JsonResponse({
                'success': False,
                'error': 'Bitte beschreiben Sie Ihr Anliegen ausfuehrlicher.'
            })
        
        lang = request.session.get('site_language', 'ge')
        result = get_professional_matches(anfrage, lang)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
