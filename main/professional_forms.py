from django import forms
from .professional_models import Professional


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
        'profile_image': 'Profilbild',
        'company_logo': 'Firmenlogo',
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
        'profile_image': 'Profilna slika',
        'company_logo': 'Logo tvrtke',
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
    },
}


class ProfessionalRegistrationForm(forms.Form):
    """
    Registration form for professionals.
    Supports German and Croatian.
    """
    
    # Basic fields
    professional_type = forms.ChoiceField(
        choices=Professional.PROFESSIONAL_TYPES,
        widget=forms.Select(attrs={'class': 'form-control'})
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
    
    # Multi-select fields (stored as JSON in model)
    spoken_languages = forms.MultipleChoiceField(
        choices=Professional.LANGUAGES,
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )
    
    # Images
    profile_image = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    company_logo = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
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
        self.fields['profile_image'].label = labels['profile_image']
        self.fields['company_logo'].label = labels['company_logo']
        
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
            profile_image=d.get('profile_image'),
            company_logo=d.get('company_logo'),
            is_active=False,
        )
        
        # Set description for the registration language
        if self.lang == 'hr':
            professional.description_hr = d.get('description', '')
        else:
            professional.description_de = d.get('description', '')
        professional.save()
        
        return professional
