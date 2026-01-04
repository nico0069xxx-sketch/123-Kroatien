# Erweiterte models.py für accounts App
# Fügen Sie diese Änderungen zu Ihrer accounts/models.py hinzu

from django.db import models
from django.contrib.auth.models import User
import uuid

class Agent(models.Model):
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    gender = models.CharField(max_length=200, choices=GENDERS, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='agents/', blank=True, null=True)
    
    # Company data
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_logo = models.ImageField(upload_to='company/', blank=True, null=True)
    portrait_photo = models.ImageField(upload_to='portrait/', blank=True, null=True)
    oib_number = models.CharField(max_length=200, blank=True, null=True)
    domain = models.CharField(max_length=200, blank=True, null=True)

    # Kontakt-Informationen
    mobile = models.CharField(max_length=200, blank=True, null=True)  # WICHTIG: JETZT PFLICHTFELD!
    fax = models.CharField(max_length=200, blank=True, null=True)
    
    # Social Media
    facebook = models.CharField(max_length=200, blank=True, null=True)
    twitter = models.CharField(max_length=200, blank=True, null=True)
    linkedin = models.CharField(max_length=200, blank=True, null=True)
    instagram = models.CharField(max_length=200, blank=True, null=True)
    youtube = models.CharField(max_length=200, blank=True, null=True)

    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        verbose_name_plural = 'Agent'
        verbose_name = 'Agent'
        ordering = ['-created']


class OTPVerification(models.Model):
    """
    OTP-Verifizierung für Email
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


# NEU: SMS-OTP Verifizierung
class SMSOTPVerification(models.Model):
    """
    SMS-OTP-Verifizierung für Telefonnummer
    Zweiter Schritt nach Email-Verifizierung
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=20)
    otp = models.CharField(max_length=6)
    sent_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)  # Anzahl der Versuche
    
    class Meta:
        verbose_name_plural = 'SMS OTP Verifications'
        verbose_name = 'SMS OTP Verification'
        ordering = ['-sent_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.phone_number}"
    
    def is_expired(self):
        """Prüft ob OTP abgelaufen ist (5 Minuten)"""
        from django.utils import timezone
        from datetime import timedelta
        return timezone.now() - self.sent_at > timedelta(minutes=5)
