# Erweiterte views.py für accounts App mit SMS-OTP
# Ersetzt/erweitert die bestehenden Registrierungs- und Login-Views

from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact
from .models import Agent, OTPVerification, SMSOTPVerification
from django.contrib.auth import logout, login, authenticate
from pages.models import Topbar
import re, random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
from django.template.loader import render_to_string
import json
from django.contrib.auth.decorators import login_required
from django.utils import translation

# SMS-Service importieren
try:
    from .sms_service import SMSService
    sms_service = SMSService()
except ImportError:
    sms_service = None
    print("WARNUNG: SMS-Service konnte nicht geladen werden!")


def register(request):
    """
    Makler-Registrierung mit Email-OTP und SMS-OTP (Zwei-Faktor)
    Schritt 1: Registrierungsformular mit PFLICHT-Mobilnummer
    """
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        city = request.POST.get('city')
        country = request.POST.get('country')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        # NEU: Mobilnummer PFLICHTFELD
        mobile = request.POST.get('mobile')
        
        # Company data
        company_name = request.POST.get('company_name')
        company_logo = request.FILES.get('company_logo')
        portrait_photo = request.FILES.get('portrait_photo')
        oib_number = request.POST.get('oib_number')
        domain = request.POST.get('domain')

        # VALIDIERUNG: Mobilnummer MUSS angegeben werden
        if not mobile:
            messages.error(request, 'Mobilnummer ist Pflichtfeld für die Registrierung')
            return render(request, 'account/signup.html')
        
        # VALIDIERUNG: Mobilnummer Format (kroatisch: +385...)
        if not mobile.startswith('+385') and not mobile.startswith('385'):
            messages.error(request, 'Bitte geben Sie eine gültige kroatische Mobilnummer ein (z.B. +385...)')
            return render(request, 'account/signup.html')
        
        # Mobilnummer normalisieren
        if not mobile.startswith('+'):
            mobile = '+' + mobile

        # Check if first name and lastname contains numbers
        if any(char.isdigit() for char in first_name) or any(char.isdigit() for char in last_name):
            messages.error(request, 'Vor- und Nachname dürfen keine Zahlen enthalten')
            return render(request, 'account/signup.html')

        # Check valid email
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(regex, email):
            messages.error(request, 'Ungültige Email-Adresse')
            return render(request, 'account/signup.html')

        username = email.split('@')[0]
        if User.objects.filter(username=username).exists():
            username = username + str(User.objects.filter(username=username).count())

        if password != password2:
            messages.error(request, 'Passwörter stimmen nicht überein')
            return render(request, 'account/signup.html')
        
        if len(password) < 6:
            messages.error(request, 'Passwort muss mindestens 6 Zeichen lang sein')
            return render(request, 'account/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email-Adresse existiert bereits')
            return render(request, 'account/signup.html')

        # User erstellen
        user = User.objects.create_user(username, email, password)
        user.save()

        # Agent-Profil erstellen (MIT Mobilnummer!)
        userProfile = Agent.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            city=city,
            country=country,
            company_name=company_name,
            company_logo=company_logo,
            profile_image=portrait_photo,
            oib_number=oib_number,
            domain=domain,
            email=email,
            mobile=mobile,  # WICHTIG: Mobilnummer speichern!
        )
        userProfile.save()

        # User einloggen
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            # SCHRITT 1: Email-OTP generieren und senden
            email_otp = random.randint(100000, 999999)
            otpVerification = OTPVerification.objects.get_or_create(user=request.user)[0]
            otpVerification.otp = email_otp
            otpVerification.sent_at = timezone.now()
            otpVerification.is_verified = False
            otpVerification.save()

            # Email-OTP senden
            name = request.user.first_name
            template = render_to_string(
                'account/otpEmail.html', 
                {'name': name, 'otp': email_otp, 'action': 'Email verifizieren'}
            )
            send_mail(
                'OTP für Email-Verifizierung',
                template,
                settings.EMAIL_HOST_USER,
                [email],
                fail_silently=False,
                html_message=template,
            )
            
            messages.success(request, f'Email-OTP wurde an {email} gesendet')
            
            context = {
                'verifyEmailPage': True,
                'title': 'Email verifizieren',
                'mobile': mobile,  # Für nächsten Schritt
            }
            return render(request, 'account/verifyEmail.html', context)
        
        return redirect('account:login')
    
    return render(request, 'account/signup.html')


@login_required(login_url='account:login')
def verifyEmail(request):
    """
    Email-Verifizierung (Schritt 1 von 2)
    Nach Erfolg: Weiter zu SMS-OTP
    """
    if request.method == 'POST':
        otp = request.POST.get('otp')
        otpVerification = OTPVerification.objects.get(user=request.user)
        now = timezone.now()
        
        # Check if OTP expired (5 minutes)
        if now - otpVerification.sent_at > timedelta(minutes=5):
            messages.error(request, 'OTP abgelaufen. Bitte fordern Sie einen neuen an.')
            context = {
                'verifyEmailPage': True,
                'title': 'Email verifizieren',
                'resend_button': True
            }
            return render(request, 'account/verifyEmail.html', context)

        # Check OTP
        if str(otpVerification.otp) == otp:
            # Email verifiziert!
            otpVerification.is_verified = True
            otpVerification.save()
            messages.success(request, 'Email erfolgreich verifiziert!')
            
            # WEITER ZU SCHRITT 2: SMS-OTP
            return redirect('account:verify_sms')
        else:
            messages.error(request, 'Ungültiger OTP-Code')
            context = {
                'verifyEmailPage': True,
                'title': 'Email verifizieren',
            }
            return render(request, 'account/verifyEmail.html', context)

    # GET Request: OTP senden
    email = request.user.email
    otp = random.randint(100000, 999999)

    otpVerification = OTPVerification.objects.get_or_create(user=request.user)[0]
    now = timezone.now()
    
    # Rate limiting: Nicht öfter als alle 2 Minuten
    if now - otpVerification.sent_at < timedelta(minutes=2):
        try_after = 2 - (now - otpVerification.sent_at).seconds // 60
        messages.error(request, f'OTP bereits gesendet. Versuchen Sie es in {try_after} Minute(n) erneut')
        context = {
            'verifyEmailPage': True,
            'title': 'Email verifizieren',
            'resend_button': True,
        }
        return render(request, 'account/verifyEmail.html', context)
    
    otpVerification.otp = otp
    otpVerification.sent_at = timezone.now()
    otpVerification.save()

    # Email senden
    name = request.user.first_name
    template = render_to_string(
        'account/otpEmail.html', 
        {'name': name, 'otp': otp, 'action': 'Email verifizieren'}
    )
    send_mail(
        'OTP für Email-Verifizierung',
        template,
        settings.EMAIL_HOST_USER,
        [email],
        fail_silently=False,
        html_message=template,
    )
    
    message = f'OTP an {email} gesendet'
    messages.success(request, message)
    
    context = {
        'verifyEmailPage': True,
        'title': 'Email verifizieren',
    }
    return render(request, 'account/verifyEmail.html', context)


@login_required(login_url='account:login')
def verify_sms(request):
    """
    SMS-OTP-Verifizierung (Schritt 2 von 2)
    Wird nach erfolgreicher Email-Verifizierung aufgerufen
    """
    
    # Prüfen ob Email bereits verifiziert
    email_otp = OTPVerification.objects.filter(user=request.user).first()
    if not email_otp or not email_otp.is_verified:
        messages.error(request, 'Bitte verifizieren Sie zuerst Ihre Email-Adresse')
        return redirect('account:verify_email')
    
    # Agent-Profil holen (für Mobilnummer)
    try:
        agent = Agent.objects.get(user=request.user)
        mobile = agent.mobile
    except Agent.DoesNotExist:
        messages.error(request, 'Kein Agent-Profil gefunden')
        return redirect('main:home')
    
    if not mobile:
        messages.error(request, 'Keine Mobilnummer hinterlegt')
        return redirect('main:home')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        
        # SMS-OTP aus Datenbank holen
        try:
            sms_otp = SMSOTPVerification.objects.filter(user=request.user).latest('sent_at')
        except SMSOTPVerification.DoesNotExist:
            messages.error(request, 'Kein SMS-OTP gefunden. Bitte fordern Sie einen neuen an.')
            return redirect('account:verify_sms')
        
        # OTP abgelaufen? (5 Minuten)
        if sms_otp.is_expired():
            messages.error(request, 'SMS-OTP abgelaufen. Bitte fordern Sie einen neuen an.')
            context = {
                'verifySMSPage': True,
                'title': 'SMS verifizieren',
                'mobile': mobile,
                'resend_button': True
            }
            return render(request, 'account/verifySMS.html', context)
        
        # Zu viele Versuche?
        if sms_otp.attempts >= 5:
            messages.error(request, 'Zu viele fehlerhafte Versuche. Bitte fordern Sie einen neuen Code an.')
            sms_otp.delete()
            return redirect('account:verify_sms')
        
        # OTP prüfen
        if str(sms_otp.otp) == otp:
            # SMS verifiziert!
            sms_otp.is_verified = True
            sms_otp.save()
            
            # Agent aktivieren (beide OTPs verifiziert)
            agent.is_active = True
            agent.save()
            
            messages.success(request, 'Registrierung erfolgreich abgeschlossen! Ihr Account ist jetzt aktiv.')
            return redirect('main:home')
        else:
            # Falscher Code
            sms_otp.attempts += 1
            sms_otp.save()
            
            remaining = 5 - sms_otp.attempts
            messages.error(request, f'Ungültiger SMS-Code. Noch {remaining} Versuch(e) übrig.')
            
            context = {
                'verifySMSPage': True,
                'title': 'SMS verifizieren',
                'mobile': mobile,
            }
            return render(request, 'account/verifySMS.html', context)
    
    # GET Request: SMS-OTP senden
    
    # Prüfen ob SMS-Service verfügbar
    if not sms_service:
        messages.error(request, 'SMS-Service nicht verfügbar. Bitte kontaktieren Sie den Support.')
        return redirect('main:home')
    
    # Rate Limiting: Nicht öfter als alle 2 Minuten
    recent_sms = SMSOTPVerification.objects.filter(
        user=request.user,
        sent_at__gte=timezone.now() - timedelta(minutes=2)
    ).first()
    
    if recent_sms:
        time_diff = timezone.now() - recent_sms.sent_at
        wait_seconds = 120 - time_diff.seconds
        wait_minutes = wait_seconds // 60
        messages.error(request, f'SMS bereits gesendet. Bitte warten Sie {wait_minutes} Minute(n)')
        context = {
            'verifySMSPage': True,
            'title': 'SMS verifizieren',
            'mobile': mobile,
            'resend_button': True
        }
        return render(request, 'account/verifySMS.html', context)
    
    # SMS-OTP generieren
    sms_otp_code = sms_service.generate_otp()
    
    # SMS senden
    result = sms_service.send_registration_sms(
        phone_number=mobile,
        otp_code=sms_otp_code,
        user_name=agent.first_name or request.user.username
    )
    
    if result['success']:
        # SMS-OTP in Datenbank speichern
        SMSOTPVerification.objects.create(
            user=request.user,
            phone_number=mobile,
            otp=sms_otp_code,
            is_verified=False,
            attempts=0
        )
        
        # Mobile number maskieren für Anzeige (z.B. +385 91 *** **45)
        masked_mobile = mobile[:7] + '***' + mobile[-2:]
        
        messages.success(request, f'SMS-Code wurde an {masked_mobile} gesendet')
        
        context = {
            'verifySMSPage': True,
            'title': 'SMS verifizieren',
            'mobile': masked_mobile,
        }
        return render(request, 'account/verifySMS.html', context)
    else:
        # SMS-Versand fehlgeschlagen
        messages.error(request, f'SMS konnte nicht gesendet werden: {result["message"]}')
        context = {
            'verifySMSPage': True,
            'title': 'SMS verifizieren',
            'mobile': mobile,
            'error': True
        }
        return render(request, 'account/verifySMS.html', context)


def login_view(request):
    """
    Login mit SMS-OTP nach Passwort-Eingabe
    """
    site_language = request.session.get('site_language')
    if not site_language:
        request.session['site_language'] = 'ge'
    
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is None:
            # Try to authenticate with email
            try:
                user = User.objects.get(email=username)
                user = authenticate(request, username=user.username, password=password)
            except User.DoesNotExist:
                messages.error(request, 'Ungültiger Benutzername oder Passwort')
                return render(request, 'account/login.html')
            
        if user is not None:
            # Passwort korrekt! Jetzt SMS-OTP senden
            auth.login(request, user)
            
            # Agent-Profil holen
            try:
                agent = Agent.objects.get(user=user)
                mobile = agent.mobile
                
                if mobile and sms_service:
                    # SMS-OTP generieren und senden
                    sms_otp_code = sms_service.generate_otp()
                    
                    result = sms_service.send_login_sms(
                        phone_number=mobile,
                        otp_code=sms_otp_code,
                        user_name=agent.first_name or user.username
                    )
                    
                    if result['success']:
                        # SMS-OTP speichern
                        SMSOTPVerification.objects.create(
                            user=user,
                            phone_number=mobile,
                            otp=sms_otp_code,
                            is_verified=False,
                            attempts=0
                        )
                        
                        messages.success(request, 'SMS-Code wurde gesendet')
                        return redirect('account:verify_login_sms')
                    else:
                        messages.error(request, 'SMS konnte nicht gesendet werden')
                        logout(request)
                        return redirect('account:login')
                else:
                    # Keine Mobilnummer oder SMS-Service nicht verfügbar
                    messages.warning(request, 'SMS-Verifizierung nicht möglich. Bitte kontaktieren Sie den Support.')
                    logout(request)
                    return redirect('account:login')
                    
            except Agent.DoesNotExist:
                messages.error(request, 'Kein Agent-Profil gefunden')
                logout(request)
                return redirect('account:login')
        else:
            messages.error(request, 'Ungültige Zugangsdaten')
            return redirect('account:login')

    else:
        tb = Topbar.objects.get()
        return render(request, 'account/login.html', {'tb':tb})


@login_required(login_url='account:login')
def verify_login_sms(request):
    """
    SMS-OTP-Verifizierung beim Login
    """
    try:
        agent = Agent.objects.get(user=request.user)
        mobile = agent.mobile
    except Agent.DoesNotExist:
        messages.error(request, 'Kein Agent-Profil gefunden')
        logout(request)
        return redirect('account:login')
    
    if request.method == 'POST':
        otp = request.POST.get('otp')
        
        try:
            sms_otp = SMSOTPVerification.objects.filter(user=request.user).latest('sent_at')
        except SMSOTPVerification.DoesNotExist:
            messages.error(request, 'Kein SMS-OTP gefunden')
            logout(request)
            return redirect('account:login')
        
        # OTP abgelaufen?
        if sms_otp.is_expired():
            messages.error(request, 'SMS-OTP abgelaufen')
            logout(request)
            sms_otp.delete()
            return redirect('account:login')
        
        # Zu viele Versuche?
        if sms_otp.attempts >= 3:
            messages.error(request, 'Zu viele fehlerhafte Versuche')
            logout(request)
            sms_otp.delete()
            return redirect('account:login')
        
        # OTP prüfen
        if str(sms_otp.otp) == otp:
            # Login erfolgreich!
            sms_otp.is_verified = True
            sms_otp.save()
            
            messages.success(request, 'Erfolgreich angemeldet!')
            return redirect('main:agent', id=agent.id)
        else:
            sms_otp.attempts += 1
            sms_otp.save()
            
            remaining = 3 - sms_otp.attempts
            messages.error(request, f'Ungültiger Code. Noch {remaining} Versuch(e)')
            
            context = {
                'verifyLoginSMSPage': True,
                'title': 'Login bestätigen',
                'mobile': mobile[:7] + '***' + mobile[-2:],
            }
            return render(request, 'account/verifyLoginSMS.html', context)
    
    # GET Request
    masked_mobile = mobile[:7] + '***' + mobile[-2:] if mobile else 'Unbekannt'
    
    context = {
        'verifyLoginSMSPage': True,
        'title': 'Login bestätigen',
        'mobile': masked_mobile,
    }
    return render(request, 'account/verifyLoginSMS.html', context)


def logout_view(request):
    logout(request)
    return redirect('account:login')
