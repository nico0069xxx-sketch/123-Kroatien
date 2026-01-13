#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Schritt 2: Professional Forms installieren
Führe aus: python3 install_step2_forms.py
"""

content = '''from django import forms
from .professional_models import Professional, ProfessionalDocument


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
        'address': 'Adresse',
        'company_name': 'Firmenname',
        'oib_number': 'OIB-Nummer (kroatische Steuernummer)',
        'website': 'Website',
        'description': 'Beschreibung Ihrer Dienstleistungen',
        'languages': 'Gesprochene Sprachen',
        'profile_image': 'Profilbild',
        'company_logo': 'Firmenlogo',
        'document': 'Dokument zur Verifizierung',
        'document_type': 'Dokumenttyp',
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
            'kvarner': 'Kvarner',
            'dalmatien': 'Dalmatien',
            'zagreb': 'Zagreb',
            'slavonien': 'Slavonien',
            'andere': 'Andere',
        },
        'document_types': {
            'business_license': 'Gewerbeschein',
            'id_document': 'Personalausweis/Reisepass',
            'company_register': 'Handelsregisterauszug',
            'other': 'Sonstiges',
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
        'address': 'Adresa',
        'company_name': 'Naziv tvrtke',
        'oib_number': 'OIB (osobni identifikacijski broj)',
        'website': 'Web stranica',
        'description': 'Opis vaših usluga',
        'languages': 'Jezici koje govorite',
        'profile_image': 'Profilna slika',
        'company_logo': 'Logo tvrtke',
        'document': 'Dokument za verifikaciju',
        'document_type': 'Vrsta dokumenta',
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
            'dalmatien': 'Dalmacija',
            'zagreb': 'Zagreb',
            'slavonien': 'Slavonija',
            'andere': 'Ostalo',
        },
        'document_types': {
            'business_license': 'Obrtnica',
            'id_document': 'Osobna iskaznica/Putovnica',
            'company_register': 'Izvadak iz sudskog registra',
            'other': 'Ostalo',
        },
    },
}


class ProfessionalRegistrationForm(forms.ModelForm):
    document = forms.FileField(required=False)
    document_type = forms.ChoiceField(choices=ProfessionalDocument.DOCUMENT_TYPES, required=False)
    
    class Meta:
        model = Professional
        fields = ['professional_type', 'name', 'email', 'phone', 'mobile', 'city', 'region', 'address', 'company_name', 'oib_number', 'website', 'description', 'languages', 'profile_image', 'company_logo']
        widgets = {
            'professional_type': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'oib_number': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'languages': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'z.B. Deutsch, Kroatisch, Englisch'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, lang='ge', **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        labels = FORM_LABELS.get(lang, FORM_LABELS['ge'])
        
        self.fields['professional_type'].label = labels['professional_type']
        self.fields['name'].label = labels['name']
        self.fields['email'].label = labels['email']
        self.fields['phone'].label = labels['phone']
        self.fields['mobile'].label = labels['mobile']
        self.fields['city'].label = labels['city']
        self.fields['region'].label = labels['region']
        self.fields['address'].label = labels['address']
        self.fields['company_name'].label = labels['company_name']
        self.fields['oib_number'].label = labels['oib_number']
        self.fields['website'].label = labels['website']
        self.fields['description'].label = labels['description']
        self.fields['languages'].label = labels['languages']
        self.fields['profile_image'].label = labels['profile_image']
        self.fields['company_logo'].label = labels['company_logo']
        
        type_labels = labels['professional_types']
        self.fields['professional_type'].choices = [(key, type_labels.get(key, val)) for key, val in Professional.PROFESSIONAL_TYPES]
        
        region_labels = labels['regions']
        self.fields['region'].choices = [('', '---')] + [(key, region_labels.get(key, val)) for key, val in Professional.REGIONS]
        
        self.fields['document'].label = labels['document']
        self.fields['document_type'].label = labels['document_type']
        doc_labels = labels['document_types']
        self.fields['document_type'].choices = [(key, doc_labels.get(key, val)) for key, val in ProfessionalDocument.DOCUMENT_TYPES]
    
    def save(self, commit=True):
        professional = super().save(commit=False)
        if self.lang == 'hr':
            professional.description_hr = professional.description
        else:
            professional.description_de = professional.description
        
        if commit:
            professional.save()
            document = self.cleaned_data.get('document')
            document_type = self.cleaned_data.get('document_type')
            if document and document_type:
                ProfessionalDocument.objects.create(professional=professional, document_type=document_type, file=document)
        
        return professional
'''

filepath = 'main/professional_forms.py'
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ {filepath} erstellt!")
