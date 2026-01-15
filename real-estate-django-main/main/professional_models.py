from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Professional(models.Model):
    """
    Unified model for all Croatian service providers:
    - Immobilienmakler (real_estate_agent) - can post properties
    - Bauunternehmen (construction_company) - can post properties  
    - Rechtsanwälte (lawyer) - directory only
    - Steuerberater (tax_advisor) - directory only
    - Architekten (architect) - directory only
    """
    
    PROFESSIONAL_TYPES = (
        ('real_estate_agent', 'Immobilienmakler'),
        ('construction_company', 'Bauunternehmen'),
        ('lawyer', 'Rechtsanwalt'),
        ('tax_advisor', 'Steuerberater'),
        ('architect', 'Architekt'),
    )
    
    # Types that can post properties (Makler-Portal access)
    CAN_POST_PROPERTIES = ['real_estate_agent', 'construction_company']
    
    REGIONS = (
        ('istrien', 'Istrien'),
        ('kvarner', 'Kvarner'),
        ('dalmatien', 'Dalmatien'),
        ('zagreb', 'Zagreb'),
        ('slavonien', 'Slavonien'),
        ('andere', 'Andere'),
    )
    
    # Primary key
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    
    # User connection (for login - only for Makler & Bauunternehmen)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='professional')
    
    # Basic info
    professional_type = models.CharField(max_length=50, choices=PROFESSIONAL_TYPES, default='real_estate_agent')
    name = models.CharField(max_length=200, verbose_name="Name / Firmenname")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    email = models.EmailField(max_length=500)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    
    # Location
    city = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGIONS, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=100, default='Kroatien')
    
    # Company details
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Firmenname")
    company_logo = models.ImageField(upload_to='professionals/logos/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='professionals/profiles/', blank=True, null=True)
    portrait_photo = models.ImageField(upload_to='professionals/portraits/', blank=True, null=True)
    
    # Extended company info (NEW)
    slogan = models.CharField(max_length=300, blank=True, null=True, verbose_name="Slogan/Motto")
    founded_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Gründungsjahr")
    employee_count = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mitarbeiterzahl")
    specializations = models.TextField(blank=True, null=True, verbose_name="Spezialisierungen")
    
    # Croatian specific
    oib_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="OIB-Nummer")
    website = models.URLField(max_length=500, blank=True, null=True)
    
    # Descriptions (only DE and HR)
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Original)")
    description_de = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Deutsch)")
    description_hr = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Kroatisch)")
    
    # Languages spoken
    languages = models.CharField(max_length=500, blank=True, null=True, verbose_name="Gesprochene Sprachen")
    
    # Social Media (extended)
    facebook = models.URLField(max_length=500, blank=True, null=True)
    instagram = models.URLField(max_length=500, blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    twitter = models.URLField(max_length=500, blank=True, null=True)
    youtube = models.URLField(max_length=500, blank=True, null=True)
    tiktok = models.URLField(max_length=500, blank=True, null=True)
    
    # Display toggles (NEW) - control what's shown on public profile
    show_references = models.BooleanField(default=True, verbose_name="Referenzen anzeigen")
    show_contact_form = models.BooleanField(default=True, verbose_name="Kontaktformular anzeigen")
    show_listings = models.BooleanField(default=True, verbose_name="Immobilien anzeigen")
    show_social_media = models.BooleanField(default=True, verbose_name="Social Media anzeigen")
    show_team = models.BooleanField(default=False, verbose_name="Team anzeigen")
    
    # Status
    is_active = models.BooleanField(default=False, verbose_name="Aktiv")
    is_verified = models.BooleanField(default=False, verbose_name="Verifiziert")
    
    # 2FA - Authenticator App (TOTP)
    totp_secret = models.CharField(max_length=32, blank=True, null=True)
    totp_enabled = models.BooleanField(default=False)
    totp_verified = models.BooleanField(default=False)
    must_setup_2fa = models.BooleanField(default=True)
    
    # 2FA - Email Code
    email_2fa_enabled = models.BooleanField(default=False)
    email_2fa_code = models.CharField(max_length=6, blank=True, null=True)
    email_2fa_code_created = models.DateTimeField(blank=True, null=True)
    
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dienstleister'
        verbose_name_plural = 'Dienstleister'
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.name} ({self.get_professional_type_display()})"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Professional.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
    
    def can_post_properties(self):
        """Check if this professional type can post properties"""
        return self.professional_type in self.CAN_POST_PROPERTIES
    
    def get_description_for_language(self, lang):
        """Get description for specified language (de or hr)"""
        if lang == 'hr':
            return self.description_hr or self.description_de or self.description
        return self.description_de or self.description


class ProfessionalContent(models.Model):
    """
    Extended multilingual content for professionals.
    Used for longer texts like 'about', 'services', 'faq' etc.
    """
    LANGUAGES = (
        ('de', 'Deutsch'),
        ('hr', 'Hrvatski'),
    )
    
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='contents')
    language = models.CharField(max_length=5, choices=LANGUAGES)
    
    # Extended content fields
    about_text = models.TextField(blank=True, null=True, verbose_name="Über uns")
    services_text = models.TextField(blank=True, null=True, verbose_name="Leistungen")
    working_approach = models.TextField(blank=True, null=True, verbose_name="Arbeitsweise")
    faq_text = models.TextField(blank=True, null=True, verbose_name="FAQ")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Dienstleister-Inhalt'
        verbose_name_plural = 'Dienstleister-Inhalte'
        unique_together = ['professional', 'language']
    
    def __str__(self):
        return f"{self.professional.name} - {self.get_language_display()}"


class ProfessionalDocument(models.Model):
    """
    Documents uploaded during registration for verification.
    """
    DOCUMENT_TYPES = (
        ('business_license', 'Gewerbeschein'),
        ('id_document', 'Personalausweis/Reisepass'),
        ('company_register', 'Handelsregisterauszug'),
        ('other', 'Sonstiges'),
    )
    
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=50, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='professionals/documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Dokument'
        verbose_name_plural = 'Dokumente'
    
    def __str__(self):
        return f"{self.professional.name} - {self.get_document_type_display()}"
