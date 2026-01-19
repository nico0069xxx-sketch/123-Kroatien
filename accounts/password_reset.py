"""
Sicheres Passwort-Reset-System für 123-Kroatien.eu
Kryptographisch sichere Token-basierte Passwort-Zurücksetzung
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

password_reset_token = PasswordResetTokenGenerator()


def get_password_reset_url(request, user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = password_reset_token.make_token(user)
    lang = request.session.get('site_language', 'ge')
    reset_url = request.build_absolute_uri(
        reverse('account:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
    )
    return reset_url, lang


def send_password_reset_email(request, user, lang='ge'):
    reset_url, _ = get_password_reset_url(request, user)
    
    if lang == 'hr':
        subject = 'Resetiranje lozinke - 123-Kroatien.eu'
        greeting = f'Postovani/a {user.first_name or user.username},'
        intro = 'Primili smo zahtjev za resetiranje vase lozinke.'
        action = 'Kliknite na sljedeci link za postavljanje nove lozinke:'
        button_text = 'Resetiraj lozinku'
        warning = 'Ovaj link vrijedi samo 1 sat.'
        ignore = 'Ako niste zatrazili resetiranje lozinke, mozete zanemariti ovu poruku.'
    elif lang == 'en':
        subject = 'Password Reset - 123-Kroatien.eu'
        greeting = f'Dear {user.first_name or user.username},'
        intro = 'We received a request to reset your password.'
        action = 'Click the following link to set a new password:'
        button_text = 'Reset Password'
        warning = 'This link is only valid for 1 hour.'
        ignore = 'If you did not request a password reset, you can ignore this email.'
    else:
        subject = 'Passwort zuruecksetzen - 123-Kroatien.eu'
        greeting = f'Guten Tag {user.first_name or user.username},'
        intro = 'Wir haben eine Anfrage zum Zuruecksetzen Ihres Passworts erhalten.'
        action = 'Klicken Sie auf den folgenden Link, um ein neues Passwort festzulegen:'
        button_text = 'Passwort zuruecksetzen'
        warning = 'Dieser Link ist nur 1 Stunde gueltig.'
        ignore = 'Falls Sie kein neues Passwort angefordert haben, koennen Sie diese E-Mail ignorieren.'
    
    context = {
        'user': user, 'reset_url': reset_url, 'greeting': greeting,
        'intro': intro, 'action': action, 'button_text': button_text,
        'warning': warning, 'ignore': ignore, 'lang': lang,
    }
    
    try:
        html_message = render_to_string('account/password_reset_email.html', context)
        plain_message = f"{greeting}\n\n{intro}\n\n{action}\n{reset_url}\n\n{warning}\n\n{ignore}"
        send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message, fail_silently=False)
        return True
    except Exception as e:
        logger.error(f"Failed to send password reset email: {e}")
        return False


def password_reset_request(request):
    lang = request.session.get('site_language', 'ge')
    
    if lang == 'hr':
        translations = {'title': 'Resetiranje lozinke', 'email_label': 'E-mail adresa', 'email_placeholder': 'Unesite svoju e-mail adresu', 'submit': 'Posalji link', 'back_to_login': 'Povratak na prijavu', 'success_message': 'Ako postoji racun s tom e-mail adresom, poslali smo link za resetiranje.', 'error_invalid_email': 'Molimo unesite valjanu e-mail adresu.'}
    elif lang == 'en':
        translations = {'title': 'Reset Password', 'email_label': 'Email Address', 'email_placeholder': 'Enter your email', 'submit': 'Send Reset Link', 'back_to_login': 'Back to Login', 'success_message': 'If an account exists with that email, we have sent a password reset link.', 'error_invalid_email': 'Please enter a valid email address.'}
    else:
        translations = {'title': 'Passwort zuruecksetzen', 'email_label': 'E-Mail-Adresse', 'email_placeholder': 'Geben Sie Ihre E-Mail ein', 'submit': 'Reset-Link senden', 'back_to_login': 'Zurueck zum Login', 'success_message': 'Falls ein Konto mit dieser E-Mail existiert, haben wir einen Link gesendet.', 'error_invalid_email': 'Bitte geben Sie eine gueltige E-Mail-Adresse ein.'}
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if not email or '@' not in email:
            messages.error(request, translations['error_invalid_email'])
            return render(request, 'account/password_reset_request.html', {'lang': lang, **translations})
        try:
            user = User.objects.get(email__iexact=email)
            send_password_reset_email(request, user, lang)
        except User.DoesNotExist:
            pass
        messages.success(request, translations['success_message'])
        return redirect('account:password_reset_done')
    
    return render(request, 'account/password_reset_request.html', {'lang': lang, **translations})


def password_reset_done(request):
    lang = request.session.get('site_language', 'ge')
    if lang == 'hr':
        translations = {'title': 'E-mail poslan', 'message': 'Ako postoji racun, poslali smo upute za resetiranje.', 'check_spam': 'Provjerite i spam folder.', 'back_to_login': 'Povratak na prijavu'}
    elif lang == 'en':
        translations = {'title': 'Email Sent', 'message': 'If an account exists, we have sent reset instructions.', 'check_spam': 'Please check your spam folder.', 'back_to_login': 'Back to Login'}
    else:
        translations = {'title': 'E-Mail gesendet', 'message': 'Falls ein Konto existiert, haben wir Anweisungen gesendet.', 'check_spam': 'Bitte auch Spam-Ordner pruefen.', 'back_to_login': 'Zurueck zum Login'}
    return render(request, 'account/password_reset_done.html', {'lang': lang, **translations})


def password_reset_confirm(request, uidb64, token):
    lang = request.session.get('site_language', 'ge')
    
    if lang == 'hr':
        translations = {'title': 'Nova lozinka', 'password_label': 'Nova lozinka', 'password_confirm_label': 'Potvrdite lozinku', 'submit': 'Postavi novu lozinku', 'error_invalid_link': 'Link je nevazeci ili je istekao.', 'error_password_mismatch': 'Lozinke se ne podudaraju.', 'error_password_short': 'Lozinka mora imati najmanje 8 znakova.', 'error_password_weak': 'Lozinka mora sadrzavati slova i brojeve.', 'success_message': 'Lozinka uspjesno promijenjena.', 'request_new_link': 'Zatrazite novi link'}
    elif lang == 'en':
        translations = {'title': 'New Password', 'password_label': 'New Password', 'password_confirm_label': 'Confirm Password', 'submit': 'Set New Password', 'error_invalid_link': 'The reset link is invalid or expired.', 'error_password_mismatch': 'Passwords do not match.', 'error_password_short': 'Password must be at least 8 characters.', 'error_password_weak': 'Password must contain letters and numbers.', 'success_message': 'Password successfully changed.', 'request_new_link': 'Request a new link'}
    else:
        translations = {'title': 'Neues Passwort', 'password_label': 'Neues Passwort', 'password_confirm_label': 'Passwort bestaetigen', 'submit': 'Neues Passwort festlegen', 'error_invalid_link': 'Der Reset-Link ist ungueltig oder abgelaufen.', 'error_password_mismatch': 'Die Passwoerter stimmen nicht ueberein.', 'error_password_short': 'Mindestens 8 Zeichen erforderlich.', 'error_password_weak': 'Buchstaben und Zahlen erforderlich.', 'success_message': 'Passwort erfolgreich geaendert.', 'request_new_link': 'Neuen Link anfordern'}
    
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is None or not password_reset_token.check_token(user, token):
        messages.error(request, translations['error_invalid_link'])
        return render(request, 'account/password_reset_invalid.html', {'lang': lang, **translations})
    
    if request.method == 'POST':
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        if password != password_confirm:
            messages.error(request, translations['error_password_mismatch'])
            return render(request, 'account/password_reset_confirm.html', {'lang': lang, 'valid_link': True, **translations})
        if len(password) < 8:
            messages.error(request, translations['error_password_short'])
            return render(request, 'account/password_reset_confirm.html', {'lang': lang, 'valid_link': True, **translations})
        if not (any(c.isalpha() for c in password) and any(c.isdigit() for c in password)):
            messages.error(request, translations['error_password_weak'])
            return render(request, 'account/password_reset_confirm.html', {'lang': lang, 'valid_link': True, **translations})
        
        user.set_password(password)
        user.save()
        messages.success(request, translations['success_message'])
        return redirect('account:password_reset_complete')
    
    return render(request, 'account/password_reset_confirm.html', {'lang': lang, 'valid_link': True, **translations})


def password_reset_complete(request):
    lang = request.session.get('site_language', 'ge')
    if lang == 'hr':
        translations = {'title': 'Lozinka promijenjena', 'message': 'Vasa lozinka je uspjesno promijenjena.', 'login_now': 'Sada se mozete prijaviti.', 'login_button': 'Prijava'}
    elif lang == 'en':
        translations = {'title': 'Password Changed', 'message': 'Your password has been successfully changed.', 'login_now': 'You can now log in.', 'login_button': 'Login'}
    else:
        translations = {'title': 'Passwort geaendert', 'message': 'Ihr Passwort wurde erfolgreich geaendert.', 'login_now': 'Sie koennen sich jetzt anmelden.', 'login_button': 'Anmelden'}
    return render(request, 'account/password_reset_complete.html', {'lang': lang, **translations})
