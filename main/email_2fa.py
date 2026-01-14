# -*- coding: utf-8 -*-
"""
E-Mail 2FA fuer Professional-Accounts
"""
import random
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from django.conf import settings
from datetime import timedelta
from .professional_models import Professional


def generate_code():
    """Generiert 6-stelligen Code"""
    return str(random.randint(100000, 999999))


def send_2fa_code(professional):
    """Sendet 2FA-Code per E-Mail"""
    code = generate_code()
    professional.email_2fa_code = code
    professional.email_2fa_code_created = timezone.now()
    professional.save()
    
    subject = "Ihr Login-Code / Vas kod za prijavu - 123-Kroatien.eu"
    message = f"""
Guten Tag {professional.name},

Ihr Sicherheitscode fuer die Anmeldung lautet:

    {code}

Dieser Code ist 10 Minuten gueltig.

---

Dobar dan {professional.name},

Vas sigurnosni kod za prijavu je:

    {code}

Ovaj kod vrijedi 10 minuta.

---
123-Kroatien.eu
"""
    
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [professional.email],
            fail_silently=False
        )
        return True
    except Exception as e:
        print(f"E-Mail Fehler: {e}")
        return False


def email_2fa_send(request):
    """Sendet 2FA-Code und zeigt Eingabeformular"""
    user_id = request.session.get("email_2fa_user_id")
    
    if not user_id:
        return redirect("account:login")
    
    try:
        user = User.objects.get(id=user_id)
        professional = Professional.objects.get(user=user)
    except:
        return redirect("account:login")
    
    lang = request.session.get("site_language", "ge")
    
    # Code senden wenn noch keiner existiert oder abgelaufen
    should_send = False
    if not professional.email_2fa_code:
        should_send = True
    elif professional.email_2fa_code_created:
        if timezone.now() - professional.email_2fa_code_created > timedelta(minutes=10):
            should_send = True
    
    if should_send:
        if send_2fa_code(professional):
            messages.success(request, "Code wurde an Ihre E-Mail gesendet. / Kod je poslan na vas email.")
        else:
            messages.error(request, "E-Mail konnte nicht gesendet werden. / Email nije mogao biti poslan.")
    
    return render(request, "makler_portal/email_2fa.html", {
        "professional": professional,
        "lang": lang,
    })


def email_2fa_verify(request):
    """Verifiziert den eingegebenen Code"""
    user_id = request.session.get("email_2fa_user_id")
    
    if not user_id:
        return redirect("account:login")
    
    lang = request.session.get("site_language", "ge")
    
    if request.method == "POST":
        code = request.POST.get("code", "").strip()
        
        try:
            user = User.objects.get(id=user_id)
            professional = Professional.objects.get(user=user)
            
            # Code pruefen
            if professional.email_2fa_code == code:
                # Pruefen ob abgelaufen (10 Minuten)
                if professional.email_2fa_code_created:
                    if timezone.now() - professional.email_2fa_code_created > timedelta(minutes=10):
                        messages.error(request, "Code abgelaufen. Neuer Code wurde gesendet. / Kod je istekao. Novi kod je poslan.")
                        send_2fa_code(professional)
                        return redirect("main:email_2fa_send")
                
                # Login erfolgreich
                auth_login(request, user)
                
                # Aufraeumen
                professional.email_2fa_code = None
                professional.email_2fa_code_created = None
                professional.must_setup_2fa = False
                professional.save()
                
                if "email_2fa_user_id" in request.session:
                    del request.session["email_2fa_user_id"]
                
                messages.success(request, "Erfolgreich eingeloggt! / Uspjesno prijavljeni!")
                
                if professional.professional_type in ["real_estate_agent", "construction_company"]:
                    return redirect("main:makler_dashboard")
                else:
                    return redirect("professional_portal:dashboard")
            else:
                messages.error(request, "Falscher Code. / Pogresan kod.")
                
        except Exception as e:
            print(f"2FA Verify Fehler: {e}")
            messages.error(request, "Ein Fehler ist aufgetreten. / Doslo je do greske.")
    
    return redirect("main:email_2fa_send")


def email_2fa_resend(request):
    """Sendet neuen Code"""
    user_id = request.session.get("email_2fa_user_id")
    
    if not user_id:
        return redirect("account:login")
    
    try:
        user = User.objects.get(id=user_id)
        professional = Professional.objects.get(user=user)
        
        if send_2fa_code(professional):
            messages.success(request, "Neuer Code wurde gesendet. / Novi kod je poslan.")
        else:
            messages.error(request, "E-Mail konnte nicht gesendet werden. / Email nije mogao biti poslan.")
            
    except Exception as e:
        print(f"Resend Fehler: {e}")
    
    return redirect("main:email_2fa_send")


def choose_2fa_method(request):
    """Zeigt Auswahlseite fuer 2FA-Methode"""
    from django.contrib.auth.decorators import login_required
    
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    professional = None
    try:
        professional = Professional.objects.get(user=request.user)
    except:
        return redirect('professional_portal:dashboard')
    
    lang = request.session.get('site_language', 'ge')
    
    return render(request, 'makler_portal/2fa_auswahl.html', {
        'professional': professional,
        'lang': lang,
    })


def choose_email_2fa(request):
    """Aktiviert E-Mail 2FA fuer den Nutzer"""
    if not request.user.is_authenticated:
        return redirect('account:login')
    
    try:
        professional = Professional.objects.get(user=request.user)
        professional.email_2fa_enabled = True
        professional.totp_enabled = False
        professional.must_setup_2fa = False
        professional.save()
        messages.success(request, 'E-Mail 2FA wurde aktiviert! / Email 2FA je aktiviran!')
        
        if professional.professional_type in ['real_estate_agent', 'construction_company']:
            return redirect('main:makler_dashboard')
        else:
            return redirect('main:home')
    except:
        return redirect('main:home')
