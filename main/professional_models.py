from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

# Konstanten fuer Import
REGIONS = (
    ('istrien', 'Istrien'),
    ('kvarner', 'Kvarner'),
    ('dalmatien', 'Dalmatien'),
    ('zagreb', 'Zagreb'),
    ('slavonien', 'Slavonien'),
    ('andere', 'Andere'),
)

PROFESSIONAL_TYPES = (
    ('real_estate_agent', 'Immobilienmakler'),
    ('construction_company', 'Bauunternehmen'),
    ('lawyer', 'Rechtsanwalt'),
    ('tax_advisor', 'Steuerberater'),
    ('architect', 'Architekt'),
)


class Professional(models.Model):
    PROFESSIONAL_TYPES = (
        ('real_estate_agent', 'Immobilienmakler'),
        ('construction_company', 'Bauunternehmen'),
        ('lawyer', 'Rechtsanwalt'),
        ('tax_advisor', 'Steuerberater'),
        ('architect', 'Architekt'),
    )
    
    CAN_POST_PROPERTIES = ['real_estate_agent', 'construction_company']
    
    REGIONS = (
        ('istrien', 'Istrien'),
        ('kvarner', 'Kvarner'),
        ('dalmatien', 'Dalmatien'),
        ('zagreb', 'Zagreb'),
        ('slavonien', 'Slavonien'),
        ('andere', 'Andere'),
    )
    
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='professional')
    
    professional_type = models.CharField(max_length=50, choices=PROFESSIONAL_TYPES, default='real_estate_agent')
    name = models.CharField(max_length=200, verbose_name="Name / Firmenname")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    email = models.EmailField(max_length=500)
    phone = models.CharField(max_length=50, blank=True, null=True)
    mobile = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    
    city = models.CharField(max_length=200, blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGIONS, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    country = models.CharField(max_length=100, default='Kroatien')
    
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Firmenname")
    company_logo = models.ImageField(upload_to='professionals/logos/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='professionals/profiles/', blank=True, null=True)
    portrait_photo = models.ImageField(upload_to='professionals/portraits/', blank=True, null=True)
    
    # Extended company info (NEW)
    slogan = models.CharField(max_length=300, blank=True, null=True, verbose_name="Slogan/Motto")
    founded_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Gründungsjahr")
    employee_count = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mitarbeiterzahl")
    specializations = models.TextField(blank=True, null=True, verbose_name="Spezialisierungen")
    
    oib_number = models.CharField(max_length=20, blank=True, null=True, verbose_name="OIB-Nummer")
    website = models.URLField(max_length=500, blank=True, null=True)
    
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Original)")
    description_de = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Deutsch)")
    description_hr = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Kroatisch)")
    
    languages = models.CharField(max_length=500, blank=True, null=True, verbose_name="Gesprochene Sprachen")
    
    facebook = models.URLField(max_length=500, blank=True, null=True)
    instagram = models.URLField(max_length=500, blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    twitter = models.URLField(max_length=500, blank=True, null=True)
    youtube = models.URLField(max_length=500, blank=True, null=True)
    tiktok = models.URLField(max_length=500, blank=True, null=True)
    
    # Display toggles
    show_references = models.BooleanField(default=True, verbose_name="Referenzen anzeigen")
    show_contact_form = models.BooleanField(default=True, verbose_name="Kontaktformular anzeigen")
    show_listings = models.BooleanField(default=True, verbose_name="Immobilien anzeigen")
    show_social_media = models.BooleanField(default=True, verbose_name="Social Media anzeigen")
    show_team = models.BooleanField(default=False, verbose_name="Team anzeigen")
    
    is_active = models.BooleanField(default=False, verbose_name="Aktiv")
    is_verified = models.BooleanField(default=False, verbose_name="Verifiziert")
    
    totp_secret = models.CharField(max_length=32, blank=True, null=True)
    totp_enabled = models.BooleanField(default=False)
    totp_verified = models.BooleanField(default=False)
    must_setup_2fa = models.BooleanField(default=True)
    
    email_2fa_enabled = models.BooleanField(default=False)
    email_2fa_code = models.CharField(max_length=6, blank=True, null=True)
    email_2fa_code_created = models.DateTimeField(blank=True, null=True)
    
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
        return self.professional_type in self.CAN_POST_PROPERTIES
    
    def get_description_for_language(self, lang):
        if lang == 'hr':
            return self.description_hr or self.description_de or self.description
        return self.description_de or self.description


class ProfessionalContent(models.Model):
    LANGUAGES = (
        ('de', 'Deutsch'),
        ('hr', 'Hrvatski'),
    )
    
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='contents')
    language = models.CharField(max_length=5, choices=LANGUAGES)
    
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


class ReferenceProject(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='reference_projects')
    
    title = models.CharField(max_length=200, verbose_name="Projekttitel")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Jahr")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Standort")
    project_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Projektart")
    
    image_1 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_6 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sortierreihenfolge")
    is_featured = models.BooleanField(default=False, verbose_name="Hervorgehoben")
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Referenzprojekt'
        verbose_name_plural = 'Referenzprojekte'
        ordering = ['sort_order', '-year', '-created']
    
    def __str__(self):
        return f"{self.title} ({self.professional.name})"
    
    def get_images(self):
        images = []
        for i in range(1, 7):
            img = getattr(self, f'image_{i}')
            if img:
                images.append(img)
        return images



class RealEstateAgentProfile(models.Model):
    """Extended profile for real estate agents"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name='agent_profile')
    license_number = models.CharField(max_length=100, blank=True, null=True)
    years_experience = models.PositiveIntegerField(blank=True, null=True)
    specialties = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Makler-Profil'
        verbose_name_plural = 'Makler-Profile'
    
    def __str__(self):
        return f"Makler-Profil: {self.professional.name}"


class ConstructionCompanyProfile(models.Model):
    """Extended profile for construction companies"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name='construction_profile')
    company_size = models.CharField(max_length=50, blank=True, null=True)
    founded_year = models.PositiveIntegerField(blank=True, null=True)
    certifications = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Bauunternehmen-Profil'
        verbose_name_plural = 'Bauunternehmen-Profile'
    
    def __str__(self):
        return f"Bauunternehmen-Profil: {self.professional.name}"


class LawyerProfile(models.Model):
    """Extended profile for lawyers"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name='lawyer_profile')
    bar_association = models.CharField(max_length=200, blank=True, null=True)
    practice_areas = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Anwalt-Profil'
        verbose_name_plural = 'Anwalt-Profile'
    
    def __str__(self):
        return f"Anwalt-Profil: {self.professional.name}"


class TaxAdvisorProfile(models.Model):
    """Extended profile for tax advisors"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name='tax_advisor_profile')
    certification = models.CharField(max_length=200, blank=True, null=True)
    specializations = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Steuerberater-Profil'
        verbose_name_plural = 'Steuerberater-Profile'
    
    def __str__(self):
        return f"Steuerberater-Profil: {self.professional.name}"


class ArchitectProfile(models.Model):
    """Extended profile for architects"""
    professional = models.OneToOneField(Professional, on_delete=models.CASCADE, related_name='architect_profile')
    chamber_membership = models.CharField(max_length=200, blank=True, null=True)
    portfolio_url = models.URLField(blank=True, null=True)
    design_style = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name = 'Architekt-Profil'
        verbose_name_plural = 'Architekt-Profile'
    
    def __str__(self):
        return f"Architekt-Profil: {self.professional.name}"


class Lead(models.Model):
    """Stores contact form submissions from professional profile pages."""
    STATUS_CHOICES = (
        ('new', 'Neu'),
        ('in_progress', 'In Bearbeitung'),
        ('completed', 'Abgeschlossen'),
        ('spam', 'Spam'),
    )
    
    professional = models.ForeignKey(
        'Professional', 
        on_delete=models.CASCADE, 
        related_name='leads',
        verbose_name="Dienstleister"
    )
    
    name = models.CharField(max_length=200, verbose_name="Name")
    email = models.EmailField(verbose_name="E-Mail")
    phone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Telefon")
    message = models.TextField(verbose_name="Nachricht")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Status")
    source_url = models.URLField(blank=True, null=True, verbose_name="Quell-URL")
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    
    created = models.DateTimeField(auto_now_add=True, verbose_name="Erstellt am")
    updated = models.DateTimeField(auto_now=True, verbose_name="Aktualisiert am")
    
    class Meta:
        verbose_name = 'Anfrage'
        verbose_name_plural = 'Anfragen'
        ordering = ['-created']
    
    def __str__(self):
        return f"Anfrage von {self.name} an {self.professional.name}"
