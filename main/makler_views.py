# -*- coding: utf-8 -*-
"""
Makler-Portal: Dashboard für Immobilienmakler & Bauunternehmen
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db.models import Count, Q
from listings.models import Listing
from .professional_models import Professional
import json


def get_makler_professional(user):
    """Holt das Professional-Profil des eingeloggten Users"""
    try:
        return Professional.objects.get(user=user, is_active=True)
    except Professional.DoesNotExist:
        return None


@login_required
def makler_dashboard(request):
    """Hauptseite des Makler-Dashboards"""
    professional = get_makler_professional(request.user)
    
    if not professional:
        messages.error(request, 'Kein Zugang zum Makler-Portal. / Nemate pristup portalu.')
        return redirect('main:home')
    
    lang = request.session.get('site_language', 'ge')
    
    listings = Listing.objects.filter(
        Q(oib_number=professional.oib_number) | Q(email=professional.email)
    ).order_by('-list_date')
    
    stats = {
        'total': listings.count(),
        'aktiv': listings.filter(listing_status='aktiv', is_published=True).count(),
        'pruefung': listings.filter(listing_status='pruefung').count(),
        'verkauft': listings.filter(listing_status='verkauft').count(),
        'pausiert': listings.filter(listing_status='pausiert').count(),
    }
    
    paginator = Paginator(listings, 20)
    page = request.GET.get('page', 1)
    listings_page = paginator.get_page(page)
    
    # Profil-Vollständigkeit berechnen
    profile_fields = [professional.name, professional.email, professional.phone, 
                      professional.city, professional.company_logo, professional.description]
    filled = sum(1 for f in profile_fields if f)
    profile_complete = int((filled / len(profile_fields)) * 100)
    
    return render(request, 'makler_portal/dashboard_neu.html', {
        'professional': professional,
        'agent': professional,
        'listings': listings_page,
        'stats': stats,
        'lang': lang,
        'profile_complete': profile_complete,
    })


@login_required

@login_required
def makler_anleitung(request):
    """Anleitung fuer das Makler-Portal"""
    professional = get_makler_professional(request.user)
    if not professional:
        return redirect("main:home")
    lang = request.GET.get("lang", request.session.get("site_language", "ge"))
    return render(request, "makler_portal/anleitung.html", {"professional": professional, "lang": lang})


def makler_objekt_neu(request):
    """Neues Objekt anlegen"""
    professional = get_makler_professional(request.user)
    if not professional:
        return redirect('main:home')
    
    lang = request.session.get('site_language', 'ge')
    
    if request.method == 'POST':
        try:
            listing = Listing(
                property_title=request.POST.get('property_title', ''),
                property_description=request.POST.get('property_description', ''),
                property_type=request.POST.get('property_type', ''),
                property_status=request.POST.get('property_status', 'Sale'),
                property_price=int(request.POST.get('property_price', 0) or 0),
                location=request.POST.get('location', ''),
                city=request.POST.get('city', ''),
                address=request.POST.get('address', ''),
                zipcode=request.POST.get('zipcode', ''),
                country='Kroatien',
                bedrooms=int(request.POST.get('bedrooms', 0) or 0),
                bathrooms=int(request.POST.get('bathrooms', 0) or 0),
                area=int(request.POST.get('area', 0) or 0),
                size=float(request.POST.get('size', 0) or 0),
                floors=int(request.POST.get('floors', 1) or 1),
                garage=int(request.POST.get('garage', 0) or 0),
                oib_number=professional.oib_number,
                email=professional.email,
                company_name=professional.company_name or professional.name,
                listing_status='pruefung',
                is_published=False,
            )
            
            if 'photo_main' in request.FILES:
                listing.photo_main = request.FILES['photo_main']
            listing.photo_main_caption = request.POST.get('photo_main_caption', '')
            
            for i in range(1, 7):
                if f'photo_{i}' in request.FILES:
                    setattr(listing, f'photo_{i}', request.FILES[f'photo_{i}'])
                setattr(listing, f'photo_{i}_caption', request.POST.get(f'photo_{i}_caption', ''))
            
            listing.save()
            
            if lang == 'hr':
                messages.success(request, f'Nekretnina "{listing.property_title}" je spremljena.')
            else:
                messages.success(request, f'Immobilie "{listing.property_title}" wurde gespeichert.')
            
            return redirect('main:makler_dashboard')
            
        except Exception as e:
            messages.error(request, f'Fehler: {str(e)}')
    
    return render(request, 'makler_portal/objekt_form.html', {
        'professional': professional,
        'lang': lang,
        'is_new': True,
    })


@login_required
def makler_objekt_bearbeiten(request, listing_id):
    """Bestehendes Objekt bearbeiten"""
    professional = get_makler_professional(request.user)
    if not professional:
        return redirect('main:home')
    
    lang = request.session.get('site_language', 'ge')
    
    listing = get_object_or_404(
        Listing,
        Q(id=listing_id) & (Q(oib_number=professional.oib_number) | Q(email=professional.email))
    )
    
    if request.method == 'POST':
        try:
            listing.property_title = request.POST.get('property_title', listing.property_title)
            listing.property_description = request.POST.get('property_description', listing.property_description)
            listing.property_type = request.POST.get('property_type', listing.property_type)
            listing.property_status = request.POST.get('property_status', listing.property_status)
            listing.property_price = int(request.POST.get('property_price', 0) or listing.property_price)
            listing.location = request.POST.get('location', listing.location)
            listing.city = request.POST.get('city', listing.city)
            listing.address = request.POST.get('address', listing.address)
            listing.zipcode = request.POST.get('zipcode', listing.zipcode)
            listing.bedrooms = int(request.POST.get('bedrooms', 0) or listing.bedrooms)
            listing.bathrooms = int(request.POST.get('bathrooms', 0) or listing.bathrooms)
            listing.area = int(request.POST.get('area', 0) or listing.area)
            listing.size = float(request.POST.get('size', 0) or listing.size)
            listing.floors = int(request.POST.get('floors', 1) or listing.floors)
            listing.garage = int(request.POST.get('garage', 0) or listing.garage)
            
            if 'photo_main' in request.FILES:
                listing.photo_main = request.FILES['photo_main']
            listing.photo_main_caption = request.POST.get('photo_main_caption', '')
            
            for i in range(1, 7):
                if f'photo_{i}' in request.FILES:
                    setattr(listing, f'photo_{i}', request.FILES[f'photo_{i}'])
                setattr(listing, f'photo_{i}_caption', request.POST.get(f'photo_{i}_caption', ''))
            
            if listing.listing_status == 'aktiv':
                listing.listing_status = 'pruefung'
                listing.is_published = False
            
            listing.save()
            
            if lang == 'hr':
                messages.success(request, 'Promjene su spremljene.')
            else:
                messages.success(request, 'Aenderungen wurden gespeichert.')
            
            return redirect('main:makler_dashboard')
            
        except Exception as e:
            messages.error(request, f'Fehler: {str(e)}')
    
    return render(request, 'makler_portal/objekt_form.html', {
        'professional': professional,
        'listing': listing,
        'lang': lang,
        'is_new': False,
    })


@login_required
@require_POST
def makler_objekt_verkauft(request, listing_id):
    professional = get_makler_professional(request.user)
    if not professional:
        return JsonResponse({'error': 'Kein Zugang'}, status=403)
    
    listing = get_object_or_404(
        Listing,
        Q(id=listing_id) & (Q(oib_number=professional.oib_number) | Q(email=professional.email))
    )
    
    listing.listing_status = 'verkauft'
    listing.is_published = False
    listing.save()
    
    return JsonResponse({'success': True})


@login_required
@require_POST
def makler_objekt_pausieren(request, listing_id):
    professional = get_makler_professional(request.user)
    if not professional:
        return JsonResponse({'error': 'Kein Zugang'}, status=403)
    
    listing = get_object_or_404(
        Listing,
        Q(id=listing_id) & (Q(oib_number=professional.oib_number) | Q(email=professional.email))
    )
    
    listing.listing_status = 'pausiert'
    listing.is_published = False
    listing.save()
    
    return JsonResponse({'success': True})


@login_required
@require_POST
def makler_objekt_aktivieren(request, listing_id):
    professional = get_makler_professional(request.user)
    if not professional:
        return JsonResponse({'error': 'Kein Zugang'}, status=403)
    
    listing = get_object_or_404(
        Listing,
        Q(id=listing_id) & (Q(oib_number=professional.oib_number) | Q(email=professional.email))
    )
    
    listing.listing_status = 'pruefung'
    listing.is_published = False
    listing.save()
    
    return JsonResponse({'success': True})


import xml.etree.ElementTree as ET
from django.core.files.base import ContentFile
import requests

@login_required
def makler_xml_import(request):
    professional = get_makler_professional(request.user)
    if not professional:
        return redirect('main:home')
    
    lang = request.session.get('site_language', 'ge')
    results = None
    
    if request.method == 'POST' and 'xml_file' in request.FILES:
        xml_file = request.FILES['xml_file']
        
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            results = {'total': 0, 'success': 0, 'errors': [], 'imported': []}
            
            immobilien = root.findall('.//immobilie')
            if not immobilien:
                immobilien = root.findall('.//nekretnina')
            if not immobilien:
                immobilien = root.findall('.//property')
            if not immobilien:
                immobilien = root.findall('.//listing')
            
            for immo in immobilien:
                results['total'] += 1
                try:
                    listing_data = extract_listing_data(immo)
                    listing = Listing(
                        property_title=listing_data.get('title', 'Ohne Titel'),
                        property_description=listing_data.get('description', ''),
                        property_type=listing_data.get('type', 'House'),
                        property_status=listing_data.get('status', 'Sale'),
                        property_price=int(listing_data.get('price', 0) or 0),
                        location=listing_data.get('location', ''),
                        city=listing_data.get('city', ''),
                        address=listing_data.get('address', ''),
                        zipcode=listing_data.get('zipcode', ''),
                        country='Kroatien',
                        bedrooms=int(listing_data.get('bedrooms', 0) or 0),
                        bathrooms=int(listing_data.get('bathrooms', 0) or 0),
                        area=int(listing_data.get('area', 0) or 0),
                        size=float(listing_data.get('size', 0) or 0),
                        floors=int(listing_data.get('floors', 1) or 1),
                        garage=int(listing_data.get('garage', 0) or 0),
                        oib_number=professional.oib_number,
                        email=professional.email,
                        company_name=professional.company_name or professional.name,
                        listing_status='pruefung',
                        is_published=False,
                    )
                    listing.save()
                    results['success'] += 1
                    results['imported'].append({'title': listing.property_title, 'id': listing.id})
                except Exception as e:
                    results['errors'].append(f"Objekt {results['total']}: {str(e)}")
            
            messages.success(request, f"{results['success']} von {results['total']} Objekten importiert.")
                
        except ET.ParseError as e:
            messages.error(request, f"XML-Fehler: {str(e)}")
        except Exception as e:
            messages.error(request, f"Fehler: {str(e)}")
    
    return render(request, 'makler_portal/xml_import.html', {
        'professional': professional,
        'lang': lang,
        'results': results,
    })


def extract_listing_data(element):
    data = {}
    
    for tag in ['objekttitel', 'naslov', 'title', 'name', 'property_title']:
        el = element.find(f'.//{tag}')
        if el is not None and el.text:
            data['title'] = el.text.strip()
            break
    
    for tag in ['objektbeschreibung', 'opis', 'description', 'property_description']:
        el = element.find(f'.//{tag}')
        if el is not None and el.text:
            data['description'] = el.text.strip()
            break
    
    for tag in ['kaufpreis', 'cijena', 'price', 'property_price']:
        el = element.find(f'.//{tag}')
        if el is not None:
            try:
                price_text = el.text or el.get('value', '0')
                data['price'] = int(float(price_text.replace('.', '').replace(',', '.').replace(' ', '')))
            except:
                data['price'] = 0
            break
    
    for tag in ['objektart', 'tip', 'type', 'property_type']:
        el = element.find(f'.//{tag}')
        if el is not None:
            typ = el.text or ''
            type_map = {
                'kuca': 'House', 'haus': 'House', 'house': 'House',
                'stan': 'Appartment', 'wohnung': 'Appartment', 'apartment': 'Appartment',
                'vila': 'Villa', 'villa': 'Villa',
                'zemljiste': 'Property', 'grundstueck': 'Property', 'land': 'Property',
                'novogradnja': 'New Building', 'neubau': 'New Building',
            }
            data['type'] = type_map.get(typ.lower(), typ)
            break
    
    for tag in ['ort', 'grad', 'city']:
        el = element.find(f'.//{tag}')
        if el is not None and el.text:
            data['city'] = el.text.strip()
            break
    
    for tag in ['region', 'lokacija', 'location', 'zupanija']:
        el = element.find(f'.//{tag}')
        if el is not None and el.text:
            data['location'] = el.text.strip()
            break
    
    return data


@login_required
@require_POST
def makler_ki_beschreibung(request):
    from .listing_description_ai import generate_listing_description
    
    professional = get_makler_professional(request.user)
    if not professional:
        return JsonResponse({'error': 'Kein Zugang'}, status=403)
    
    try:
        data = json.loads(request.body)
        lang = request.session.get('site_language', 'ge')
        
        listing_data = {
            'typ': data.get('typ', 'Immobilie'),
            'preis': int(data.get('preis', 0) or 0),
            'ort': data.get('ort', ''),
            'region': data.get('region', ''),
            'wohnflaeche': float(data.get('wohnflaeche', 0) or 0),
            'grundstueck': int(data.get('grundstueck', 0) or 0),
            'schlafzimmer': int(data.get('schlafzimmer', 0) or 0),
            'badezimmer': int(data.get('badezimmer', 0) or 0),
            'etagen': int(data.get('etagen', 1) or 1),
            'garage': int(data.get('garage', 0) or 0),
            'extras': data.get('extras', ''),
        }
        
        beschreibung = generate_listing_description(listing_data, lang)
        
        if beschreibung:
            return JsonResponse({'success': True, 'beschreibung': beschreibung})
        else:
            return JsonResponse({'error': 'KI konnte keine Beschreibung generieren'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
@require_POST
def makler_ki_beschreibung_listing(request, listing_id):
    from .listing_description_ai import generate_description_from_listing
    
    professional = get_makler_professional(request.user)
    if not professional:
        return JsonResponse({'error': 'Kein Zugang'}, status=403)
    
    listing = get_object_or_404(
        Listing,
        Q(id=listing_id) & (Q(oib_number=professional.oib_number) | Q(email=professional.email))
    )
    
    lang = request.session.get('site_language', 'ge')
    
    try:
        beschreibung = generate_description_from_listing(listing, lang)
        
        if beschreibung:
            listing.property_description = beschreibung
            listing.save()
            return JsonResponse({'success': True, 'beschreibung': beschreibung})
        else:
            return JsonResponse({'error': 'KI konnte keine Beschreibung generieren'}, status=500)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@login_required
def makler_xml_dokumentation(request):
    professional = get_makler_professional(request.user)
    if not professional:
        return redirect('main:home')
    
    lang = request.session.get('site_language', 'ge')
    
    return render(request, 'makler_portal/xml_dokumentation.html', {
        'professional': professional,
        'lang': lang,
    })
