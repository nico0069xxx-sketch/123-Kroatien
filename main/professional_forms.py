from django import forms
from .professional_models import Professional, ProfessionalDocument


# Form labels in German and Croatian
FORM_LABELS = {
    'ge': {
        'title': 'Dienstleister-Registrierung',
        'subtitle': 'Registrieren Sie sich als kroatischer Dienstleister',
        'professional_type': 'Art des Dienstleisters',
        'name': 'Name / Firmenname',
        'email': 'E-Mail-Adresse',
        'phone': 'Telefon',
        'mobile': 'Mobil',
        'city': 'Stadt',
        'region': 'Region',
        'service_regions': 'Service-Regionen',
        'address': 'Adresse',
        'company_name': 'Firmenname',
        'oib_number': 'OIB-Nummer (kroatische Steuernummer)',
        'website': 'Website',
        'description': 'Beschreibung Ihrer Dienstleistungen',
        'spoken_languages': 'Gesprochene Sprachen',
        'specializations': 'Spezialisierungen',
        'profile_image': 'Profilbild (Pflicht)',
        'company_logo': 'Firmenlogo',
        'document': 'Dokument zur Verifizierung (z.B. Ausweis)',
        'document_type': 'Dokumenttyp',
        'opening_hours': 'Öffnungszeiten',
        'submit': 'Registrierung absenden',
        'success_title': 'Registrierung erfolgreich!',
        'success_message': 'Vielen Dank für Ihre Registrierung. Wir werden Ihre Angaben prüfen und Sie per E-Mail benachrichtigen.',
        'required': 'Pflichtfeld',
        'professional_types': {
            'real_estate_agent': 'Immobilienmakler',
            'construction_company': 'Bauunternehmen',
            'lawyer': 'Rechtsanwalt',
            'tax_advisor': 'Steuerberater',
            'architect': 'Architekt',
        },
        'regions': {
            'istrien': 'Istrien',
            'kvarner': 'Kvarner Bucht',
            'norddalmatien': 'Norddalmatien',
            'mitteldalmatien': 'Mitteldalmatien',
            'sueddalmatien': 'Süddalmatien',
            'zagreb': 'Stadt Zagreb',
            'zagreber_umland': 'Zagreber Umland',
            'nordkroatien': 'Nordkroatien',
            'slawonien': 'Slawonien',
            'zentralkroatien': 'Zentralkroatien',
            'lika': 'Lika',
            'gorski_kotar': 'Gorski Kotar',
        },
        'document_types': {
            'business_license': 'Gewerbeschein',
            'id_document': 'Personalausweis/Reisepass',
            'company_register': 'Handelsregisterauszug',
            'other': 'Sonstiges',
        },
        'days': {
            'mo': 'Montag',
            'di': 'Dienstag',
            'mi': 'Mittwoch',
            'do': 'Donnerstag',
            'fr': 'Freitag',
            'sa': 'Samstag',
            'so': 'Sonntag',
        },
    },
    'hr': {
        'title': 'Registracija pružatelja usluga',
        'subtitle': 'Registrirajte se kao hrvatski pružatelj usluga',
        'professional_type': 'Vrsta pružatelja usluga',
        'name': 'Ime / Naziv tvrtke',
        'email': 'E-mail adresa',
        'phone': 'Telefon',
        'mobile': 'Mobitel',
        'city': 'Grad',
        'region': 'Regija',
        'service_regions': 'Servisne regije',
        'address': 'Adresa',
        'company_name': 'Naziv tvrtke',
        'oib_number': 'OIB (osobni identifikacijski broj)',
        'website': 'Web stranica',
        'description': 'Opis vaših usluga',
        'spoken_languages': 'Jezici koje govorite',
        'specializations': 'Specijalizacije',
        'profile_image': 'Profilna slika (obavezno)',
        'company_logo': 'Logo tvrtke',
        'document': 'Dokument za verifikaciju (npr. osobna iskaznica)',
        'document_type': 'Vrsta dokumenta',
        'opening_hours': 'Radno vrijeme',
        'submit': 'Pošalji registraciju',
        'success_title': 'Registracija uspješna!',
        'success_message': 'Hvala vam na registraciji. Provjerit ćemo vaše podatke i obavijestiti vas putem e-maila.',
        'required': 'Obavezno polje',
        'professional_types': {
            'real_estate_agent': 'Agent za nekretnine',
            'construction_company': 'Građevinska tvrtka',
            'lawyer': 'Odvjetnik',
            'tax_advisor': 'Porezni savjetnik',
            'architect': 'Arhitekt',
        },
        'regions': {
            'istrien': 'Istra',
            'kvarner': 'Kvarner',
            'norddalmatien': 'Sjeverna Dalmacija',
            'mitteldalmatien': 'Srednja Dalmacija',
            'sueddalmatien': 'Južna Dalmacija',
            'zagreb': 'Grad Zagreb',
            'zagreber_umland': 'Zagrebačka okolica',
            'nordkroatien': 'Sjeverna Hrvatska',
            'slawonien': 'Slavonija',
            'zentralkroatien': 'Središnja Hrvatska',
            'lika': 'Lika',
            'gorski_kotar': 'Gorski Kotar',
        },
        'document_types': {
            'business_license': 'Obrtnica',
            'id_document': 'Osobna iskaznica/Putovnica',
            'company_register': 'Izvadak iz sudskog registra',
            'other': 'Ostalo',
        },
        'days': {
            'mo': 'Ponedjeljak',
            'di': 'Utorak',
            'mi': 'Srijeda',
            'do': 'Četvrtak',
            'fr': 'Petak',
            'sa': 'Subota',
            'so': 'Nedjelja',
        },
    },
}

# All specializations combined for form choices
ALL_SPECIALIZATIONS = {
    'real_estate_agent': Professional.SPEC_REAL_ESTATE_AGENT,
    'construction_company': Professional.SPEC_CONSTRUCTION,
    'lawyer': Professional.SPEC_LAWYER,
    'tax_advisor': Professional.SPEC_TAX_ADVISOR,
    'architect': Professional.SPEC_ARCHITECT,
}


class ProfessionalRegistrationForm(forms.Form):
    """
    Registration form for professionals with all fields.
    Supports German and Croatian.
    """
    
    # Basic fields
    professional_type = forms.ChoiceField(
        choices=Professional.PROFESSIONAL_TYPES,
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_professional_type'})
    )
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    mobile = forms.CharField(
        max_length=50, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Location
    city = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    region = forms.ChoiceField(
        choices=[('', '---')] + list(Professional.REGIONS),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    service_regions = forms.MultipleChoiceField(
        choices=Professional.REGIONS,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    address = forms.CharField(
        max_length=500, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    # Company
    company_name = forms.CharField(
        max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    oib_number = forms.CharField(
        max_length=20, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'})
    )
    
    # Description
    description = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5})
    )
    
    # Multi-select fields
    spoken_languages = forms.MultipleChoiceField(
        choices=Professional.LANGUAGES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    # Specializations - will be filtered by JavaScript based on professional_type
    specializations = forms.MultipleChoiceField(
        choices=[],  # Set dynamically
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    # Images - profile_image is required
    profile_image = forms.ImageField(
        required=True,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    company_logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    # Document upload
    document = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control', 'accept': '.pdf,.jpg,.jpeg,.png'})
    )
    document_type = forms.ChoiceField(
        choices=[('', '---')] + list(ProfessionalDocument.DOCUMENT_TYPES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    # Opening hours fields (for each day)
    mo_from = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    mo_to = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    mo_closed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    di_from = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    di_to = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    di_closed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    mi_from = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    mi_to = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    mi_closed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    do_from = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    do_to = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    do_closed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    fr_from = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    fr_to = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    fr_closed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    sa_from = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    sa_to = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    sa_closed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    so_from = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    so_to = forms.ChoiceField(choices=Professional.TIME_CHOICES, required=False, widget=forms.Select(attrs={'class': 'form-control form-control-sm'}))
    so_closed = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    
    def __init__(self, *args, lang='ge', **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        labels = FORM_LABELS.get(lang, FORM_LABELS['ge'])
        
        # Apply translated labels
        self.fields['professional_type'].label = labels['professional_type']
        self.fields['name'].label = labels['name']
        self.fields['email'].label = labels['email']
        self.fields['phone'].label = labels['phone']
        self.fields['mobile'].label = labels['mobile']
        self.fields['city'].label = labels['city']
        self.fields['region'].label = labels['region']
        self.fields['service_regions'].label = labels.get('service_regions', 'Service-Regionen')
        self.fields['address'].label = labels['address']
        self.fields['company_name'].label = labels['company_name']
        self.fields['oib_number'].label = labels['oib_number']
        self.fields['website'].label = labels['website']
        self.fields['description'].label = labels['description']
        self.fields['spoken_languages'].label = labels.get('spoken_languages', 'Gesprochene Sprachen')
        self.fields['specializations'].label = labels.get('specializations', 'Spezialisierungen')
        self.fields['profile_image'].label = labels['profile_image']
        self.fields['company_logo'].label = labels['company_logo']
        self.fields['document'].label = labels.get('document', 'Dokument')
        self.fields['document_type'].label = labels.get('document_type', 'Dokumenttyp')
        
        # Translate professional type choices
        type_labels = labels['professional_types']
        self.fields['professional_type'].choices = [
            (key, type_labels.get(key, val))
            for key, val in Professional.PROFESSIONAL_TYPES
        ]
        
        # Translate region choices
        region_labels = labels['regions']
        self.fields['region'].choices = [('', '---')] + [
            (key, region_labels.get(key, val))
            for key, val in Professional.REGIONS
        ]
        self.fields['service_regions'].choices = [
            (key, region_labels.get(key, val))
            for key, val in Professional.REGIONS
        ]
        
        # Combine all specializations for the form
        all_specs = []
        for specs in ALL_SPECIALIZATIONS.values():
            all_specs.extend(specs)
        self.fields['specializations'].choices = list(set(all_specs))
        
        # Document type choices
        doc_labels = labels.get('document_types', {})
        self.fields['document_type'].choices = [('', '---')] + [
            (key, doc_labels.get(key, val))
            for key, val in ProfessionalDocument.DOCUMENT_TYPES
        ]
    
    def get_opening_hours(self):
        """Extract opening hours from form data"""
        d = self.cleaned_data
        days = ['mo', 'di', 'mi', 'do', 'fr', 'sa', 'so']
        opening_hours = {}
        
        for day in days:
            opening_hours[day] = {
                'from': d.get(f'{day}_from', ''),
                'to': d.get(f'{day}_to', ''),
                'closed': d.get(f'{day}_closed', False),
            }
        
        return opening_hours
    
    def save(self):
        """Create Professional instance from cleaned form data"""
        d = self.cleaned_data
        
        # Create professional with all fields
        professional = Professional.objects.create(
            professional_type=d['professional_type'],
            name=d['name'],
            email=d['email'],
            phone=d.get('phone', ''),
            mobile=d.get('mobile', ''),
            city=d['city'],
            region=d.get('region', ''),
            service_regions=d.get('service_regions', []),
            address=d.get('address', ''),
            company_name=d.get('company_name', ''),
            oib_number=d.get('oib_number', ''),
            website=d.get('website', ''),
            description=d.get('description', ''),
            spoken_languages=d.get('spoken_languages', []),
            specializations=d.get('specializations', []),
            profile_image=d.get('profile_image'),
            company_logo=d.get('company_logo'),
            opening_hours=self.get_opening_hours(),
            is_active=False,
        )
        
        # Set description for the registration language
        if self.lang == 'hr':
            professional.description_hr = d.get('description', '')
        else:
            professional.description_de = d.get('description', '')
        professional.save()
        
        # Save document if provided
        document = d.get('document')
        document_type = d.get('document_type')
        if document and document_type:
            ProfessionalDocument.objects.create(
                professional=professional,
                document_type=document_type,
                file=document
            )
        
        return professional
