from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid
import json


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
    
    # Updated regions (12 Croatian regions)
    REGIONS = (
        ('istrien', 'Istrien'),
        ('kvarner', 'Kvarner Bucht'),
        ('norddalmatien', 'Norddalmatien'),
        ('mitteldalmatien', 'Mitteldalmatien'),
        ('sueddalmatien', 'Süddalmatien'),
        ('zagreb', 'Stadt Zagreb'),
        ('zagreber_umland', 'Zagreber Umland'),
        ('nordkroatien', 'Nordkroatien (Varaždin & Međimurje)'),
        ('slawonien', 'Slawonien'),
        ('zentralkroatien', 'Zentralkroatien (Karlovac & Sisak)'),
        ('lika', 'Lika'),
        ('gorski_kotar', 'Gorski Kotar'),
    )
    
    # Languages (12 supported languages)
    LANGUAGES = (
        ('de', 'Deutsch'),
        ('en', 'English'),
        ('hr', 'Hrvatski'),
        ('fr', 'Français'),
        ('nl', 'Nederlands'),
        ('pl', 'Polski'),
        ('cz', 'Čeština'),
        ('sk', 'Slovenčina'),
        ('ru', 'Русский'),
        ('gr', 'Ελληνικά'),
        ('sw', 'Svenska'),
        ('no', 'Norsk'),
    )
    
    # Specializations per professional type
    SPEC_REAL_ESTATE_AGENT = (
        ('wohnimmobilien', 'Wohnimmobilien'),
        ('gewerbeimmobilien', 'Gewerbeimmobilien'),
        ('luxusimmobilien', 'Luxusimmobilien'),
        ('grundstuecke', 'Grundstücke'),
        ('ferienimmobilien', 'Ferienimmobilien'),
        ('neubauprojekte', 'Neubauprojekte & Bauträgerobjekte'),
        ('investitionsimmobilien', 'Investitionsimmobilien'),
        ('kaeuferbetreuung', 'Auslands- & Käuferbetreuung'),
        ('projektvermarktung', 'Projektvermarktung'),
        ('immobilienbewertung', 'Immobilienbewertung'),
        ('immobilienverwaltung', 'Immobilienverwaltung'),
    )
    
    SPEC_CONSTRUCTION = (
        ('neubau', 'Neubau'),
        ('sanierung', 'Sanierung & Renovierung'),
        ('umbau', 'Umbau & Erweiterung'),
        ('rohbau', 'Rohbau'),
        ('schluesselfertig', 'Schlüsselfertiges Bauen'),
        ('poolbau', 'Poolbau'),
        ('aussenanlagen', 'Außenanlagen & Erschließung'),
        ('innenausbau', 'Innenausbau'),
        ('dach_fassade', 'Dach- & Fassadenbau'),
        ('betonarbeiten', 'Beton- & Stahlbetonarbeiten'),
        ('hangbebauung', 'Küsten- & Hangbebauung'),
        ('kroatische_normen', 'Bau nach kroatischen Normen'),
    )
    
    SPEC_LAWYER = (
        ('immobilienrecht', 'Immobilienrecht'),
        ('baurecht', 'Baurecht & Raumordnungsrecht'),
        ('gesellschaftsrecht', 'Gesellschaftsrecht'),
        ('steuerrecht', 'Steuerrecht'),
        ('erbrecht', 'Erbrecht & Nachlassplanung'),
        ('familienrecht', 'Familienrecht'),
        ('einwanderungsrecht', 'Einwanderungs- & Aufenthaltsrecht'),
        ('vertragsrecht', 'Vertragsrecht'),
        ('verwaltungsrecht', 'Verwaltungsrecht'),
        ('grundbuchrecht', 'Grundbuch- & Katasterrecht'),
        ('due_diligence', 'Due-Diligence-Prüfungen'),
        ('behoerdenvertretung', 'Vertretung vor Behörden & Gerichten'),
    )
    
    SPEC_TAX_ADVISOR = (
        ('einkommensteuer', 'Einkommensteuer'),
        ('unternehmensbesteuerung', 'Unternehmensbesteuerung'),
        ('immobilienbesteuerung', 'Immobilienbesteuerung'),
        ('internationale_steuern', 'Internationale Steuerberatung'),
        ('buchhaltung', 'Buchhaltung & Jahresabschlüsse'),
        ('mehrwertsteuer', 'Mehrwertsteuer (PDV)'),
        ('steueroptimierung', 'Steueroptimierung für Investoren'),
        ('grenzueberschreitend', 'Grenzüberschreitende Strukturen'),
        ('selbststaendige', 'Selbstständige & Freiberufler'),
        ('steuervertretung', 'Steuerliche Vertretung'),
        ('ferienvermietung', 'Ferienvermietung & Tourismusbesteuerung'),
    )
    
    SPEC_ARCHITECT = (
        ('wohnbau', 'Wohnbau'),
        ('gewerbebau', 'Gewerbe- & Tourismusbau'),
        ('innenarchitektur', 'Innenarchitektur'),
        ('landschaftsarchitektur', 'Landschaftsarchitektur'),
        ('sanierung_denkmal', 'Sanierung & Denkmalpflege'),
        ('energieeffizient', 'Energieeffizientes Bauen'),
        ('genehmigungsplanung', 'Genehmigungs- & Einreichplanung'),
        ('ausfuehrungsplanung', 'Ausführungsplanung'),
        ('3d_visualisierung', '3D-Planung & Visualisierung'),
        ('raumordnung', 'Raumordnungs- & Bebauungsberatung'),
        ('kuestenplanung', 'Küsten- & Zonenplanung'),
        ('nachhaltiges_bauen', 'Nachhaltiges & ökologisches Bauen'),
    )
    
    # Time choices for opening hours (30 min intervals)
    TIME_CHOICES = (
        ('', '-- Uhrzeit --'),
        ('06:00', '06:00'), ('06:30', '06:30'),
        ('07:00', '07:00'), ('07:30', '07:30'),
        ('08:00', '08:00'), ('08:30', '08:30'),
        ('09:00', '09:00'), ('09:30', '09:30'),
        ('10:00', '10:00'), ('10:30', '10:30'),
        ('11:00', '11:00'), ('11:30', '11:30'),
        ('12:00', '12:00'), ('12:30', '12:30'),
        ('13:00', '13:00'), ('13:30', '13:30'),
        ('14:00', '14:00'), ('14:30', '14:30'),
        ('15:00', '15:00'), ('15:30', '15:30'),
        ('16:00', '16:00'), ('16:30', '16:30'),
        ('17:00', '17:00'), ('17:30', '17:30'),
        ('18:00', '18:00'), ('18:30', '18:30'),
        ('19:00', '19:00'), ('19:30', '19:30'),
        ('20:00', '20:00'), ('20:30', '20:30'),
        ('21:00', '21:00'), ('21:30', '21:30'),
        ('22:00', '22:00'),
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
    service_regions = models.JSONField(default=list, blank=True, verbose_name="Serviceregionen (Mehrfachauswahl)")
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


class ReferenceProject(models.Model):
    """
    Reference projects/portfolio for professionals.
    Allows showcasing completed projects with images.
    """
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='reference_projects')
    
    # Project info
    title = models.CharField(max_length=200, verbose_name="Projekttitel")
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung")
    year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Jahr")
    location = models.CharField(max_length=200, blank=True, null=True, verbose_name="Standort")
    project_type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Projektart")
    
    # Images (up to 6)
    image_1 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    image_6 = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    
    # Ordering
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sortierreihenfolge")
    is_featured = models.BooleanField(default=False, verbose_name="Hervorgehoben")
    
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Referenzprojekt'
        verbose_name_plural = 'Referenzprojekte'
        ordering = ['sort_order', '-year', '-created']
    
    def __str__(self):
        return f"{self.title} ({self.professional.name})"
    
    def get_images(self):
        """Return list of all non-empty images"""
        images = []
        for i in range(1, 7):
            img = getattr(self, f'image_{i}')
            if img:
                images.append(img)
        return images
