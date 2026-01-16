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
        elif obj.id_document or obj.business_document:
            return format_html('<span style="background:#c9a227;color:white;padding:4px 12px;border-radius:4px;font-weight:bold;">PRUEFEN</span>')
        else:
            return format_html('<span style="background:#8b0000;color:white;padding:4px 12px;border-radius:4px;font-weight:bold;">NEU</span>')
    
    @admin.display(description='Dokumente')
    def dokumente_vorhanden(self, obj):
        hat_ausweis = 'Ja' if obj.id_document else 'Nein'
        hat_gewerbe = 'Ja' if obj.business_document else 'Nein'
        farbe_a = '#1a5c1a' if obj.id_document else '#999'
        farbe_g = '#1a5c1a' if obj.business_document else '#999'
        return format_html(
            '<span style="color:{}">Ausweis: {}</span> | <span style="color:{}">Gewerbe: {}</span>',
            farbe_a, hat_ausweis, farbe_g, hat_gewerbe
        )
    
    @admin.display(description='Registriert am')
    def datum(self, obj):
        return obj.created.strftime('%d.%m.%Y')
    
    fieldsets = (
        ('STATUS', {
            'fields': (
                ('is_verified', 'is_active'),
                'verification_notes',
            ),
        }),
        ('DOKUMENTE', {
            'fields': (
                'dokumente_vorschau',
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
    
    readonly_fields = ['dokumente_vorschau', 'created']
    
    @admin.display(description='')
    def dokumente_vorschau(self, obj):
        html = '<div style="display:flex;gap:30px;flex-wrap:wrap;">'
        
        html += '<div style="flex:1;min-width:300px;">'
        html += '<h3 style="color:#1a5c1a;margin-bottom:10px;">Ausweis / Reisepass</h3>'
        if obj.id_document:
            url = obj.id_document.url
            if url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                html += f'<a href="{url}" target="_blank"><img src="{url}" style="max-width:350px;border:2px solid #1a5c1a;border-radius:8px;"></a>'
            else:
                html += f'<a href="{url}" target="_blank" style="display:inline-block;background:#1a5c1a;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">Dokument oeffnen</a>'
        else:
            html += '<span style="color:#8b0000;font-weight:bold;">Nicht hochgeladen</span>'
        html += '</div>'
        
        html += '<div style="flex:1;min-width:300px;">'
        html += '<h3 style="color:#1a5c1a;margin-bottom:10px;">Gewerbeschein / Lizenz</h3>'
        if obj.business_document:
            url = obj.business_document.url
            if url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                html += f'<a href="{url}" target="_blank"><img src="{url}" style="max-width:350px;border:2px solid #1a5c1a;border-radius:8px;"></a>'
            else:
                html += f'<a href="{url}" target="_blank" style="display:inline-block;background:#1a5c1a;color:white;padding:10px 20px;border-radius:5px;text-decoration:none;">Dokument oeffnen</a>'
        else:
            html += '<span style="color:#8b0000;font-weight:bold;">Nicht hochgeladen</span>'
        html += '</div>'
        
        html += '</div>'
        return format_html(html)


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

