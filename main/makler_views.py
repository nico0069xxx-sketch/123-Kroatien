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
from listings.validation import validate_listing
from .professional_models import Professional
import json


def get_makler_professional(user):
    """Holt das Professional-Profil des eingeloggten Users"""
    try:
        return Professional.objects.get(user=user, has_portal_access=True)
    except Professional.DoesNotExist:
        return None


@login_required
def makler_dashboard(request):
    """Hauptseite des Makler-Dashboards"""
    professional = get_makler_professional(request.user)
    
    if not professional:
        messages.error(request, 'Kein Zugang zum Makler-Portal. / Nemate pristup portalu.')
        return redirect('main:home')
    
    # Sprache
    lang = request.session.get('site_language', 'ge')
    
    # Objekte des Maklers (nach OIB oder Email)
    listings = Listing.objects.filter(
        Q(oib_number=professional.oib_number) | Q(email=professional.email)
    ).order_by('-list_date')
    
    # Statistiken
    stats = {
        'total': listings.count(),
        'aktiv': listings.filter(listing_status='aktiv', is_published=True).count(),
        'pruefung': listings.filter(listing_status='pruefung').count(),
        'verkauft': listings.filter(listing_status='verkauft').count(),
        'pausiert': listings.filter(listing_status='pausiert').count(),
    }
    
    # Pagination
    paginator = Paginator(listings, 20)
    page = request.GET.get('page', 1)
    listings_page = paginator.get_page(page)
    
    return render(request, 'makler_portal/dashboard.html', {
        'professional': professional,
        'listings': listings_page,
        'stats': stats,
        'lang': lang,
    })


@login_required
def makler_objekt_neu(request):
    """Neues Objekt anlegen"""
    professional = get_makler_professional(request.user)
    if not professional:
        return redirect('main:home')
    
    lang = request.session.get('site_language', 'ge')
    
    if request.method == 'POST':
        # Daten aus Formular
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
                # Makler-Daten
                oib_number=professional.oib_number,
                email=professional.email,
                company_name=professional.company_name or professional.name,
                # Status
                listing_status='pruefung',
                is_published=False,
            )
            
            # Foto hochladen
            if 'photo_main' in request.FILES:
                listing.photo_main = request.FILES['photo_main']
            
            # Weitere Fotos
            for i in range(1, 7):
                if f'photo_{i}' in request.FILES:
                    setattr(listing, f'photo_{i}', request.FILES[f'photo_{i}'])
            
            listing.save()
            
            # Validierung
            fehler = validate_listing(listing)
            if fehler:
                listing.pruefung_fehler = "\n".join(fehler)
                listing.save()
            
            if lang == 'hr':
                messages.success(request, f'Nekretnina "{listing.property_title}" je spremljena i poslana na provjeru.')
            else:
                messages.success(request, f'Immobilie "{listing.property_title}" wurde gespeichert und zur Prüfung eingereicht.')
            
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
    
    # Nur eigene Objekte
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
            
            # Fotos
            if 'photo_main' in request.FILES:
                listing.photo_main = request.FILES['photo_main']
            for i in range(1, 7):
                if f'photo_{i}' in request.FILES:
                    setattr(listing, f'photo_{i}', request.FILES[f'photo_{i}'])
            
            # Wenn bearbeitet, zur erneuten Pruefung
            if listing.listing_status == 'aktiv':
                listing.listing_status = 'pruefung'
                listing.is_published = False
            
            listing.save()
            
            # Validierung
            fehler = validate_listing(listing)
            if fehler:
                listing.pruefung_fehler = "\n".join(fehler)
            else:
                listing.pruefung_fehler = None
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
    """Objekt als verkauft markieren"""
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
    
    return JsonResponse({'success': True, 'message': 'Als verkauft markiert / Označeno kao prodano'})


@login_required
@require_POST
def makler_objekt_pausieren(request, listing_id):
    """Objekt pausieren"""
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
    
    return JsonResponse({'success': True, 'message': 'Pausiert / Pauzirano'})


@login_required
@require_POST
def makler_objekt_aktivieren(request, listing_id):
    """Objekt wieder aktivieren (zur Pruefung)"""
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
    
    return JsonResponse({'success': True, 'message': 'Zur Pruefung eingereicht / Poslano na provjeru'})
