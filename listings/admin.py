from django.contrib import admin
from django.contrib import messages
from .models import Listing
from .ai_content_generator import generate_all_listing_content


@admin.action(description="KI-Beschreibung generieren (12 Sprachen)")
def generate_ai_descriptions(modeladmin, request, queryset):
    """Admin action to generate AI descriptions for selected listings."""
    total_success = 0
    
    for listing in queryset:
        print(f"\n=== Generating for: {listing.property_title} ===")
        success_count = generate_all_listing_content(listing)
        total_success += success_count
        print(f"=== Done: {success_count}/12 languages ===\n")
    
    messages.success(
        request,
        f"KI-Beschreibungen generiert: {total_success} Sprachen für {queryset.count()} Immobilie(n)"
    )


class ListingAdmin(admin.ModelAdmin):
    list_display = ('property_title', 'property_type', 'city', 'property_price', 'is_published', 'list_date')
    list_display_links = ('property_title',)
    list_filter = ('property_type', 'property_status', 'city', 'is_published')
    list_editable = ('is_published',)
    search_fields = ('property_title', 'property_description', 'city', 'address')
    list_per_page = 25
    actions = [generate_ai_descriptions]
    
    fieldsets = (
        ('Basis-Informationen', {
            'fields': ('property_title', 'property_description', 'property_type', 'property_status', 'property_price')
        }),
        ('Standort', {
            'fields': ('address', 'city', 'state', 'country', 'zipcode', 'neighborhood', 'location')
        }),
        ('Details', {
            'fields': ('bedrooms', 'bathrooms', 'floors', 'garage', 'area', 'size')
        }),
        ('Medien', {
            'fields': ('photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6', 'video_url')
        }),
        ('Makler', {
            'fields': ('realtor', 'company_name', 'company_logo', 'portrait_photo', 'email', 'domain', 'oib_number')
        }),
        ('KI-generierte Übersetzungen', {
            'classes': ('collapse',),
            'fields': (
                'english_content', 'german_content', 'french_content', 'greek_content',
                'croatian_content', 'polish_content', 'czech_content', 'russian_content',
                'swedish_content', 'norway_content', 'slovak_content', 'dutch_content'
            )
        }),
        ('Status', {
            'fields': ('is_published', 'property_id', 'list_date')
        }),
    )


admin.site.register(Listing, ListingAdmin)

Listing._meta.verbose_name = 'Immobilie'
Listing._meta.verbose_name_plural = 'Immobilien'
