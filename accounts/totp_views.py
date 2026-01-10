import pyotp
import qrcode
import io
import base64
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.utils import timezone
from .models import Agent


@login_required
def setup_2fa(request):
    agent = Agent.objects.filter(user=request.user).first()
    if not agent:
        messages.error(request, "Nur Dienstleister koennen 2FA aktivieren")
        return redirect("main:home")
    if not agent.totp_secret:
        agent.totp_secret = pyotp.random_base32()
        agent.save()
    totp = pyotp.TOTP(agent.totp_secret)
    uri = totp.provisioning_uri(name=agent.email, issuer_name="123-Kroatien.eu")
    qr = qrcode.make(uri)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode()
    return render(request, "account/setup_2fa.html", {"qr_code": qr_base64, "secret": agent.totp_secret, "agent": agent})

@login_required
def verify_2fa_setup(request):
    if request.method != "POST":
        return redirect("account:setup_2fa")
    agent = Agent.objects.filter(user=request.user).first()
    code = request.POST.get("code", "")
    totp = pyotp.TOTP(agent.totp_secret)
    if totp.verify(code):
        agent.totp_enabled = True
        agent.totp_verified = True
        agent.save()
        messages.success(request, "2FA wurde erfolgreich aktiviert!")
        return redirect("main:home")
    else:
        messages.error(request, "Falscher Code. Bitte versuche es erneut.")
        return redirect("account:setup_2fa")

def verify_2fa_login(request):
    user_id = request.session.get("2fa_user_id")
    if not user_id:
        return redirect("account:login")
    if request.method == "POST":
        from django.contrib.auth.models import User
        from django.contrib import auth
        user = User.objects.get(id=user_id)
        agent = Agent.objects.filter(user=user).first()
        code = request.POST.get("code", "")
        totp = pyotp.TOTP(agent.totp_secret)
        if totp.verify(code):
            auth.login(request, user)
            del request.session["2fa_user_id"]
            try:
                send_mail("Login-Benachrichtigung", f"Jemand hat sich in Ihr Konto eingeloggt am {timezone.now()}", "noreply@123-kroatien.eu", [agent.email], fail_silently=True)
            except:
                pass
            messages.success(request, "Erfolgreich eingeloggt!")
            return redirect("main:agent", id=agent.id)
        else:
            messages.error(request, "Falscher Code")
    return render(request, "account/verify_2fa.html")
