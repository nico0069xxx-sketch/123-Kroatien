"""
Views für das Professional Portal - Gruppe B (Architekten, Anwälte, Steuerberater)
Diese Gruppe verwaltet keine Immobilien, sondern nur ihr Profil.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from main.professional_models import Professional


# Gruppe B: Architekten, Anwälte, Steuerberater (kein Immobilien-Management)
GRUPPE_B_TYPES = ['lawyer', 'tax_advisor', 'architect']


def is_gruppe_b(professional):
    """Prüft ob ein Professional zur Gruppe B gehört"""
    return professional.professional_type in GRUPPE_B_TYPES


@login_required(login_url='account:login')
def dashboard_gruppe_b(request):
    """Dashboard für Gruppe B Professionals"""
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        messages.error(request, 'Kein Professional-Profil gefunden.')
        return redirect('main:home')
    
    # Prüfe ob User zur Gruppe B gehört
    if not is_gruppe_b(professional):
        # Weiterleitung zum Makler-Portal für Gruppe A
        return redirect('main:home')  # TODO: Update to Makler-Portal URL
    
    context = {
        'professional': professional,
    }
    return render(request, 'professional_portal/dashboard_gruppe_b.html', context)


@login_required(login_url='account:login')
def edit_profile(request):
    """Profil bearbeiten für Gruppe B"""
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        messages.error(request, 'Kein Professional-Profil gefunden.')
        return redirect('main:home')
    
    if request.method == 'POST':
        # Grunddaten
        professional.name = request.POST.get('name', professional.name)
        professional.email = request.POST.get('email', professional.email)
        professional.phone = request.POST.get('phone', '')
        professional.mobile = request.POST.get('mobile', '')
        professional.website = request.POST.get('website', '')
        
        # Adresse
        professional.city = request.POST.get('city', '')
        professional.address = request.POST.get('address', '')
        professional.region = request.POST.get('region', '')
        
        # Beschreibung
        professional.description_de = request.POST.get('description_de', '')
        professional.description_hr = request.POST.get('description_hr', '')
        
        # Sprachen
        professional.languages = request.POST.get('languages', '')
        
        # Social Media
        professional.facebook = request.POST.get('facebook', '')
        professional.instagram = request.POST.get('instagram', '')
        professional.linkedin = request.POST.get('linkedin', '')
        
        # Bilder
        if 'profile_image' in request.FILES:
            professional.profile_image = request.FILES['profile_image']
        if 'company_logo' in request.FILES:
            professional.company_logo = request.FILES['company_logo']
        
        professional.save()
        messages.success(request, 'Profil erfolgreich aktualisiert!')
        return redirect('professional_portal:dashboard')
    
    context = {
        'professional': professional,
        'regions': Professional.REGIONS,
    }
    return render(request, 'professional_portal/edit_profile.html', context)


@login_required(login_url='account:login')
def change_password(request):
    """Passwort ändern"""
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        professional = None
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Passwort erfolgreich geändert!')
            return redirect('professional_portal:dashboard')
        else:
            for error in form.errors.values():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'professional': professional,
    }
    return render(request, 'professional_portal/change_password.html', context)


@login_required(login_url='account:login')
def setup_2fa(request):
    """2FA Einstellungen verwalten"""
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        messages.error(request, 'Kein Professional-Profil gefunden.')
        return redirect('main:home')
    
    context = {
        'professional': professional,
    }
    return render(request, 'professional_portal/setup_2fa.html', context)
