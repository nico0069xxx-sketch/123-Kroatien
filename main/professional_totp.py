# -*- coding: utf-8 -*-
"""
TOTP 2FA fuer Professional-Accounts (Makler, Bauunternehmen, etc.)
"""
import pyotp
import qrcode
import io
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from .professional_models import Professional


def get_professional_for_user(user):
    """Holt das Professional-Profil fuer einen User"""
    try:
        return Professional.objects.get(user=user)
    except Professional.DoesNotExist:
        return None


@login_required
def professional_setup_2fa(request):
    """2FA einrichten - QR-Code anzeigen"""
    professional = get_professional_for_user(request.user)
    
    if not professional:
        messages.error(request, "Kein Professional-Profil gefunden.")
        return redirect("main:home")
    
    if not professional.is_verified or not professional.is_active:
        messages.error(request, "Ihr Profil wurde noch nicht freigeschaltet.")
        return redirect("main:home")
    
    # TOTP-Secret generieren falls nicht vorhanden
    if not professional.totp_secret:
        professional.totp_secret = pyotp.random_base32()
        professional.save()
    
    # QR-Code generieren
    totp = pyotp.TOTP(professional.totp_secret)
    uri = totp.provisioning_uri(
        name=professional.email, 
        issuer_name="123-Kroatien.eu"
    )
    
    qr = qrcode.make(uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    lang = request.session.get("site_language", "ge")
    
    return render(request, "makler_portal/setup_2fa.html", {
        "qr_code": qr_base64,
        "secret": professional.totp_secret,
        "professional": professional,
        "lang": lang,
    })


@login_required
def professional_verify_2fa_setup(request):
    """2FA-Setup verifizieren mit erstem Code"""
    if request.method != "POST":
        return redirect("main:professional_setup_2fa")
    
    professional = get_professional_for_user(request.user)
    if not professional:
        return redirect("main:home")
    
    code = request.POST.get("code", "").strip()
    
    if not code:
        messages.error(request, "Bitte Code eingeben.")
        return redirect("main:professional_setup_2fa")
    
    totp = pyotp.TOTP(professional.totp_secret)
    
    if totp.verify(code, valid_window=1):
        professional.totp_enabled = True
        professional.totp_verified = True
        professional.must_setup_2fa = False
        professional.save()
        
        messages.success(request, "2FA wurde erfolgreich aktiviert!")
        
        if professional.professional_type in ["real_estate_agent", "construction_company"]:
            return redirect("main:makler_dashboard")
        else:
            return redirect("main:home")
    else:
        messages.error(request, "Falscher Code. Bitte erneut versuchen.")
        return redirect("main:professional_setup_2fa")


def professional_verify_2fa_login(request):
    """2FA-Verifizierung beim Login"""
    user_id = request.session.get("professional_2fa_user_id")
    
    if not user_id:
        return redirect("main:professional_login")
    
    lang = request.session.get("site_language", "ge")
    
    if request.method == "POST":
        try:
            user = User.objects.get(id=user_id)
            professional = get_professional_for_user(user)
            
            if not professional:
                messages.error(request, "Kein Professional-Profil gefunden.")
                return redirect("main:professional_login")
            
            code = request.POST.get("code", "").strip()
            totp = pyotp.TOTP(professional.totp_secret)
            
            if totp.verify(code, valid_window=1):
                auth_login(request, user)
                
                if "professional_2fa_user_id" in request.session:
                    del request.session["professional_2fa_user_id"]
                
                messages.success(request, "Erfolgreich eingeloggt!")
                
                if professional.professional_type in ["real_estate_agent", "construction_company"]:
                    return redirect("main:makler_dashboard")
                else:
                    return redirect("main:home")
            else:
                messages.error(request, "Falscher Code.")
                
        except User.DoesNotExist:
            messages.error(request, "Benutzer nicht gefunden.")
            return redirect("main:professional_login")
    
    return render(request, "makler_portal/verify_2fa.html", {"lang": lang})


def professional_login(request):
    """Spezieller Login fuer Professionals mit 2FA-Support"""
    from django.contrib.auth import authenticate
    
    print("=== PROFESSIONAL LOGIN VIEW AUFGERUFEN ===")
    print(f"Method: {request.method}")
    print(f"User authenticated: {request.user.is_authenticated}")
    
    # Falls bereits eingeloggt, zur 2FA-Pruefung
    if request.user.is_authenticated:
        professional = get_professional_for_user(request.user)
        if professional:
            print(f"Bereits eingeloggt als: {professional.name}")
            if professional.must_setup_2fa and not professional.totp_enabled:
                print("-> Weiterleitung zu 2FA Setup")
                return redirect("main:professional_setup_2fa")
    
    lang = request.session.get("site_language", "ge")
    
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        
        user = authenticate(request, username=username, password=password)
        
        if user is None:
            try:
                user_obj = User.objects.get(email=username)
                user = authenticate(request, username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        
        if user is not None:
            professional = get_professional_for_user(user)
            
            if not professional:
                messages.error(request, "Kein Professional-Zugang.")
                return render(request, "makler_portal/login.html", {"lang": lang})
            
            if not professional.is_verified or not professional.is_active:
                messages.error(request, "Ihr Profil wurde noch nicht freigeschaltet.")
                return render(request, "makler_portal/login.html", {"lang": lang})
            
            if professional.must_setup_2fa and not professional.totp_enabled:
                auth_login(request, user)
                return redirect("main:professional_setup_2fa")
            
            if professional.totp_enabled:
                request.session["professional_2fa_user_id"] = user.id
                return redirect("main:professional_verify_2fa")
            
            auth_login(request, user)
            
            if professional.professional_type in ["real_estate_agent", "construction_company"]:
                return redirect("main:makler_dashboard")
            else:
                return redirect("main:home")
        else:
            messages.error(request, "Falsche Zugangsdaten.")
    
    return render(request, "makler_portal/login.html", {"lang": lang})
