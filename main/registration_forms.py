"""
Mehrstufige Registrierungsformulare für Professionals
Schritt 1: Basisdaten
Schritt 2: Profiltext (8 KI-Vorschläge oder eigener Text)
Schritt 3: Dokumente & Bestätigung
"""
from django import forms
from django.core.validators import FileExtensionValidator
from .professional_models import Professional, REGIONS, PROFESSIONAL_TYPES
from .registration_utils import validate_oib, validate_registration_number, validate_phone_croatia, validate_document


# =============================================================================
# ÜBERSETZUNGEN FÜR ALLE 12 SPRACHEN
# =============================================================================
FORM_TRANSLATIONS = {
    'ge': {
        'step1_title': 'Schritt 1: Basisdaten',
        'step2_title': 'Schritt 2: Profiltext',
        'step3_title': 'Schritt 3: Dokumente & Bestätigung',
        'professional_type': 'Berufsgruppe',
        'name': 'Ihr Name',
        'company_name': 'Firmenname',
        'email': 'E-Mail-Adresse',
        'phone': 'Telefon',
        'city': 'Stadt',
        'region': 'Region',
        'service_regions': 'Tätigkeitsregionen',
        'languages_spoken': 'Gesprochene Sprachen',
        'website': 'Webseite',
        'oib_number': 'OIB-Nummer (Pflicht)',
        'registration_number': 'Berufsregistrierungsnummer',
        'logo': 'Firmenlogo',
        'portrait': 'Profilbild',
        'id_document': 'Personalausweis / Reisepass',
        'business_document': 'Geschäftsdokument',
        'profile_text': 'Profiltext',
        'choose_style': 'Wählen Sie einen Stil:',
        'own_text': 'Eigenen Text schreiben',
        'ki_suggestions': 'KI-Vorschläge',
        'professional_serious': 'Professionell & Seriös',
        'friendly_personal': 'Freundlich & Persönlich',
        'short_concise': 'Kurz & Knapp',
        'detailed': 'Ausführlich & Detailliert',
        'select_this': 'Diesen Text wählen',
        'check_spelling': 'Rechtschreibung prüfen',
        'improve_text': 'Text verbessern',
        'privacy_consent': 'Ich stimme der Verarbeitung meiner Daten zu',
        'terms_consent': 'Ich akzeptiere die AGB',
        'next': 'Weiter',
        'back': 'Zurück',
        'submit': 'Registrierung abschließen',
        'generating': 'KI generiert Vorschläge...',
        'oib_required': 'OIB-Nummer ist erforderlich',
        'reg_required': 'Registrierungsnummer ist für diese Berufsgruppe erforderlich',
        'id_required': 'Ausweisdokument ist erforderlich',
    },
    'en': {
        'step1_title': 'Step 1: Basic Information',
        'step2_title': 'Step 2: Profile Text',
        'step3_title': 'Step 3: Documents & Confirmation',
        'professional_type': 'Professional Type',
        'name': 'Your Name',
        'company_name': 'Company Name',
        'email': 'Email Address',
        'phone': 'Phone',
        'city': 'City',
        'region': 'Region',
        'service_regions': 'Service Regions',
        'languages_spoken': 'Languages Spoken',
        'website': 'Website',
        'oib_number': 'OIB Number (Required)',
        'registration_number': 'Professional Registration Number',
        'logo': 'Company Logo',
        'portrait': 'Profile Picture',
        'id_document': 'ID Card / Passport',
        'business_document': 'Business Document',
        'profile_text': 'Profile Text',
        'choose_style': 'Choose a style:',
        'own_text': 'Write your own text',
        'ki_suggestions': 'AI Suggestions',
        'professional_serious': 'Professional & Serious',
        'friendly_personal': 'Friendly & Personal',
        'short_concise': 'Short & Concise',
        'detailed': 'Detailed & Comprehensive',
        'select_this': 'Select this text',
        'check_spelling': 'Check spelling',
        'improve_text': 'Improve text',
        'privacy_consent': 'I agree to the processing of my data',
        'terms_consent': 'I accept the terms and conditions',
        'next': 'Next',
        'back': 'Back',
        'submit': 'Complete Registration',
        'generating': 'AI generating suggestions...',
        'oib_required': 'OIB number is required',
        'reg_required': 'Registration number is required for this profession',
        'id_required': 'ID document is required',
    },
    'hr': {
        'step1_title': 'Korak 1: Osnovni podaci',
        'step2_title': 'Korak 2: Tekst profila',
        'step3_title': 'Korak 3: Dokumenti i potvrda',
        'professional_type': 'Vrsta profesije',
        'name': 'Vaše ime',
        'company_name': 'Naziv tvrtke',
        'email': 'E-mail adresa',
        'phone': 'Telefon',
        'city': 'Grad',
        'region': 'Regija',
        'service_regions': 'Područja usluga',
        'languages_spoken': 'Jezici',
        'website': 'Web stranica',
        'oib_number': 'OIB broj (obavezno)',
        'registration_number': 'Registracijski broj',
        'logo': 'Logo tvrtke',
        'portrait': 'Profilna slika',
        'id_document': 'Osobna iskaznica / Putovnica',
        'business_document': 'Poslovni dokument',
        'profile_text': 'Tekst profila',
        'choose_style': 'Odaberite stil:',
        'own_text': 'Napišite vlastiti tekst',
        'ki_suggestions': 'AI prijedlozi',
        'professional_serious': 'Profesionalno i ozbiljno',
        'friendly_personal': 'Prijateljski i osobno',
        'short_concise': 'Kratko i jasno',
        'detailed': 'Detaljno i sveobuhvatno',
        'select_this': 'Odaberi ovaj tekst',
        'check_spelling': 'Provjeri pravopis',
        'improve_text': 'Poboljšaj tekst',
        'privacy_consent': 'Pristajem na obradu mojih podataka',
        'terms_consent': 'Prihvaćam uvjete korištenja',
        'next': 'Dalje',
        'back': 'Natrag',
        'submit': 'Završi registraciju',
        'generating': 'AI generira prijedloge...',
        'oib_required': 'OIB broj je obavezan',
        'reg_required': 'Registracijski broj je obavezan za ovu profesiju',
        'id_required': 'Dokument identifikacije je obavezan',
    },
}

# Kopiere Übersetzungen für weitere Sprachen (mit Fallback auf Englisch)
for lang in ['fr', 'nl', 'pl', 'cz', 'sk', 'ru', 'gr', 'sw', 'no']:
    if lang not in FORM_TRANSLATIONS:
        FORM_TRANSLATIONS[lang] = FORM_TRANSLATIONS['en'].copy()


PROFESSIONAL_TYPES_ALL_LANGS = {
    'ge': [
        ('real_estate_agent', 'Immobilienmakler'),
        ('construction_company', 'Bauunternehmen'),
        ('lawyer', 'Rechtsanwalt'),
        ('tax_advisor', 'Steuerberater'),
        ('architect', 'Architekt'),
    ],
    'en': [
        ('real_estate_agent', 'Real Estate Agent'),
        ('construction_company', 'Construction Company'),
        ('lawyer', 'Lawyer'),
        ('tax_advisor', 'Tax Advisor'),
        ('architect', 'Architect'),
    ],
    'hr': [
        ('real_estate_agent', 'Agencija za nekretnine'),
        ('construction_company', 'Građevinska tvrtka'),
        ('lawyer', 'Odvjetnik'),
        ('tax_advisor', 'Porezni savjetnik'),
        ('architect', 'Arhitekt'),
    ],
}

REGIONS_ALL_LANGS = {
    'ge': REGIONS,
    'hr': [
        ('istrien', 'Istra'),
        ('kvarner', 'Kvarner'),
        ('dalmatien-nord', 'Sjeverna Dalmacija'),
        ('dalmatien-mitte', 'Srednja Dalmacija'),
        ('dalmatien-sued', 'Južna Dalmacija'),
        ('zagreb', 'Zagreb'),
        ('slavonien', 'Slavonija'),
        ('lika-gorski-kotar', 'Lika i Gorski Kotar'),
    ],
    'en': REGIONS,
}


# =============================================================================
# SCHRITT 1: BASISDATEN FORMULAR
# =============================================================================
class Step1Form(forms.Form):
    """Basisdaten: Name, Firma, Kontakt, Region"""
    
    professional_type = forms.ChoiceField(choices=PROFESSIONAL_TYPES)
    name = forms.CharField(max_length=200)
    company_name = forms.CharField(max_length=200, required=False)
    email = forms.EmailField()
    phone = forms.CharField(max_length=50)
    city = forms.CharField(max_length=100)
    region = forms.ChoiceField(choices=REGIONS)
    service_regions = forms.MultipleChoiceField(choices=REGIONS, required=False, 
                                                 widget=forms.CheckboxSelectMultiple)
    languages_spoken = forms.CharField(max_length=200, 
                                       help_text='z.B. Deutsch, Englisch, Kroatisch')
    website = forms.URLField(required=False)
    oib_number = forms.CharField(max_length=20)
    registration_number = forms.CharField(max_length=100, required=False)
    logo = forms.ImageField(required=False)
    portrait = forms.ImageField(required=False)
    
    def __init__(self, *args, lang='ge', **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        trans = FORM_TRANSLATIONS.get(lang, FORM_TRANSLATIONS['ge'])
        
        # Übersetzte Choices
        self.fields['professional_type'].choices = PROFESSIONAL_TYPES_ALL_LANGS.get(lang, PROFESSIONAL_TYPES_ALL_LANGS['ge'])
        self.fields['region'].choices = REGIONS_ALL_LANGS.get(lang, REGIONS_ALL_LANGS['ge'])
        self.fields['service_regions'].choices = REGIONS_ALL_LANGS.get(lang, REGIONS_ALL_LANGS['ge'])
        
        # Übersetzte Labels
        for field_name, field in self.fields.items():
            if field_name in trans:
                field.label = trans[field_name]
    
    def clean_oib_number(self):
        oib = self.cleaned_data.get('oib_number')
        is_valid, error = validate_oib(oib)
        if not is_valid:
            raise forms.ValidationError(error)
        return oib
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        is_valid, error = validate_phone_croatia(phone)
        if not is_valid:
            raise forms.ValidationError(error)
        return phone
    
    def clean(self):
        cleaned_data = super().clean()
        prof_type = cleaned_data.get('professional_type')
        reg_number = cleaned_data.get('registration_number')
        
        is_valid, error = validate_registration_number(reg_number, prof_type)
        if not is_valid:
            self.add_error('registration_number', error)
        
        return cleaned_data


# =============================================================================
# SCHRITT 2: PROFILTEXT FORMULAR
# =============================================================================
class Step2Form(forms.Form):
    """Profiltext: KI-Vorschlag wählen oder eigenen Text schreiben"""
    
    text_choice = forms.ChoiceField(
        choices=[
            ('ki_1', 'KI Vorschlag 1'),
            ('ki_2', 'KI Vorschlag 2'),
            ('ki_3', 'KI Vorschlag 3'),
            ('ki_4', 'KI Vorschlag 4'),
            ('ki_5', 'KI Vorschlag 5'),
            ('ki_6', 'KI Vorschlag 6'),
            ('ki_7', 'KI Vorschlag 7'),
            ('ki_8', 'KI Vorschlag 8'),
            ('own', 'Eigener Text'),
        ],
        widget=forms.RadioSelect,
        initial='ki_1'
    )
    
    own_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 6, 'placeholder': 'Schreiben Sie hier Ihren eigenen Profiltext...'}),
        required=False
    )
    
    def __init__(self, *args, lang='ge', **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
    
    def clean(self):
        cleaned_data = super().clean()
        choice = cleaned_data.get('text_choice')
        own_text = cleaned_data.get('own_text')
        
        if choice == 'own' and not own_text:
            self.add_error('own_text', 'Bitte geben Sie einen Text ein oder wählen Sie einen KI-Vorschlag.')
        
        return cleaned_data


# =============================================================================
# SCHRITT 3: DOKUMENTE & BESTÄTIGUNG
# =============================================================================
class Step3Form(forms.Form):
    """Verifizierungsdokumente und Zustimmungen"""
    
    id_document = forms.FileField(
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text='Personalausweis oder Reisepass (PDF, JPG, PNG - max. 10 MB)'
    )
    
    business_document = forms.FileField(
        required=False,
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png'])],
        help_text='Handelsregisterauszug, Kammerbescheinigung, etc.'
    )
    
    privacy_consent = forms.BooleanField(required=True)
    terms_consent = forms.BooleanField(required=True)
    
    def __init__(self, *args, lang='ge', professional_type=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        self.professional_type = professional_type
        trans = FORM_TRANSLATIONS.get(lang, FORM_TRANSLATIONS['ge'])
        
        # Labels übersetzen
        self.fields['id_document'].label = trans.get('id_document', 'ID Document')
        self.fields['business_document'].label = trans.get('business_document', 'Business Document')
        self.fields['privacy_consent'].label = trans.get('privacy_consent', 'Privacy Consent')
        self.fields['terms_consent'].label = trans.get('terms_consent', 'Terms Consent')
        
        # Business-Dokument erforderlich für bestimmte Berufsgruppen
        if professional_type in ['lawyer', 'architect', 'real_estate_agent']:
            self.fields['business_document'].required = True
    
    def clean_id_document(self):
        doc = self.cleaned_data.get('id_document')
        is_valid, error = validate_document(doc)
        if not is_valid:
            raise forms.ValidationError(error)
        return doc
    
    def clean_business_document(self):
        doc = self.cleaned_data.get('business_document')
        if doc:
            is_valid, error = validate_document(doc)
            if not is_valid:
                raise forms.ValidationError(error)
        return doc
