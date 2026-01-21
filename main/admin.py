from django.contrib import admin
from django.utils.html import format_html
from django.utils import timezone
from main.professional_models import Professional, ProfessionalContent


@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    
    list_display = [
        'name', 
        'berufsgruppe',
        'stadt_region',
        'status_anzeige',
        'dokumente_vorhanden',
        'datum',
        'is_active'
    ]
    
    list_filter = [
        'is_verified',
        'professional_type',
                'user',
    ]
    
    search_fields = ['name', 'email', 'city']
    list_per_page = 30
    ordering = ['-created']
    
    actions = ['genehmigen', 'ablehnen']
    
    @admin.action(description='GENEHMIGEN - Profil freischalten')
    def genehmigen(self, request, queryset):
        anzahl = queryset.update(
            is_verified=True,
            is_active=True,
            verified_by='Nik',
            verification_date=timezone.now()
        )
        self.message_user(request, f'{anzahl} Profil(e) wurden freigeschaltet!')
    
    @admin.action(description='ABLEHNEN - Profil sperren')
    def ablehnen(self, request, queryset):
        anzahl = queryset.update(
            is_verified=False,
            is_active=False
        )
        self.message_user(request, f'{anzahl} Profil(e) wurden abgelehnt.')
    
    @admin.display(description='Berufsgruppe')
    def berufsgruppe(self, obj):
        typen = {
            'real_estate_agent': 'Makler',
            'construction_company': 'Bauunternehmen',
            'lawyer': 'Anwalt',
            'tax_advisor': 'Steuerberater',
            'architect': 'Architekt',
        }
        return typen.get(obj.professional_type, obj.professional_type)
    
    @admin.display(description='Ort')
    def stadt_region(self, obj):
        return f"{obj.city}"
    
    @admin.display(description='Status')
    def status_anzeige(self, obj):
        if obj.is_verified and obj.is_active:
            return format_html('<span style="background:#1a5c1a;color:white;padding:4px 12px;border-radius:4px;font-weight:bold;">AKTIV</span>')
        elif obj.id_document:
            return format_html('<span style="background:#c9a227;color:white;padding:4px 12px;border-radius:4px;font-weight:bold;">PRUEFEN</span>')
        else:
            return format_html('<span style="background:#8b0000;color:white;padding:4px 12px;border-radius:4px;font-weight:bold;">NEU</span>')
    
    @admin.display(description='Dokumente')
    def dokumente_vorhanden(self, obj):
        if obj.id_document:
            return format_html('<span style="color:#1a5c1a">✓ Ja</span>')
        return format_html('<span style="color:#999">Nein</span>')
    
    @admin.display(description='Dokumente')
    def dokumente_vorhanden(self, obj):
        count = obj.documents.count()
        if count > 0:
            return format_html('<span style="color:#1a5c1a">Ja ({})</span>', count)
        return format_html('<span style="color:#999">Nein</span>')

    
    @admin.display(description='Registriert am')
    def datum(self, obj):
        return obj.created.strftime('%d.%m.%Y')
    
    fieldsets = (
        ('STATUS', {
            'fields': (
                ('is_verified', 'is_active'),
                'professional_type',
                'user',
            ),
        }),
        ('DOKUMENTE', {
            'fields': (
            ),
        }),
        ('KONTAKT', {
            'fields': (
                'name',
                'email',
                'phone',
                'website',
            ),
        }),
        ('STANDORT', {
            'fields': (
                'city',
                'region',
            ),
        }),
    )
    
    readonly_fields = ['created']
    

@admin.register(ProfessionalContent)
class ProfessionalContentAdmin(admin.ModelAdmin):
    list_display = ['professional', 'language']
    list_filter = ['language']


Professional._meta.verbose_name = 'Registrierung'
Professional._meta.verbose_name_plural = 'Registrierungen'
ProfessionalContent._meta.verbose_name = 'Uebersetzung'
ProfessionalContent._meta.verbose_name_plural = 'Uebersetzungen'

from main.professional_models import Lead

@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'professional', 'status', 'created']
    list_filter = ['status', 'created', 'professional']
    search_fields = ['name', 'email', 'message']
    readonly_fields = ['created', 'updated', 'ip_address', 'source_url']
    ordering = ['-created']

from main.professional_models import Lead

