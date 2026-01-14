from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from main.professional_models import Professional
import random
import pyotp
import qrcode
import base64
from io import BytesIO

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

@login_required(login_url='account:login')
def twofa_auswahl(request):
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        return redirect('main:home')
    return render(request, 'professional_portal/2fa_auswahl.html', {'professional': professional})

@login_required(login_url='account:login')
def setup_2fa(request):
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        return redirect('main:home')
    if not professional.totp_secret:
        professional.totp_secret = pyotp.random_base32()
        professional.save()
    totp = pyotp.TOTP(professional.totp_secret)
    uri = totp.provisioning_uri(name=professional.email, issuer_name="123-Kroatien")
    qr = qrcode.make(uri)
    buffer = BytesIO()
    qr.save(buffer, format='PNG')
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    if request.method == 'POST':
        code = request.POST.get('otp_code', '')
        if totp.verify(code):
            professional.totp_enabled = True
            professional.totp_verified = True
            professional.must_setup_2fa = False
            professional.save()
            messages.success(request, '2FA erfolgreich eingerichtet!')
            return redirect('professional_portal:dashboard')
        else:
            messages.error(request, 'Falscher Code. Bitte erneut versuchen.')
    return render(request, 'professional_portal/setup_2fa.html', {'professional': professional, 'qr_code': qr_code})

@login_required(login_url='account:login')
def setup_email_2fa(request):
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        return redirect('main:home')
    professional.email_2fa_enabled = True
    professional.must_setup_2fa = False
    professional.save()
    messages.success(request, 'E-Mail 2FA aktiviert!')
    return redirect('professional_portal:dashboard')

@login_required(login_url='account:login')
def verify_email_2fa(request):
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        return redirect('main:home')
    if request.method == 'POST':
        code = request.POST.get('code', '')
        if code == professional.email_2fa_code:
            professional.email_2fa_code = None
            professional.save()
            messages.success(request, 'Erfolgreich eingeloggt!')
            return redirect('professional_portal:dashboard')
        else:
            messages.error(request, 'Falscher Code.')
    return render(request, 'professional_portal/email_2fa.html', {'email': professional.email})

@login_required(login_url='account:login')
def resend_email_code(request):
    try:
        professional = Professional.objects.get(user=request.user)
    except Professional.DoesNotExist:
        return redirect('main:home')
    code = str(random.randint(100000, 999999))
    professional.email_2fa_code = code
    professional.email_2fa_code_created = timezone.now()
    professional.save()
    try:
        send_mail('Ihr Login-Code', f'Ihr Code: {code}', settings.EMAIL_HOST_USER, [professional.email], fail_silently=False)
        messages.success(request, 'Neuer Code gesendet!')
    except:
        messages.error(request, 'E-Mail konnte nicht gesendet werden.')
    return redirect('professional_portal:verify_email_2fa')
