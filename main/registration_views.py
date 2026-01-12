"""
Views für die mehrstufige Professional-Registrierung
"""
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.utils.text import slugify
from datetime import timedelta
import uuid

from .registration_forms import Step1Form, Step2Form, Step3Form, FORM_TRANSLATIONS
from .registration_utils import get_client_ip, check_spam_block, validate_oib
from .professional_models import Professional, ProfessionalContent
from .profile_generator import generate_profile_texts, check_spelling, improve_text, translate_profile, generate_seo_slug

# Sprach-Mapping
COUNTRY_NAMES = {
    'ge': 'kroatien', 'en': 'croatia', 'hr': 'hrvatska', 'fr': 'croatie',
    'nl': 'kroatie', 'pl': 'chorwacja', 'cz': 'chorvatsko', 'sk': 'chorvatsko',
    'ru': 'horvatiya', 'gr': 'kroatia', 'sw': 'kroatien', 'no': 'kroatia',
}


def get_session_lang(request):
    """Holt die aktuelle Sprache aus der Session"""
    return request.session.get('site_language', 'ge')


def registration_step1(request, country):
    """Schritt 1: Basisdaten"""
    lang = get_session_lang(request)
    trans = FORM_TRANSLATIONS.get(lang, FORM_TRANSLATIONS['ge'])
    
    # Spam-Check
    ip = get_client_ip(request)
    is_blocked, remaining = check_spam_block(ip, Professional)
    if is_blocked:
        return render(request, 'main/registration/blocked.html', {
            'remaining_minutes': remaining,
            'lang': lang,
            'trans': trans,
        })
    
    if request.method == 'POST':
        form = Step1Form(request.POST, request.FILES, lang=lang)
        if form.is_valid():
            # Daten in Session speichern
            request.session['reg_step1'] = {
                'professional_type': form.cleaned_data['professional_type'],
                'name': form.cleaned_data['name'],
                'company_name': form.cleaned_data.get('company_name', ''),
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone'],
                'city': form.cleaned_data['city'],
                'region': form.cleaned_data['region'],
                'service_regions': ','.join(form.cleaned_data.get('service_regions', [])),
                'languages_spoken': form.cleaned_data['languages_spoken'],
                'website': form.cleaned_data.get('website', ''),
                'oib_number': form.cleaned_data['oib_number'],
                'registration_number': form.cleaned_data.get('registration_number', ''),
            }
            
            # Bilder separat speichern (falls vorhanden)
            if 'logo' in request.FILES:
                request.session['reg_has_logo'] = True
            if 'portrait' in request.FILES:
                request.session['reg_has_portrait'] = True
            
            # Weiter zu Schritt 2
            country_name = COUNTRY_NAMES.get(lang, 'kroatien')
            return redirect(f'/{country_name}/professional-registrierung-schritt2/')
    else:
        form = Step1Form(lang=lang)
    
    return render(request, 'main/registration/step1.html', {
        'form': form,
        'step': 1,
        'total_steps': 3,
        'lang': lang,
        'trans': trans,
        'country_name': COUNTRY_NAMES.get(lang, 'kroatien'),
    })


def registration_step2(request, country):
    """Schritt 2: Profiltext wählen oder schreiben"""
    lang = get_session_lang(request)
    trans = FORM_TRANSLATIONS.get(lang, FORM_TRANSLATIONS['ge'])
    
    # Prüfen ob Schritt 1 abgeschlossen
    step1_data = request.session.get('reg_step1')
    if not step1_data:
        country_name = COUNTRY_NAMES.get(lang, 'kroatien')
        return redirect(f'/{country_name}/professional-registrierung/')
    
    # KI-Vorschläge generieren (nur beim ersten Laden)
    if 'reg_suggestions' not in request.session:
        suggestions = generate_profile_texts(step1_data, lang)
        request.session['reg_suggestions'] = suggestions
    else:
        suggestions = request.session['reg_suggestions']
    
    if request.method == 'POST':
        form = Step2Form(request.POST, lang=lang)
        if form.is_valid():
            choice = form.cleaned_data['text_choice']
            
            if choice == 'own':
                selected_text = form.cleaned_data['own_text']
                style = 'own'
            else:
                # KI-Vorschlag gewählt (ki_1 bis ki_8)
                style_key = list(suggestions.keys())[int(choice.split('_')[1]) - 1]
                selected_text = suggestions[style_key]['text']
                style = style_key
            
            # In Session speichern
            request.session['reg_step2'] = {
                'style': style,
                'text': selected_text,
            }
            
            # Weiter zu Schritt 3
            country_name = COUNTRY_NAMES.get(lang, 'kroatien')
            return redirect(f'/{country_name}/professional-registrierung-schritt3/')
    else:
        form = Step2Form(lang=lang)
    
    return render(request, 'main/registration/step2.html', {
        'form': form,
        'suggestions': suggestions,
        'step': 2,
        'total_steps': 3,
        'lang': lang,
        'trans': trans,
        'country_name': COUNTRY_NAMES.get(lang, 'kroatien'),
        'step1_data': step1_data,
    })


def registration_step3(request, country):
    """Schritt 3: Dokumente hochladen und Bestätigung"""
    lang = get_session_lang(request)
    trans = FORM_TRANSLATIONS.get(lang, FORM_TRANSLATIONS['ge'])
    
    # Prüfen ob Schritt 1 & 2 abgeschlossen
    step1_data = request.session.get('reg_step1')
    step2_data = request.session.get('reg_step2')
    
    if not step1_data or not step2_data:
        country_name = COUNTRY_NAMES.get(lang, 'kroatien')
        return redirect(f'/{country_name}/professional-registrierung/')
    
    if request.method == 'POST':
        form = Step3Form(
            request.POST, 
            request.FILES, 
            lang=lang,
            professional_type=step1_data['professional_type']
        )
        
        if form.is_valid():
            # Professional erstellen
            try:
                # SEO-Slug generieren
                slug = generate_seo_slug(
                    step1_data['name'],
                    step1_data['company_name'],
                    step1_data['city'],
                    step1_data['professional_type']
                )
                
                # Professional-Objekt erstellen
                professional = Professional.objects.create(
                    professional_type=step1_data['professional_type'],
                    name=step1_data['name'],
                    company_name=step1_data['company_name'],
                    email=step1_data['email'],
                    phone=step1_data['phone'],
                    city=step1_data['city'],
                    region=step1_data['region'],
                    service_regions=step1_data['service_regions'],
                    languages_spoken=step1_data['languages_spoken'],
                    website=step1_data['website'],
                    oib_number=step1_data['oib_number'],
                    registration_number=step1_data['registration_number'],
                    slug=slug,
                    profile_text_style=step2_data['style'],
                    profile_text_original=step2_data['text'],
                    registration_ip=get_client_ip(request),
                    is_active=False,
                    is_verified=False,
                )
                
                # Dokumente speichern
                if 'id_document' in request.FILES:
                    professional.id_document = request.FILES['id_document']
                if 'business_document' in request.FILES:
                    professional.business_document = request.FILES['business_document']
                professional.save()
                
                # Übersetzungen generieren
                all_languages = ['ge', 'en', 'hr', 'fr', 'nl', 'pl', 'cz', 'sk', 'ru', 'gr', 'sw', 'no']
                translations = translate_profile(step2_data['text'], all_languages)
                
                # ProfessionalContent für jede Sprache erstellen
                for target_lang, translated_text in translations.items():
                    ProfessionalContent.objects.create(
                        professional=professional,
                        language=target_lang,
                        profile_summary=translated_text,
                    )
                
                # Session aufräumen
                for key in ['reg_step1', 'reg_step2', 'reg_suggestions', 'reg_has_logo', 'reg_has_portrait']:
                    if key in request.session:
                        del request.session[key]
                
                # Erfolgsseite
                return render(request, 'main/registration/success.html', {
                    'professional': professional,
                    'lang': lang,
                    'trans': trans,
                    'country_name': COUNTRY_NAMES.get(lang, 'kroatien'),
                })
                
            except Exception as e:
                print(f"Registrierung Fehler: {e}")
                form.add_error(None, f"Ein Fehler ist aufgetreten: {str(e)}")
    else:
        form = Step3Form(lang=lang, professional_type=step1_data['professional_type'])
    
    return render(request, 'main/registration/step3.html', {
        'form': form,
        'step': 3,
        'total_steps': 3,
        'lang': lang,
        'trans': trans,
        'country_name': COUNTRY_NAMES.get(lang, 'kroatien'),
        'step1_data': step1_data,
        'step2_data': step2_data,
    })


# =============================================================================
# AJAX ENDPOINTS für Echtzeit-Funktionen
# =============================================================================

@require_POST
def ajax_check_spelling(request):
    """AJAX: Rechtschreibprüfung"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        lang = get_session_lang(request)
        
        result = check_spelling(text, lang)
        return JsonResponse(result)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def ajax_improve_text(request):
    """AJAX: Text verbessern"""
    try:
        data = json.loads(request.body)
        text = data.get('text', '')
        lang = get_session_lang(request)
        
        improved = improve_text(text, lang)
        return JsonResponse({'improved_text': improved})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST
def ajax_regenerate_suggestions(request):
    """AJAX: Neue KI-Vorschläge generieren"""
    try:
        step1_data = request.session.get('reg_step1')
        if not step1_data:
            return JsonResponse({'error': 'Keine Basisdaten gefunden'}, status=400)
        
        lang = get_session_lang(request)
        suggestions = generate_profile_texts(step1_data, lang)
        request.session['reg_suggestions'] = suggestions
        
        return JsonResponse({'suggestions': suggestions})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@require_POST  
def ajax_validate_oib(request):
    """AJAX: OIB-Nummer validieren"""
    try:
        data = json.loads(request.body)
        oib = data.get('oib', '')
        
        is_valid, error = validate_oib(oib)
        return JsonResponse({
            'is_valid': is_valid,
            'error': error
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)
