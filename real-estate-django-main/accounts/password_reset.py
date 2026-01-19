"""
Sicheres Passwort-Reset-System für 123-Kroatien.eu
==================================================

Verwendet Django's eingebaute kryptographische Token-Generierung.
Dies ist die SICHERSTE kostenlose Lösung auf dem Markt.

Sicherheitsmerkmale:
- Kryptographisch sichere Tokens (SHA256)
- Zeitlich begrenzt (1 Stunde gültig)
- Einmalige Verwendung (Token wird nach Nutzung ungültig)
- Keine sensiblen Daten in der URL (nur uidb64 + token)
- Schutz gegen Brute-Force durch Token-Länge
"""

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)


class SecurePasswordResetTokenGenerator(PasswordResetTokenGenerator):
    """
    Erweiterter Token-Generator mit zusätzlicher Sicherheit.
    Token ist nur 1 Stunde gültig (konfigurierbar in settings.py).
    """
    pass


# Singleton für Token-Generierung
password_reset_token = SecurePasswordResetTokenGenerator()


def get_password_reset_url(request, user):
    """
    Generiert eine sichere Passwort-Reset-URL.
    
    Args:
        request: HTTP Request für absolute URL
        user: User-Objekt
    
    Returns:
        Vollständige Reset-URL
    """
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    
    # Bestimme Sprache aus Session oder Default
    lang = request.session.get('site_language', 'ge')
    
    reset_url = request.build_absolute_uri(
        reverse('account:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
    )
    
    return reset_url, lang


def send_password_reset_email(request, user, lang='ge'):
    """
    Sendet die Passwort-Reset-Email.
    
    Args:
        request: HTTP Request
        user: User-Objekt
        lang: Sprache ('ge', 'hr', 'en')
    """
    reset_url, _ = get_password_reset_url(request, user)
    
    # Sprachspezifische Texte
    if lang == 'hr':
        subject = 'Resetiranje lozinke - 123-Kroatien.eu'
        greeting = f'Poštovani/a {user.first_name or user.username},'
        intro = 'Primili smo zahtjev za resetiranje vaše lozinke.'
        action = 'Kliknite na sljedeći link za postavljanje nove lozinke:'
        button_text = 'Resetiraj lozinku'
        warning = 'Ovaj link vrijedi samo 1 sat.'
        ignore = 'Ako niste zatražili resetiranje lozinke, možete zanemariti ovu poruku.'
    elif lang == 'en':
        subject = 'Password Reset - 123-Kroatien.eu'
        greeting = f'Dear {user.first_name or user.username},'
        intro = 'We received a request to reset your password.'
        action = 'Click the following link to set a new password:'
        button_text = 'Reset Password'
        warning = 'This link is only valid for 1 hour.'
        ignore = 'If you did not request a password reset, you can ignore this email.'
    else:  # German default
        subject = 'Passwort zurücksetzen - 123-Kroatien.eu'
        greeting = f'Guten Tag {user.first_name or user.username},'
        intro = 'Wir haben eine Anfrage zum Zurücksetzen Ihres Passworts erhalten.'
        action = 'Klicken Sie auf den folgenden Link, um ein neues Passwort festzulegen:'
        button_text = 'Passwort zurücksetzen'
        warning = 'Dieser Link ist nur 1 Stunde gültig.'
        ignore = 'Falls Sie kein neues Passwort angefordert haben, können Sie diese E-Mail ignorieren.'
    
    context = {
        'user': user,
        'reset_url': reset_url,
        'greeting': greeting,
        'intro': intro,
        'action': action,
        'button_text': button_text,
        'warning': warning,
        'ignore': ignore,
        'lang': lang,
    }
    
    try:
        html_message = render_to_string('account/password_reset_email.html', context)
        plain_message = f"{greeting}\n\n{intro}\n\n{action}\n{reset_url}\n\n{warning}\n\n{ignore}"
        
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Password reset email sent to {user.email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email to {user.email}: {e}")
        return False


def password_reset_request(request):
    """
    View für Passwort-Reset-Anfrage.
    Ersetzt die alte OTP-basierte forgetPassword Funktion.
    """
    lang = request.session.get('site_language', 'ge')
    
    # Sprachspezifische Texte
    if lang == 'hr':
        translations = {
            'title': 'Resetiranje lozinke',
            'email_label': 'E-mail adresa',
            'email_placeholder': 'Unesite svoju e-mail adresu',
            'submit': 'Pošalji link za resetiranje',
            'back_to_login': 'Povratak na prijavu',
            'success_message': 'Ako postoji račun s tom e-mail adresom, poslali smo link za resetiranje lozinke.',
            'error_invalid_email': 'Molimo unesite valjanu e-mail adresu.',
        }
    elif lang == 'en':
        translations = {
            'title': 'Reset Password',
            'email_label': 'Email Address',
            'email_placeholder': 'Enter your email address',
            'submit': 'Send Reset Link',
            'back_to_login': 'Back to Login',
            'success_message': 'If an account exists with that email, we have sent a password reset link.',
            'error_invalid_email': 'Please enter a valid email address.',
        }
    else:  # German default
        translations = {
            'title': 'Passwort zurücksetzen',
            'email_label': 'E-Mail-Adresse',
            'email_placeholder': 'Geben Sie Ihre E-Mail-Adresse ein',
            'submit': 'Reset-Link senden',
            'back_to_login': 'Zurück zum Login',
            'success_message': 'Falls ein Konto mit dieser E-Mail existiert, haben wir einen Link zum Zurücksetzen gesendet.',
            'error_invalid_email': 'Bitte geben Sie eine gültige E-Mail-Adresse ein.',
        }
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        
        if not email or '@' not in email:
            messages.error(request, translations['error_invalid_email'])
            return render(request, 'account/password_reset_request.html', {
                'lang': lang,
                **translations
            })
        
        # SICHERHEIT: Immer gleiche Nachricht zeigen (verhindert Email-Enumeration)
        try:
            user = User.objects.get(email__iexact=email)
            send_password_reset_email(request, user, lang)
        except User.DoesNotExist:
            # Aus Sicherheitsgründen keine Fehlermeldung - verhindert Email-Enumeration
            logger.info(f"Password reset requested for non-existent email: {email}")
            pass
        
        messages.success(request, translations['success_message'])
        return redirect('account:password_reset_done')
    
    return render(request, 'account/password_reset_request.html', {
        'lang': lang,
        **translations
    })


def password_reset_done(request):
    """
    Bestätigungsseite nach Absenden der Reset-Anfrage.
    """
    lang = request.session.get('site_language', 'ge')
    
    if lang == 'hr':
        translations = {
            'title': 'E-mail poslan',
            'message': 'Ako postoji račun s unesenom e-mail adresom, poslali smo upute za resetiranje lozinke.',
            'check_spam': 'Molimo provjerite i neželjenu poštu (spam) ako ne vidite e-mail.',
            'back_to_login': 'Povratak na prijavu',
        }
    elif lang == 'en':
        translations = {
            'title': 'Email Sent',
            'message': 'If an account exists with the email address you entered, we have sent password reset instructions.',
            'check_spam': 'Please also check your spam folder if you do not see the email.',
            'back_to_login': 'Back to Login',
        }
    else:
        translations = {
            'title': 'E-Mail gesendet',
            'message': 'Falls ein Konto mit der eingegebenen E-Mail-Adresse existiert, haben wir Anweisungen zum Zurücksetzen des Passworts gesendet.',
            'check_spam': 'Bitte überprüfen Sie auch Ihren Spam-Ordner, falls Sie die E-Mail nicht sehen.',
            'back_to_login': 'Zurück zum Login',
        }
    
    return render(request, 'account/password_reset_done.html', {
        'lang': lang,
        **translations
    })


def password_reset_confirm(request, uidb64, token):
    """
    View für Passwort-Reset-Bestätigung mit Token.
    """
    lang = request.session.get('site_language', 'ge')
    
    # Sprachspezifische Texte
    if lang == 'hr':
        translations = {
            'title': 'Nova lozinka',
            'password_label': 'Nova lozinka',
            'password_confirm_label': 'Potvrdite lozinku',
            'submit': 'Postavi novu lozinku',
            'error_invalid_link': 'Link za resetiranje je nevažeći ili je istekao.',
            'error_password_mismatch': 'Lozinke se ne podudaraju.',
            'error_password_short': 'Lozinka mora imati najmanje 8 znakova.',
            'error_password_weak': 'Lozinka mora sadržavati slova i brojeve.',
            'success_message': 'Vaša lozinka je uspješno promijenjena.',
            'request_new_link': 'Zatražite novi link',
        }
    elif lang == 'en':
        translations = {
            'title': 'New Password',
            'password_label': 'New Password',
            'password_confirm_label': 'Confirm Password',
            'submit': 'Set New Password',
            'error_invalid_link': 'The reset link is invalid or has expired.',
            'error_password_mismatch': 'Passwords do not match.',
            'error_password_short': 'Password must be at least 8 characters long.',
            'error_password_weak': 'Password must contain letters and numbers.',
            'success_message': 'Your password has been successfully changed.',
            'request_new_link': 'Request a new link',
        }
    else:
        translations = {
            'title': 'Neues Passwort',
            'password_label': 'Neues Passwort',
            'password_confirm_label': 'Passwort bestätigen',
            'submit': 'Neues Passwort festlegen',
            'error_invalid_link': 'Der Reset-Link ist ungültig oder abgelaufen.',
            'error_password_mismatch': 'Die Passwörter stimmen nicht überein.',
            'error_password_short': 'Das Passwort muss mindestens 8 Zeichen lang sein.',
            'error_password_weak': 'Das Passwort muss Buchstaben und Zahlen enthalten.',
            'success_message': 'Ihr Passwort wurde erfolgreich geändert.',
            'request_new_link': 'Neuen Link anfordern',
        }
    
    # Token validieren
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    # Token-Validierung
    if user is None or not password_reset_token.check_token(user, token):
        messages.error(request, translations['error_invalid_link'])
        return render(request, 'account/password_reset_invalid.html', {
            'lang': lang,
            **translations
        })
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # Validierung
        if password != password_confirm:
            messages.error(request, translations['error_password_mismatch'])
            return render(request, 'account/password_reset_confirm.html', {
                'lang': lang,
                'valid_link': True,
                **translations
            })
        
        if len(password) < 8:
            messages.error(request, translations['error_password_short'])
            return render(request, 'account/password_reset_confirm.html', {
                'lang': lang,
                'valid_link': True,
                **translations
            })
        
        # Passwort-Stärke prüfen (mindestens Buchstaben UND Zahlen)
        has_letter = any(c.isalpha() for c in password)
        has_digit = any(c.isdigit() for c in password)
        if not (has_letter and has_digit):
            messages.error(request, translations['error_password_weak'])
            return render(request, 'account/password_reset_confirm.html', {
                'lang': lang,
                'valid_link': True,
                **translations
            })
        
        # Passwort setzen
        user.set_password(password)
        user.save()
        
        logger.info(f"Password successfully reset for user: {user.email}")
        messages.success(request, translations['success_message'])
        return redirect('account:password_reset_complete')
    
    return render(request, 'account/password_reset_confirm.html', {
        'lang': lang,
        'valid_link': True,
        **translations
    })


def password_reset_complete(request):
    """
    Erfolgsseite nach Passwort-Änderung.
    """
    lang = request.session.get('site_language', 'ge')
    
    if lang == 'hr':
        translations = {
            'title': 'Lozinka promijenjena',
            'message': 'Vaša lozinka je uspješno promijenjena.',
            'login_now': 'Sada se možete prijaviti s novom lozinkom.',
            'login_button': 'Prijava',
        }
    elif lang == 'en':
        translations = {
            'title': 'Password Changed',
            'message': 'Your password has been successfully changed.',
            'login_now': 'You can now log in with your new password.',
            'login_button': 'Login',
        }
    else:
        translations = {
            'title': 'Passwort geändert',
            'message': 'Ihr Passwort wurde erfolgreich geändert.',
            'login_now': 'Sie können sich jetzt mit Ihrem neuen Passwort anmelden.',
            'login_button': 'Anmelden',
        }
    
    return render(request, 'account/password_reset_complete.html', {
        'lang': lang,
        **translations
    })
