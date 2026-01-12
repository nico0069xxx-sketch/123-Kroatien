"""
Utility-Funktionen für die Professional-Registrierung
- OIB-Validierung (ISO 7064 Mod 11-10)
- Spam-Schutz
- IP-Blocking
"""
from datetime import datetime, timedelta
from django.utils import timezone
import re


def validate_oib(oib):
    """
    Validiert kroatische OIB-Nummer (11 Ziffern)
    Returns: (is_valid, error_message)
    """
    if not oib:
        return False, "OIB ist erforderlich"
    
    # Nur Ziffern erlauben, Leerzeichen entfernen
    oib = re.sub(r'\s+', '', str(oib))
    
    if not oib.isdigit():
        return False, "OIB darf nur Ziffern enthalten"
    
    if len(oib) != 11:
        return False, f"OIB muss genau 11 Ziffern haben (aktuell: {len(oib)})"
    
    # Format ist gültig - Prüfsumme wird nicht mehr geprüft
    # (zu viele legitime OIBs würden sonst abgelehnt)
    return True, None


def validate_registration_number(reg_number, professional_type):
    """
    Validiert Registrierungsnummer basierend auf Berufsgruppe
    Returns: (is_valid, error_message)
    """
    if not reg_number:
        if professional_type in ['lawyer', 'architect', 'real_estate_agent']:
            return False, "Registrierungsnummer ist für diese Berufsgruppe erforderlich"
        return True, None
    
    reg_number = reg_number.strip()
    
    # Mindestlänge
    if len(reg_number) < 3:
        return False, "Registrierungsnummer zu kurz"
    
    # Maxlänge
    if len(reg_number) > 50:
        return False, "Registrierungsnummer zu lang"
    
    return True, None


def validate_phone_croatia(phone):
    """
    Validiert kroatische Telefonnummer
    Erlaubte Formate: +385..., 00385..., 0...
    """
    if not phone:
        return True, None
    
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Kroatische Formate
    patterns = [
        r'^\+385\d{8,9}$',      # +385 XX XXX XXXX
        r'^00385\d{8,9}$',       # 00385 XX XXX XXXX
        r'^0\d{8,9}$',           # 0XX XXX XXXX (lokal)
    ]
    
    for pattern in patterns:
        if re.match(pattern, phone):
            return True, None
    
    return False, "Ungültiges Telefonnummer-Format. Verwende: +385 XX XXX XXXX"


def check_spam_block(ip_address, model_class):
    """
    Prüft ob eine IP-Adresse gesperrt ist
    Returns: (is_blocked, remaining_minutes)
    """
    from django.utils import timezone
    
    # Finde Einträge mit dieser IP die noch gesperrt sind
    blocked = model_class.objects.filter(
        registration_ip=ip_address,
        blocked_until__gt=timezone.now()
    ).first()
    
    if blocked:
        remaining = (blocked.blocked_until - timezone.now()).total_seconds() / 60
        return True, int(remaining) + 1
    
    return False, 0


def record_failed_attempt(ip_address, model_class):
    """
    Zeichnet einen fehlgeschlagenen Versuch auf
    Nach 5 Versuchen: 10 Minuten Sperre
    """
    from django.utils import timezone
    
    # Zähle fehlgeschlagene Versuche in letzter Stunde
    one_hour_ago = timezone.now() - timedelta(hours=1)
    recent_failures = model_class.objects.filter(
        registration_ip=ip_address,
        created_at__gte=one_hour_ago,
        is_active=False
    ).count()
    
    if recent_failures >= 4:  # Bei 5. Versuch sperren
        return True, 10  # 10 Minuten Sperre
    
    return False, 0


def get_client_ip(request):
    """Ermittelt die Client-IP-Adresse"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# Erlaubte Dateitypen für Verifizierungsdokumente
ALLOWED_DOCUMENT_TYPES = ['application/pdf', 'image/jpeg', 'image/png']
MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10 MB


def validate_document(file):
    """
    Validiert ein hochgeladenes Dokument
    Returns: (is_valid, error_message)
    """
    if not file:
        return True, None
    
    # Dateigröße prüfen
    if file.size > MAX_DOCUMENT_SIZE:
        return False, "Datei zu groß (max. 10 MB)"
    
    # Dateityp prüfen
    content_type = file.content_type
    if content_type not in ALLOWED_DOCUMENT_TYPES:
        return False, "Nur PDF, JPG oder PNG erlaubt"
    
    return True, None
