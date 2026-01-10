from django.contrib import admin
from main.professional_models import Professional, ProfessionalContent

@admin.register(Professional)
class ProfessionalAdmin(admin.ModelAdmin):
    actions = ['generate_ai_content']

    def generate_ai_content(self, request, queryset):
        from main.ai_content_generator import generate_content_sync
        for prof in queryset:
            results = generate_content_sync(prof)
            success = sum(1 for r in results if r['status'] == 'success')
            self.message_user(request, f'{prof.name}: {success}/12 Sprachen generiert')
    generate_ai_content.short_description = 'KI-Content generieren (12 Sprachen)'

    list_display = ['name', 'professional_type', 'city', 'email', 'is_active', 'is_verified', 'created_at']
    list_filter = ['professional_type', 'is_active', 'is_verified', 'region']
    search_fields = ['name', 'email', 'city']
    list_editable = ['is_active', 'is_verified']
    
    class Meta:
        verbose_name = 'Registrierung'
        verbose_name_plural = 'Registrierungen'

Professional._meta.verbose_name = 'Registrierung'
Professional._meta.verbose_name_plural = 'Registrierungen'

@admin.register(ProfessionalContent)
class ProfessionalContentAdmin(admin.ModelAdmin):
    list_display = ['professional', 'language']
    list_filter = ['language']

ProfessionalContent._meta.verbose_name = 'Professional Inhalt'
ProfessionalContent._meta.verbose_name_plural = 'Professional Inhalte'
