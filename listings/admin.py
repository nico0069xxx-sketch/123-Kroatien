from django.contrib import admin
from django.contrib import messages
from django.utils.html import format_html
from django.utils import timezone
from .models import Listing
from .ai_content_generator import generate_all_listing_content
from .validation import validate_listing


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    
    list_display = [
        'property_title', 
        'typ_anzeige',
        'location', 
        'preis_formatiert',
        'status_badge',
        'fehler_status',
        'list_date'
    ]
    
    list_filter = [
        'listing_status',
        'property_type', 
        'property_status',
        'location',
    ]
    
    search_fields = ['property_title', 'property_description', 'city', 'address']
    list_per_page = 30
    ordering = ['-list_date']
    
    actions = ['freigeben', 'ablehnen', 'als_verkauft', 'neu_pruefen', 'generate_ai_descriptions']
    
    @admin.action(description='FREIGEBEN - Online stellen')
    def freigeben(self, request, queryset):
        ok = 0
        fehler_count = 0
        
        for listing in queryset:
            fehler = validate_listing(listing)
            if fehler:
                listing.pruefung_fehler = "\n".join(fehler)
                listing.save()
                fehler_count += 1
            else:
                listing.listing_status = 'aktiv'
                listing.is_published = True
                listing.pruefung_fehler = None
                listing.geprueft_am = timezone.now()
                listing.save()
                ok += 1
        
        if ok:
            messages.success(request, f'{ok} Immobilie(n) freigeschaltet!')
        if fehler_count:
            messages.warning(request, f'{fehler_count} Immobilie(n) haben noch Fehler')
    
    @admin.action(description='ABLEHNEN')
    def ablehnen(self, request, queryset):
        anzahl = queryset.update(listing_status='abgelehnt', is_published=False, geprueft_am=timezone.now())
        messages.success(request, f'{anzahl} abgelehnt')
    
    @admin.action(description='Als VERKAUFT markieren')
    def als_verkauft(self, request, queryset):
        anzahl = queryset.update(listing_status='verkauft', is_published=False)
        messages.success(request, f'{anzahl} als verkauft markiert')
    
    @admin.action(description='Neu pruefen')
    def neu_pruefen(self, request, queryset):
        ok = 0
        fehler_count = 0
        for listing in queryset:
            fehler = validate_listing(listing)
            listing.pruefung_fehler = "\n".join(fehler) if fehler else None
            listing.save()
            if fehler:
                fehler_count += 1
            else:
                ok += 1
        messages.info(request, f'{ok} OK, {fehler_count} mit Fehlern')
    
    @admin.action(description='KI-Beschreibung generieren')
    def generate_ai_descriptions(self, request, queryset):
        total = 0
        for listing in queryset:
            total += generate_all_listing_content(listing)
        messages.success(request, f'{total} Sprachen generiert')
    
    @admin.display(description='Typ')
    def typ_anzeige(self, obj):
        typen = {'House': 'Haus', 'Appartment': 'Wohnung', 'New Building': 'Neubau', 'Property': 'Grundstueck', 'Villa': 'Villa'}
        return typen.get(obj.property_type, obj.property_type or '-')
    
    @admin.display(description='Preis')
    def preis_formatiert(self, obj):
        if obj.property_price:
            return f"{obj.property_price:,.0f} EUR".replace(',', '.')
        return "-"
    
    @admin.display(description='Status')
    def status_badge(self, obj):
        farben = {
            'pruefung': ('#c9a227', 'PRUEFEN'),
            'aktiv': ('#1a5c1a', 'ONLINE'),
            'verkauft': ('#666', 'VERKAUFT'),
            'pausiert': ('#ff9800', 'PAUSIERT'),
            'abgelehnt': ('#8b0000', 'ABGELEHNT'),
        }
        farbe, text = farben.get(obj.listing_status, ('#999', obj.listing_status or 'NEU'))
        return format_html('<span style="background:{};color:white;padding:4px 10px;border-radius:4px;font-weight:bold;font-size:11px;">{}</span>', farbe, text)
    
    @admin.display(description='Fehler')
    def fehler_status(self, obj):
        if obj.pruefung_fehler:
            anzahl = len(obj.pruefung_fehler.split("\n"))
            return format_html('<span style="color:#8b0000;font-weight:bold;">{} Fehler</span>', anzahl)
        return format_html('<span style="color:#1a5c1a;">OK</span>')
    
    fieldsets = (
        ('STATUS', {
            'fields': ('listing_status', 'is_published', 'fehler_anzeige', 'pruefung_notizen'),
        }),
        ('BASISDATEN', {
            'fields': ('property_title', 'property_description', 'property_type', 'property_status', 'property_price'),
        }),
        ('STANDORT', {
            'fields': ('location', 'city', 'address', 'zipcode', 'country'),
        }),
        ('DETAILS', {
            'fields': ('bedrooms', 'bathrooms', 'area', 'size', 'floors', 'garage'),
        }),
        ('FOTOS', {
            'fields': ('photo_main', 'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6'),
            'classes': ('collapse',),
        }),
        ('MAKLER', {
            'fields': ('realtor', 'company_name', 'email', 'oib_number'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['fehler_anzeige', 'geprueft_am']
    
    @admin.display(description='Fehler (kroatisch fuer Makler)')
    def fehler_anzeige(self, obj):
        if not obj.pruefung_fehler:
            return format_html('<span style="color:#1a5c1a;font-weight:bold;">Alles OK - kann freigeschaltet werden</span>')
        
        fehler_liste = obj.pruefung_fehler.split("\n")
        html = '<div style="background:#fff3cd;border:1px solid #ffc107;border-radius:5px;padding:10px;">'
        html += '<strong>Fehler (Makler sieht auf Kroatisch):</strong><ul style="margin:10px 0;">'
        for f in fehler_liste:
            html += f'<li style="color:#8b0000;">{f}</li>'
        html += '</ul></div>'
        return format_html(html)


Listing._meta.verbose_name = 'Immobilie'
Listing._meta.verbose_name_plural = 'Immobilien'
