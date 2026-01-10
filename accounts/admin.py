from django.contrib import admin
from django.contrib import messages
from .models import Agent
from .ai_content_generator import generate_all_descriptions


@admin.action(description="KI-Content generieren (12 Sprachen)")
def generate_ai_content(modeladmin, request, queryset):
    """Admin action to generate AI content for selected agents."""
    total_generated = 0
    
    for agent in queryset:
        print(f"\n=== Generating content for: {agent} ===")
        results, success_count = generate_all_descriptions(agent)
        
        # Save results to agent model
        if 'en' in results:
            agent.description_en = results['en']
        if 'de' in results:
            agent.description_de = results['de']
        if 'fr' in results:
            agent.description_fr = results['fr']
        if 'gr' in results:
            agent.description_gr = results['gr']
        if 'hr' in results:
            agent.description_hr = results['hr']
        if 'pl' in results:
            agent.description_pl = results['pl']
        if 'cz' in results:
            agent.description_cz = results['cz']
        if 'ru' in results:
            agent.description_ru = results['ru']
        if 'sw' in results:
            agent.description_sw = results['sw']
        if 'no' in results:
            agent.description_no = results['no']
        if 'sk' in results:
            agent.description_sk = results['sk']
        if 'nl' in results:
            agent.description_nl = results['nl']
        
        agent.save()
        total_generated += success_count
        print(f"=== Done: {success_count}/12 languages for {agent} ===\n")
    
    messages.success(
        request,
        f"KI-Content generiert: {total_generated} Beschreibungen für {queryset.count()} Agent(en)"
    )


class AgentsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'user', 'email', 'is_active', 'created')
    list_display_links = ('first_name', 'last_name', 'user')
    list_editable = ('is_active',)
    search_fields = ('user',)
    list_per_page = 25
    actions = [generate_ai_content]
    
    fieldsets = (
        ('Persönliche Daten', {
            'fields': ('user', 'first_name', 'last_name', 'email', 'gender', 'city', 'country')
        }),
        ('Firma', {
            'fields': ('company_name', 'company_logo', 'portrait_photo', 'oib_number', 'domain')
        }),
        ('Kontakt & Social Media', {
            'fields': ('mobile', 'fax', 'facebook', 'twitter', 'linkedin', 'instagram', 'youtube')
        }),
        ('Bilder', {
            'fields': ('profile_image',)
        }),
        ('Original-Beschreibung', {
            'fields': ('description',)
        }),
        ('KI-generierte Beschreibungen', {
            'classes': ('collapse',),
            'fields': (
                'description_en', 'description_de', 'description_fr', 'description_gr',
                'description_hr', 'description_pl', 'description_cz', 'description_ru',
                'description_sw', 'description_no', 'description_sk', 'description_nl'
            )
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )


# Register your models here.
admin.site.register(Agent, AgentsAdmin)