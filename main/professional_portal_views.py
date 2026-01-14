from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from main.professional_models import Professional

GRUPPE_B_TYPES = ['lawyer', 'tax_advisor', 'architect']

def is_gruppe_b(professional):
    return professional.professional_type in GRUPPE_B_TYPES

@login_required(login_url='account:login')
def dashboard_gruppe_b(request):
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        messages.error(request, 'Kein Professional-Profil gefunden.')
        return redirect('main:home')
    return render(request, 'professional_portal/dashboard_gruppe_b.html', {'professional': professional})

@login_required(login_url='account:login')
def edit_profile(request):
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        return redirect('main:home')
    if request.method == 'POST':
        professional.name = request.POST.get('name', professional.name)
        professional.email = request.POST.get('email', professional.email)
        professional.phone = request.POST.get('phone', '')
        professional.city = request.POST.get('city', '')
        professional.save()
        messages.success(request, 'Profil aktualisiert!')
        return redirect('professional_portal:dashboard')
    return render(request, 'professional_portal/edit_profile.html', {'professional': professional})

@login_required(login_url='account:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Passwort geaendert!')
            return redirect('professional_portal:dashboard')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'professional_portal/change_password.html', {'form': form})