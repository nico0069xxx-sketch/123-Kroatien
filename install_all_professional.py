#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===========================================
AGENT-MODEL KONSOLIDIERUNG - KOMPLETT
===========================================

Führe aus in deinem Projekt-Ordner:
cd real-estate-django-ALTmain
python3 install_all_professional.py

Nach dem Ausführen:
python manage.py makemigrations main
python manage.py migrate
"""

import os

# ========================================
# 1. Professional Models
# ========================================
professional_models = '''from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid


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
    is_active = models.BooleanField(default=False, verbose_name="Aktiv")
    is_verified = models.BooleanField(default=False, verbose_name="Verifiziert")
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
    LANGUAGES = (('de', 'Deutsch'), ('hr', 'Hrvatski'))
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
'''

# ========================================
# 2. Professional Forms
# ========================================
professional_forms = '''from django import forms
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
        'professional_types': {'real_estate_agent': 'Immobilienmakler', 'construction_company': 'Bauunternehmen', 'lawyer': 'Rechtsanwalt', 'tax_advisor': 'Steuerberater', 'architect': 'Architekt'},
        'regions': {'istrien': 'Istrien', 'kvarner': 'Kvarner', 'dalmatien': 'Dalmatien', 'zagreb': 'Zagreb', 'slavonien': 'Slavonien', 'andere': 'Andere'},
        'document_types': {'business_license': 'Gewerbeschein', 'id_document': 'Personalausweis/Reisepass', 'company_register': 'Handelsregisterauszug', 'other': 'Sonstiges'},
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
        'professional_types': {'real_estate_agent': 'Agent za nekretnine', 'construction_company': 'Građevinska tvrtka', 'lawyer': 'Odvjetnik', 'tax_advisor': 'Porezni savjetnik', 'architect': 'Arhitekt'},
        'regions': {'istrien': 'Istra', 'kvarner': 'Kvarner', 'dalmatien': 'Dalmacija', 'zagreb': 'Zagreb', 'slavonien': 'Slavonija', 'andere': 'Ostalo'},
        'document_types': {'business_license': 'Obrtnica', 'id_document': 'Osobna iskaznica/Putovnica', 'company_register': 'Izvadak iz sudskog registra', 'other': 'Ostalo'},
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
        for field_name in ['professional_type', 'name', 'email', 'phone', 'mobile', 'city', 'region', 'address', 'company_name', 'oib_number', 'website', 'description', 'languages', 'profile_image', 'company_logo']:
            if field_name in labels:
                self.fields[field_name].label = labels[field_name]
        type_labels = labels['professional_types']
        self.fields['professional_type'].choices = [(k, type_labels.get(k, v)) for k, v in Professional.PROFESSIONAL_TYPES]
        region_labels = labels['regions']
        self.fields['region'].choices = [('', '---')] + [(k, region_labels.get(k, v)) for k, v in Professional.REGIONS]
        self.fields['document'].label = labels['document']
        self.fields['document_type'].label = labels['document_type']
        doc_labels = labels['document_types']
        self.fields['document_type'].choices = [(k, doc_labels.get(k, v)) for k, v in ProfessionalDocument.DOCUMENT_TYPES]
    
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

# ========================================
# 3. Admin
# ========================================
admin_content = '''from django.contrib import admin
from django.contrib import messages
from .professional_models import Professional, ProfessionalContent, ProfessionalDocument

class ProfessionalContentInline(admin.TabularInline):
    model = ProfessionalContent
    extra = 0
    fields = ['language', 'about_text', 'services_text']

class ProfessionalDocumentInline(admin.TabularInline):
    model = ProfessionalDocument
    extra = 0
    fields = ['document_type', 'file', 'is_verified', 'uploaded_at']
    readonly_fields = ['uploaded_at']

@admin.action(description="Ausgewählte Dienstleister aktivieren")
def activate_professionals(modeladmin, request, queryset):
    count = queryset.update(is_active=True)
    messages.success(request, f"{count} Dienstleister aktiviert.")

@admin.action(description="Ausgewählte Dienstleister verifizieren")
def verify_professionals(modeladmin, request, queryset):
    count = queryset.update(is_verified=True, is_active=True)
    messages.success(request, f"{count} Dienstleister verifiziert und aktiviert.")

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    list_display = ['name', 'professional_type', 'city', 'region', 'is_active', 'is_verified', 'created']
    list_display_links = ['name']
    list_editable = ['is_active', 'is_verified']
    list_filter = ['professional_type', 'region', 'is_active', 'is_verified']
    search_fields = ['name', 'email', 'company_name', 'city']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['id', 'created', 'updated']
    actions = [activate_professionals, verify_professionals]
    fieldsets = (
        ('Grunddaten', {'fields': ('professional_type', 'name', 'slug', 'user')}),
        ('Kontakt', {'fields': ('email', 'phone', 'mobile', 'fax', 'website')}),
        ('Standort', {'fields': ('city', 'region', 'address', 'country')}),
        ('Firma', {'fields': ('company_name', 'oib_number', 'company_logo', 'profile_image', 'portrait_photo')}),
        ('Beschreibungen', {'fields': ('description', 'description_de', 'description_hr', 'languages')}),
        ('Social Media', {'fields': ('facebook', 'instagram', 'linkedin', 'twitter', 'youtube'), 'classes': ('collapse',)}),
        ('Status', {'fields': ('is_active', 'is_verified')}),
        ('System', {'fields': ('id', 'created', 'updated'), 'classes': ('collapse',)}),
    )
    inlines = [ProfessionalContentInline, ProfessionalDocumentInline]

@admin.register(ProfessionalContent)
class ProfessionalContentAdmin(admin.ModelAdmin):
    list_display = ['professional', 'language', 'updated']
    list_filter = ['language']
    search_fields = ['professional__name']

@admin.register(ProfessionalDocument)
class ProfessionalDocumentAdmin(admin.ModelAdmin):
    list_display = ['professional', 'document_type', 'is_verified', 'uploaded_at']
    list_filter = ['document_type', 'is_verified']
    list_editable = ['is_verified']
    search_fields = ['professional__name']
'''

# ========================================
# Dateien schreiben
# ========================================
files = {
    'main/professional_models.py': professional_models,
    'main/professional_forms.py': professional_forms,
    'main/admin.py': admin_content,
}

print("=" * 50)
print("AGENT-MODEL KONSOLIDIERUNG")
print("=" * 50)

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {filepath}")

print()
print("=" * 50)
print("NÄCHSTE SCHRITTE:")
print("=" * 50)
print()
print("1. Migration erstellen:")
print("   python manage.py makemigrations main")
print()
print("2. Migration ausführen:")
print("   python manage.py migrate")
print()
print("3. Server starten und testen:")
print("   python manage.py runserver")
print()
print("4. Admin-Panel öffnen:")
print("   http://127.0.0.1:8000/admin/main/professional/")
print()
