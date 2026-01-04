# SMS-OTP Service mit Twilio
# Sendet SMS-Codes an Makler für Zwei-Faktor-Authentifizierung

from twilio.rest import Client
from django.conf import settings
import random
import logging

logger = logging.getLogger(__name__)


class SMSService:
    """
    Service für SMS-Versand über Twilio
    """
    
    def __init__(self):
        """Initialisiert Twilio Client mit Credentials aus .env"""
        self.account_sid = settings.TWILIO_ACCOUNT_SID
        self.auth_token = settings.TWILIO_AUTH_TOKEN
        self.from_number = settings.TWILIO_PHONE_NUMBER
        
        # Twilio Client initialisieren
        try:
            self.client = Client(self.account_sid, self.auth_token)
        except Exception as e:
            logger.error(f"Twilio Client konnte nicht initialisiert werden: {e}")
            self.client = None
    
    def generate_otp(self, length=6):
        """
        Generiert einen zufälligen OTP-Code
        
        Args:
            length: Länge des Codes (Standard: 6)
            
        Returns:
            String mit Zahlen-Code
        """
        return ''.join([str(random.randint(0, 9)) for _ in range(length)])
    
    def send_sms_otp(self, phone_number, otp_code, user_name=None):
        """
        Sendet SMS mit OTP-Code an Telefonnummer
        
        Args:
            phone_number: Telefonnummer im Format +385... (Kroatien)
            otp_code: Der zu sendende OTP-Code
            user_name: Optional - Name des Nutzers
            
        Returns:
            dict mit 'success' (bool) und 'message' (str)
        """
        
        # Prüfen ob Twilio konfiguriert ist
        if not self.client:
            logger.error("Twilio Client nicht verfügbar")
            return {
                'success': False,
                'message': 'SMS-Service nicht konfiguriert'
            }
        
        # Telefonnummer validieren
        if not phone_number.startswith('+'):
            phone_number = '+' + phone_number
        
        # SMS-Text erstellen
        if user_name:
            message_body = f"Hallo {user_name},\n\nIhr SMS-Verifizierungscode lautet: {otp_code}\n\nDieser Code ist 5 Minuten gültig.\n\n123-Kroatien Immobilien"
        else:
            message_body = f"Ihr SMS-Verifizierungscode: {otp_code}\n\nGültig für 5 Minuten.\n\n123-Kroatien Immobilien"
        
        try:
            # SMS über Twilio senden
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=phone_number
            )
            
            logger.info(f"SMS erfolgreich gesendet an {phone_number}. Message SID: {message.sid}")
            
            return {
                'success': True,
                'message': 'SMS erfolgreich gesendet',
                'message_sid': message.sid
            }
            
        except Exception as e:
            logger.error(f"Fehler beim SMS-Versand an {phone_number}: {str(e)}")
            
            # Spezifische Fehlerbehandlung
            error_message = 'SMS konnte nicht gesendet werden'
            if 'Invalid' in str(e):
                error_message = 'Ungültige Telefonnummer'
            elif 'Unverified' in str(e):
                error_message = 'Telefonnummer nicht verifiziert (Twilio Test-Modus)'
            
            return {
                'success': False,
                'message': error_message,
                'error': str(e)
            }
    
    def send_registration_sms(self, phone_number, otp_code, user_name):
        """
        Sendet SMS bei Registrierung
        
        Args:
            phone_number: Telefonnummer
            otp_code: OTP-Code
            user_name: Name des Maklers
            
        Returns:
            dict mit Erfolg/Fehler
        """
        message_body = f"Willkommen {user_name}!\n\nIhr SMS-Verifizierungscode: {otp_code}\n\nGültig für 5 Minuten.\n\n123-Kroatien Immobilien"
        
        try:
            if not self.client:
                return {'success': False, 'message': 'SMS-Service nicht konfiguriert'}
            
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=phone_number if phone_number.startswith('+') else '+' + phone_number
            )
            
            return {
                'success': True,
                'message': 'Willkommens-SMS gesendet',
                'message_sid': message.sid
            }
        except Exception as e:
            logger.error(f"Fehler beim Versand der Registrierungs-SMS: {e}")
            return {
                'success': False,
                'message': 'SMS konnte nicht gesendet werden',
                'error': str(e)
            }
    
    def send_login_sms(self, phone_number, otp_code, user_name):
        """
        Sendet SMS bei Login
        
        Args:
            phone_number: Telefonnummer
            otp_code: OTP-Code
            user_name: Name des Maklers
            
        Returns:
            dict mit Erfolg/Fehler
        """
        message_body = f"Login-Verifizierung\n\n{user_name}, Ihr Code: {otp_code}\n\nGültig für 5 Minuten.\n\n123-Kroatien Immobilien"
        
        try:
            if not self.client:
                return {'success': False, 'message': 'SMS-Service nicht konfiguriert'}
            
            message = self.client.messages.create(
                body=message_body,
                from_=self.from_number,
                to=phone_number if phone_number.startswith('+') else '+' + phone_number
            )
            
            return {
                'success': True,
                'message': 'Login-SMS gesendet',
                'message_sid': message.sid
            }
        except Exception as e:
            logger.error(f"Fehler beim Versand der Login-SMS: {e}")
            return {
                'success': False,
                'message': 'SMS konnte nicht gesendet werden',
                'error': str(e)
            }


# Helper-Funktion zum einfachen Zugriff
def send_otp_sms(phone_number, user_name=None):
    """
    Einfache Funktion zum Senden einer SMS mit OTP
    
    Args:
        phone_number: Telefonnummer
        user_name: Optional - Name des Nutzers
        
    Returns:
        tuple (otp_code, result_dict)
    """
    sms_service = SMSService()
    otp_code = sms_service.generate_otp()
    result = sms_service.send_sms_otp(phone_number, otp_code, user_name)
    
    return otp_code, result
