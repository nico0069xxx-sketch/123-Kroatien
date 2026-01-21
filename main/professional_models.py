from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


class Professional(models.Model):
    """
    Unified model for all Croatian service providers (Branchenbuch)
    """
    
    PROFESSIONAL_TYPES = (
        ('real_estate_agent', 'Immobilienmakler'),
        ('construction_company', 'Bauunternehmen'),
        ('lawyer', 'Rechtsanwalt'),
        ('tax_advisor', 'Steuerberater'),
        ('architect', 'Architekt'),
    )
    
    CAN_POST_PROPERTIES = ['real_estate_agent', 'construction_company']
    
    # 12 Croatian Regions
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
    
    # 12 Languages
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
    
    # Specializations per type
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
    
    # Time choices for opening hours
    TIME_CHOICES = (
        ('', '-- Vrijeme --'),
        ('06:00', '06:00'), ('06:30', '06:30'), ('07:00', '07:00'), ('07:30', '07:30'),
        ('08:00', '08:00'), ('08:30', '08:30'), ('09:00', '09:00'), ('09:30', '09:30'),
        ('10:00', '10:00'), ('10:30', '10:30'), ('11:00', '11:00'), ('11:30', '11:30'),
        ('12:00', '12:00'), ('12:30', '12:30'), ('13:00', '13:00'), ('13:30', '13:30'),
        ('14:00', '14:00'), ('14:30', '14:30'), ('15:00', '15:00'), ('15:30', '15:30'),
        ('16:00', '16:00'), ('16:30', '16:30'), ('17:00', '17:00'), ('17:30', '17:30'),
        ('18:00', '18:00'), ('18:30', '18:30'), ('19:00', '19:00'), ('19:30', '19:30'),
        ('20:00', '20:00'), ('20:30', '20:30'), ('21:00', '21:00'), ('21:30', '21:30'),
        ('22:00', '22:00'),
    )
    
    # Primary key
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='professional')
    
    # REQUIRED FIELDS (Pflichtfelder)
    professional_type = models.CharField(max_length=50, choices=PROFESSIONAL_TYPES, default='real_estate_agent')
    name = models.CharField(max_length=200, verbose_name="Firmenname *")
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    email = models.EmailField(max_length=500, verbose_name="E-Mail *")
    phone = models.CharField(max_length=50, verbose_name="Telefon *")
    city = models.CharField(max_length=200, verbose_name="Stadt *")
    address = models.CharField(max_length=500, verbose_name="Adresse *")
    oib_number = models.CharField(max_length=20, verbose_name="OIB-Nummer * (intern)")
    
    # Multi-select required fields (stored as JSON)
    service_regions = models.JSONField(default=list, verbose_name="Serviceregionen * (mind. 1)")
    spoken_languages = models.JSONField(default=list, verbose_name="Sprachen * (mind. 1)")
    specializations = models.JSONField(default=list, verbose_name="Spezialisierungen * (mind. 1)")
    
    # Images - at least one required
    company_logo = models.ImageField(upload_to='professionals/logos/', blank=True, null=True, verbose_name="Logo")
    profile_image = models.ImageField(upload_to='professionals/profiles/', blank=True, null=True, verbose_name="Profilbild")
    portrait_photo = models.ImageField(upload_to='professionals/portraits/', blank=True, null=True)
    id_document = models.FileField(upload_to='professionals/documents/', blank=True, null=True, verbose_name="Ausweisdokument")
    
    # OPTIONAL FIELDS
    mobile = models.CharField(max_length=50, blank=True, null=True)
    fax = models.CharField(max_length=50, blank=True, null=True)
    region = models.CharField(max_length=50, choices=REGIONS, blank=True, null=True)
    country = models.CharField(max_length=100, default='Kroatien')
    company_name = models.CharField(max_length=200, blank=True, null=True)
    slogan = models.CharField(max_length=300, blank=True, null=True, verbose_name="Slogan/Motto")
    founded_year = models.PositiveIntegerField(blank=True, null=True, verbose_name="Gründungsjahr")
    employee_count = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mitarbeiterzahl")
    website = models.URLField(max_length=500, blank=True, null=True)
    
    # Opening hours (JSON)
    opening_hours = models.JSONField(default=dict, blank=True, verbose_name="Öffnungszeiten")
    
    # Descriptions
    description = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Original)")
    description_de = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Deutsch)")
    description_hr = models.TextField(blank=True, null=True, verbose_name="Beschreibung (Kroatisch)")
    
    # Social Media
    facebook = models.URLField(max_length=500, blank=True, null=True)
    instagram = models.URLField(max_length=500, blank=True, null=True)
    linkedin = models.URLField(max_length=500, blank=True, null=True)
    twitter = models.URLField(max_length=500, blank=True, null=True)
    youtube = models.URLField(max_length=500, blank=True, null=True)
    tiktok = models.URLField(max_length=500, blank=True, null=True)
    
    # Display toggles
    show_references = models.BooleanField(default=True)
    show_contact_form = models.BooleanField(default=True)
    show_listings = models.BooleanField(default=True)
    show_social_media = models.BooleanField(default=True)
    show_team = models.BooleanField(default=False)
    
    # Status
    is_active = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    
    # 2FA
    totp_secret = models.CharField(max_length=32, blank=True, null=True)
    totp_enabled = models.BooleanField(default=False)
    totp_verified = models.BooleanField(default=False)
    must_setup_2fa = models.BooleanField(default=True)
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
        return self.professional_type in self.CAN_POST_PROPERTIES
    
    def get_description_for_language(self, lang):
        if lang == 'hr':
            return self.description_hr or self.description_de or self.description
        return self.description_de or self.description
    
    def get_specialization_choices(self):
        spec_map = {
            'real_estate_agent': self.SPEC_REAL_ESTATE_AGENT,
            'construction_company': self.SPEC_CONSTRUCTION,
            'lawyer': self.SPEC_LAWYER,
            'tax_advisor': self.SPEC_TAX_ADVISOR,
            'architect': self.SPEC_ARCHITECT,
        }
        return spec_map.get(self.professional_type, ())
    
    def get_specializations_display(self):
        if not self.specializations:
            return []
        choices = dict(self.get_specialization_choices())
        return [choices.get(spec, spec) for spec in self.specializations]
    
    def get_spoken_languages_display(self):
        if not self.spoken_languages:
            return []
        lang_dict = dict(self.LANGUAGES)
        return [lang_dict.get(lang, lang) for lang in self.spoken_languages]
    
    def get_service_regions_display(self):
        if not self.service_regions:
            return []
        region_dict = dict(self.REGIONS)
        return [region_dict.get(reg, reg) for reg in self.service_regions]
    
    def get_opening_hours_display(self):
        if not self.opening_hours:
            return {}
        days = ['Montag', 'Dienstag', 'Mittwoch', 'Donnerstag', 'Freitag', 'Samstag', 'Sonntag']
        day_keys = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']
        result = {}
        for day_name, day_key in zip(days, day_keys):
            day_data = self.opening_hours.get(day_key, {})
            if day_data.get('closed'):
                result[day_name] = 'Geschlossen'
            elif day_data.get('from') and day_data.get('to'):
                result[day_name] = f"{day_data['from']} - {day_data['to']}"
            else:
                result[day_name] = '-'
        return result
    
    def has_required_image(self):
        """Check if at least logo or profile image exists"""
        return bool(self.company_logo) or bool(self.profile_image)
    
    def is_profile_complete(self):
        """Check if all required fields are filled"""
        return all([
            self.name,
            self.email,
            self.phone,
            self.city,
            self.address,
            self.oib_number,
            len(self.service_regions) >= 1,
            len(self.spoken_languages) >= 1,
            len(self.specializations) >= 1,
            self.has_required_image(),
        ])


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
    
    class Meta:
        unique_together = ('professional', 'language')
        verbose_name = 'Professional Content'
        verbose_name_plural = 'Professional Contents'
    
    def __str__(self):
        return f"{self.professional.name} - {self.get_language_display()}"

class Lead(models.Model):
    STATUS_CHOICES = (
        ('new', 'Neu'),
        ('contacted', 'Kontaktiert'),
        ('closed', 'Abgeschlossen'),
    )
    
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='leads', null=True, blank=True)
    listing = models.ForeignKey('listings.Listing', on_delete=models.SET_NULL, null=True, blank=True, related_name='leads')
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=50, blank=True, null=True)
    message = models.TextField()
    property_reference = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    notes = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_read = models.BooleanField(default=False)

    ip_address = models.GenericIPAddressField(blank=True, null=True)
    source_url = models.URLField(max_length=500, blank=True, null=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Lead von {self.name} - {self.created.strftime('%d.%m.%Y')}"
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f"Lead von {self.name} - {self.created.strftime('%d.%m.%Y')}"


# Reference projects for professionals
class ReferenceProject(models.Model):
    professional = models.ForeignKey(Professional, on_delete=models.CASCADE, related_name='reference_projects')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='professionals/references/', blank=True, null=True)
    year = models.PositiveIntegerField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-year', '-created']
    
    def __str__(self):
        return f"{self.title} - {self.professional.name}"


# Backward compatibility aliases
RealEstateAgentProfile = Professional
ConstructionCompanyProfile = Professional
LawyerProfile = Professional
TaxAdvisorProfile = Professional
ArchitectProfile = Professional

# Export constants at module level
REGIONS = Professional.REGIONS
PROFESSIONAL_TYPES = Professional.PROFESSIONAL_TYPES
