from django.contrib import admin
from django.contrib import messages
from .professional_models import Professional, ProfessionalContent, ProfessionalDocument

# Import Glossar Admin
from .glossary_admin import *


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
        ('Grunddaten', {
            'fields': ('professional_type', 'name', 'slug', 'user')
        }),
        ('Kontakt', {
            'fields': ('email', 'phone', 'mobile', 'fax', 'website')
        }),
        ('Standort', {
            'fields': ('city', 'region', 'address', 'country')
        }),
        ('Firma', {
            'fields': ('company_name', 'oib_number', 'company_logo', 'profile_image', 'portrait_photo')
        }),
        ('Beschreibungen', {
            'fields': ('description', 'description_de', 'description_hr', 'languages')
        }),
        ('Social Media', {
            'fields': ('facebook', 'instagram', 'linkedin', 'twitter', 'youtube'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active', 'is_verified')
        }),
        ('System', {
            'fields': ('id', 'created', 'updated'),
            'classes': ('collapse',)
        }),
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
