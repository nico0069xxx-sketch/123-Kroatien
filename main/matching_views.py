# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt
"""
Views fuer KI-Matching Seite - 12 Sprachen
"""
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json

from .ki_matching import get_professional_matches


# Texte in 12 Sprachen
TEXTE = {
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
        'error_short': 'Bitte beschreiben Sie Ihr Anliegen ausfuehrlicher.',
        'view_profile': 'Profil ansehen',
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
        'error_short': 'Please describe your request in more detail.',
        'view_profile': 'View profile',
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
        'error_short': 'Molimo opisite svoj zahtjev detaljnije.',
        'view_profile': 'Pogledaj profil',
    },
    'fr': {
        'title': 'Recherche d\'experts',
        'subtitle': 'Decrivez votre demande et nous trouverons l\'expert adapte pour vous.',
        'placeholder': 'p.ex. Je cherche une maison en Istrie et j\'ai besoin d\'un avocat pour le contrat d\'achat...',
        'button': 'Trouver des experts',
        'loading': 'Recherche en cours...',
        'no_results': 'Desole, aucun expert correspondant trouve.',
        'results_title': 'Experts correspondants',
        'contact': 'Contacter',
        'website': 'Site web',
        'error_short': 'Veuillez decrire votre demande plus en detail.',
        'view_profile': 'Voir le profil',
    },
    'nl': {
        'title': 'Expert zoeken',
        'subtitle': 'Beschrijf uw vraag en wij vinden de juiste expert voor u.',
        'placeholder': 'bijv. Ik zoek een huis in Istrie en heb een advocaat nodig voor het koopcontract...',
        'button': 'Experts vinden',
        'loading': 'Zoeken...',
        'no_results': 'Helaas geen passende experts gevonden.',
        'results_title': 'Passende experts',
        'contact': 'Contact',
        'website': 'Website',
        'error_short': 'Beschrijf uw vraag uitgebreider.',
        'view_profile': 'Bekijk profiel',
    },
    'pl': {
        'title': 'Wyszukiwarka ekspertow',
        'subtitle': 'Opisz swoja potrzebe, a my znajdziemy odpowiedniego eksperta.',
        'placeholder': 'np. Szukam domu w Istrii i potrzebuje prawnika do umowy kupna...',
        'button': 'Znajdz ekspertow',
        'loading': 'Szukanie...',
        'no_results': 'Niestety nie znaleziono pasujacych ekspertow.',
        'results_title': 'Pasujacy eksperci',
        'contact': 'Kontakt',
        'website': 'Strona www',
        'error_short': 'Prosze opisac swoja potrzebe bardziej szczegolowo.',
        'view_profile': 'Zobacz profil',
    },
    'cz': {
        'title': 'Vyhledavac expertu',
        'subtitle': 'Popiste svuj pozadavek a my najdeme spravneho experta.',
        'placeholder': 'napr. Hledam dum v Istrii a potrebuji pravnika na kupni smlouvu...',
        'button': 'Najit experty',
        'loading': 'Hledani...',
        'no_results': 'Bohuzel nebyli nalezeni zadni odpovidajici experti.',
        'results_title': 'Odpovidajici experti',
        'contact': 'Kontaktovat',
        'website': 'Webova stranka',
        'error_short': 'Popiste prosim svuj pozadavek podrobneji.',
        'view_profile': 'Zobrazit profil',
    },
    'sk': {
        'title': 'Vyhladavac expertov',
        'subtitle': 'Popiste svoju poziadavku a my najdeme spravneho experta.',
        'placeholder': 'napr. Hladam dom v Istrii a potrebujem pravnika na kupnu zmluvu...',
        'button': 'Najst expertov',
        'loading': 'Hladanie...',
        'no_results': 'Zial neboli najdeni ziadni odpovedajuci experti.',
        'results_title': 'Odpovedajuci experti',
        'contact': 'Kontaktovat',
        'website': 'Webova stranka',
        'error_short': 'Popiste prosim svoju poziadavku podrobnejsie.',
        'view_profile': 'Zobrazit profil',
    },
    'ru': {
        'title': 'Poisk ekspertov',
        'subtitle': 'Opishite vash zapros i my najdem podhodjashego eksperta.',
        'placeholder': 'napr. Ja ishhu dom v Istrii i mne nuzhen advokat dlja dogovora kupli-prodazhi...',
        'button': 'Najti ekspertov',
        'loading': 'Poisk...',
        'no_results': 'K sozhaleniju, podhodyashie eksperty ne najdeny.',
        'results_title': 'Podhodyashie eksperty',
        'contact': 'Svjazatsja',
        'website': 'Sajt',
        'error_short': 'Pozhalujsta, opishite vash zapros podrobnee.',
        'view_profile': 'Posmotret profil',
    },
    'gr': {
        'title': 'Anazhthsh eidikwn',
        'subtitle': 'Perigrapste to aithma sas kai tha vroume ton katallhlo eidiko.',
        'placeholder': 'p.x. Psaxnw spiti sthn Istria kai xreiazomai dikigoro gia to symvolaio agoras...',
        'button': 'Vreste eidikous',
        'loading': 'Anazhthsh...',
        'no_results': 'Dystitxws den vrethikan katallhloi eidikoi.',
        'results_title': 'Katallhloi eidikoi',
        'contact': 'Epikoinwnia',
        'website': 'Istoselida',
        'error_short': 'Parakalw perigrapste to aithma sas pio analytika.',
        'view_profile': 'Provoli profil',
    },
    'sw': {
        'title': 'Expertsokare',
        'subtitle': 'Beskriv ditt arende och vi hittar ratt expert at dig.',
        'placeholder': 't.ex. Jag soker ett hus i Istrien och behover en advokat for kopekontraktet...',
        'button': 'Hitta experter',
        'loading': 'Soker...',
        'no_results': 'Tyvarr hittades inga matchande experter.',
        'results_title': 'Matchande experter',
        'contact': 'Kontakta',
        'website': 'Webbplats',
        'error_short': 'Beskriv ditt arende mer utforligt.',
        'view_profile': 'Visa profil',
    },
    'no': {
        'title': 'Ekspertsoker',
        'subtitle': 'Beskriv ditt behov og vi finner riktig ekspert for deg.',
        'placeholder': 'f.eks. Jeg soker et hus i Istria og trenger en advokat for kjopekontrakten...',
        'button': 'Finn eksperter',
        'loading': 'Soker...',
        'no_results': 'Beklager, ingen matchende eksperter funnet.',
        'results_title': 'Matchende eksperter',
        'contact': 'Kontakt',
        'website': 'Nettsted',
        'error_short': 'Vennligst beskriv ditt behov mer detaljert.',
        'view_profile': 'Se profil',
    },
}


def matching_page(request):
    """KI-Matching Seite"""
    lang = request.session.get('site_language', 'ge')
    
    return render(request, 'main/matching.html', {
        'lang': lang,
        'texte': TEXTE.get(lang, TEXTE['ge']),
    })


@require_POST
@csrf_exempt
def matching_api(request):
    """API-Endpoint fuer KI-Matching"""
    try:
        data = json.loads(request.body)
        anfrage = data.get('anfrage', '')
        lang = request.session.get('site_language', 'ge')
        texte = TEXTE.get(lang, TEXTE['ge'])
        
        if not anfrage or len(anfrage) < 10:
            return JsonResponse({
                'success': False,
                'error': texte['error_short']
            })
        
        result = get_professional_matches(anfrage, lang)
        
        return JsonResponse(result)
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
