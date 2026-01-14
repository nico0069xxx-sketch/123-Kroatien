from django.db import models
import uuid
from django.contrib.auth.models import User

# Kroatische Regionen
REGIONS = [
    ('istrien', 'Istrien'),
    ('kvarner', 'Kvarner'),
    ('dalmatien-nord', 'Nord-Dalmatien'),
    ('dalmatien-mitte', 'Mittel-Dalmatien'),
    ('dalmatien-sued', 'Süd-Dalmatien'),
    ('zagreb', 'Zagreb'),
    ('slavonien', 'Slavonien'),
    ('lika-gorski-kotar', 'Lika & Gorski Kotar'),
]

LANGUAGES_SPOKEN = [
    ('de', 'Deutsch'),
    ('en', 'Englisch'),
    ('hr', 'Kroatisch'),
    ('it', 'Italienisch'),
    ('fr', 'Französisch'),
    ('sl', 'Slowenisch'),
    ('hu', 'Ungarisch'),
]

PROFESSIONAL_TYPES = [
    ('real_estate_agent', 'Immobilienmakler'),
    ('construction_company', 'Bauunternehmen'),
    ('lawyer', 'Rechtsanwalt'),
    ('tax_advisor', 'Steuerberater'),
    ('architect', 'Architekt'),
]


class Professional(models.Model):
    class Meta:
        verbose_name = "Registrierung"
        verbose_name_plural = "Professionals (Registrierungen)"
    # Basis-Model fuer alle Berufsgruppen
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    # Login-Verknuepfung (nur fuer Makler & Bauunternehmen)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='professional_profile')
    has_portal_access = models.BooleanField(default=False, help_text='Zugang zum Makler-Portal')
    
    # Berufsgruppe
    professional_type = models.CharField(max_length=50, choices=PROFESSIONAL_TYPES)
    
    # Basis-Daten (Pflicht)
    name = models.CharField(max_length=200)  # Name oder Firmenname
    email = models.EmailField(max_length=500)
    phone = models.CharField(max_length=50, blank=True, null=True)
    
    # Standort
    city = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=REGIONS)
    address = models.CharField(max_length=300, blank=True, null=True)
    
    # Service-Regionen (ManyToMany über separate Tabelle)
    service_regions = models.CharField(max_length=500, blank=True, null=True)  # Komma-getrennt
    
    # Sprachen (Komma-getrennt)
    languages_spoken = models.CharField(max_length=200)
    
    # Firmen-Daten
    company_name = models.CharField(max_length=200, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    
    # Bilder
    logo = models.ImageField(upload_to='professionals/logos/', blank=True, null=True)
    portrait = models.ImageField(upload_to='professionals/portraits/', blank=True, null=True)
    
    # Verifizierungsdokumente (DSGVO-konform gespeichert)
    id_document = models.FileField(upload_to='professionals/verification/id/', blank=True, null=True, 
                                   help_text='Personalausweis oder Reisepass (PDF/JPG)')
    business_document = models.FileField(upload_to='professionals/verification/business/', blank=True, null=True,
                                         help_text='Handelsregisterauszug, Kammerbescheinigung, etc.')
    verification_notes = models.TextField(blank=True, null=True, 
                                          help_text='Interne Notizen zur Verifizierung')
    verified_by = models.CharField(max_length=100, blank=True, null=True,
                                   help_text='Name des Mitarbeiters der verifiziert hat')
    verification_date = models.DateTimeField(blank=True, null=True)
    
    # Profiltext (vom User gewählt oder selbst geschrieben)
    profile_text_style = models.CharField(max_length=50, blank=True, null=True,
                                          help_text='Stil des gewählten Profiltextes')
    profile_text_original = models.TextField(blank=True, null=True,
                                             help_text='Originaltext in der Eingabesprache')
    
    # Beschreibungen (3 Sprachen)
    description_de = models.TextField(blank=True, null=True, help_text='Beschreibung Deutsch')
    description_hr = models.TextField(blank=True, null=True, help_text='Beschreibung Kroatisch')
    description_en = models.TextField(blank=True, null=True, help_text='Beschreibung Englisch')
    
    # Spam-Schutz
    failed_attempts = models.IntegerField(default=0)
    blocked_until = models.DateTimeField(blank=True, null=True)
    registration_ip = models.GenericIPAddressField(blank=True, null=True)
    
    # Registrierung/Lizenz
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    oib_number = models.CharField(max_length=20, blank=True, null=True)  # Kroatische Steuernummer
    
    # SEO
    slug = models.SlugField(max_length=200, unique=True)
    
    # Status
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    verified_at = models.DateTimeField(blank=True, null=True)
    
    # TOTP 2FA Felder (optional - Authenticator App)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)
    totp_enabled = models.BooleanField(default=False)
    totp_verified = models.BooleanField(default=False)
    must_setup_2fa = models.BooleanField(default=True, help_text='Muss 2FA bei erstem Login einrichten')
    
    # E-Mail 2FA Felder
    email_2fa_enabled = models.BooleanField(default=True, help_text='2FA per E-Mail aktiviert')
    email_2fa_code = models.CharField(max_length=6, blank=True, null=True)
    email_2fa_code_created = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Registrierung"
        verbose_name_plural = "Professionals"
        ordering = ["-created_at"]
    
    def __str__(self):
        return f"{self.name} ({self.get_professional_type_display()})"


class RealEstateAgentProfile(models.Model):
    """Spezifische Daten für Immobilienmakler"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name="agent_profile")
    
    license_info = models.CharField(max_length=200, blank=True, null=True)
    property_focus = models.CharField(max_length=300, blank=True, null=True)  # z.B. "Villen, Apartments, Grundstücke"
    years_active = models.PositiveIntegerField(blank=True, null=True)
    
    def __str__(self):
        return f"Agent: {self.professional.name}"


class ConstructionCompanyProfile(models.Model):
    """Spezifische Daten für Bauunternehmen"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name="construction_profile")
    
    trade_registration = models.CharField(max_length=200, blank=True, null=True)
    project_types = models.CharField(max_length=500, blank=True, null=True)  # z.B. "Neubauten, Renovierungen, Erweiterungen"
    
    def __str__(self):
        return f"Construction: {self.professional.name}"


class LawyerProfile(models.Model):
    """Spezifische Daten für Rechtsanwälte"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name="lawyer_profile")
    
    law_firm = models.CharField(max_length=200, blank=True, null=True)
    bar_registration = models.CharField(max_length=200, blank=True, null=True)
    practice_areas = models.CharField(max_length=500, blank=True, null=True)  # z.B. "Immobilienrecht, Vertragsrecht"
    
    def __str__(self):
        return f"Lawyer: {self.professional.name}"


class TaxAdvisorProfile(models.Model):
    """Spezifische Daten für Steuerberater"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name="tax_profile")
    
    firm_name = models.CharField(max_length=200, blank=True, null=True)
    professional_registration = models.CharField(max_length=200, blank=True, null=True)
    core_services = models.CharField(max_length=500, blank=True, null=True)
    
    def __str__(self):
        return f"Tax Advisor: {self.professional.name}"


class ArchitectProfile(models.Model):
    """Spezifische Daten für Architekten"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name="architect_profile")
    
    office_name = models.CharField(max_length=200, blank=True, null=True)
    chamber_registration = models.CharField(max_length=200, blank=True, null=True)
    planning_focus = models.CharField(max_length=500, blank=True, null=True)  # z.B. "Wohnbau, Gewerbebau, Sanierung"
    
    def __str__(self):
        return f"Architect: {self.professional.name}"


class ProfessionalContent(models.Model):
    """Mehrsprachige Profil-Inhalte (generiert)"""
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name="contents")
    language = models.CharField(max_length=5)  # ge, en, hr, fr, etc.
    
    # Generierter Content
    profile_summary = models.TextField(blank=True, null=True)
    areas_of_activity = models.TextField(blank=True, null=True)  # Als JSON oder Bullet-Points
    typical_situations = models.TextField(blank=True, null=True)
    working_approach = models.TextField(blank=True, null=True)
    faq_content = models.TextField(blank=True, null=True)  # FAQ als JSON
    
    # SEO
    meta_title = models.CharField(max_length=200, blank=True, null=True)
    meta_description = models.CharField(max_length=300, blank=True, null=True)
    
    # Verifizierungs-Statement
    verification_statement = models.TextField(blank=True, null=True)
    
    # Timestamps
    generated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ["professional", "language"]
        verbose_name = "Professional Content"
        verbose_name_plural = "Professional Contents"
    
    def __str__(self):
        return f"{self.professional.name} - {self.language}"
