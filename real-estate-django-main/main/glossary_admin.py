# main/glossary_admin.py
"""
Django Admin Konfiguration für Glossar
- Inline Translations pro Term
- Status-Workflow (draft → needs_review → approved → published)
- KI-Übersetzungs-Hilfe (optional)
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .glossary_models import (
    GlossaryTerm,
    GlossaryTermTranslation,
    GlossaryTermAlias,
    TermCategory,
)


# ============================================
# INLINE ADMINS
# ============================================

class GlossaryTermTranslationInline(admin.TabularInline):
    """Inline für Übersetzungen im Term-Admin."""
    model = GlossaryTermTranslation
    extra = 0
    fields = [
        "language",
        "title",
        "slug",
        "short_def",
        "status",
        "updated_at",
    ]
    readonly_fields = ["updated_at"]
    ordering = ["language"]
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related("term")


class GlossaryTermAliasInline(admin.TabularInline):
    """Inline für Aliase im Translation-Admin."""
    model = GlossaryTermAlias
    extra = 0
    fields = ["language", "slug", "created_at"]
    readonly_fields = ["created_at"]


# ============================================
# TERM CATEGORY ADMIN
# ============================================

@admin.register(TermCategory)
class TermCategoryAdmin(admin.ModelAdmin):
    """Admin für Taxonomie-Kategorien."""
    list_display = ["key", "group", "label", "label_en", "label_hr", "order"]
    list_filter = ["group"]
    search_fields = ["key", "label", "label_en", "label_hr"]
    ordering = ["group", "order", "label"]
    
    fieldsets = (
        (None, {
            "fields": ("group", "key", "order")
        }),
        ("Labels", {
            "fields": ("label", "label_en", "label_hr"),
            "description": "Anzeigenamen in verschiedenen Sprachen"
        }),
    )


# ============================================
# GLOSSARY TERM ADMIN
# ============================================

@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    """
    Admin für Glossar-Begriffe.
    
    Features:
    - Inline Translations
    - Kategorien-Zuordnung
    - Publish-Status
    """
    list_display = [
        "canonical_key",
        "is_published",
        "get_translations_count",
        "get_categories_display",
        "updated_at",
    ]
    list_filter = [
        "is_published",
        "categories__group",
        "categories",
    ]
    search_fields = [
        "canonical_key",
        "translations__title",
        "translations__short_def",
    ]
    filter_horizontal = ["categories"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["canonical_key"]
    
    inlines = [GlossaryTermTranslationInline]
    
    fieldsets = (
        (None, {
            "fields": ("canonical_key", "is_published")
        }),
        ("Kategorien", {
            "fields": ("categories",),
            "description": "Ordne den Begriff Zielgruppen, Themen und Objekttypen zu"
        }),
        ("Metadaten", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def get_translations_count(self, obj):
        """Zeigt Anzahl der Übersetzungen."""
        count = obj.translations.count()
        published = obj.translations.filter(status__in=["approved", "published"]).count()
        return f"{published}/{count}"
    get_translations_count.short_description = "Übersetzungen (veröff./gesamt)"
    
    def get_categories_display(self, obj):
        """Zeigt zugeordnete Kategorien."""
        cats = obj.categories.all()[:3]
        display = ", ".join([c.key for c in cats])
        if obj.categories.count() > 3:
            display += f" (+{obj.categories.count() - 3})"
        return display or "-"
    get_categories_display.short_description = "Kategorien"
    
    actions = ["publish_terms", "unpublish_terms"]
    
    @admin.action(description="Ausgewählte Begriffe veröffentlichen")
    def publish_terms(self, request, queryset):
        updated = queryset.update(is_published=True)
        self.message_user(request, f"{updated} Begriff(e) veröffentlicht.")
    
    @admin.action(description="Ausgewählte Begriffe zurückziehen")
    def unpublish_terms(self, request, queryset):
        updated = queryset.update(is_published=False)
        self.message_user(request, f"{updated} Begriff(e) zurückgezogen.")


# ============================================
# GLOSSARY TRANSLATION ADMIN
# ============================================

@admin.register(GlossaryTermTranslation)
class GlossaryTermTranslationAdmin(admin.ModelAdmin):
    """
    Admin für Glossar-Übersetzungen.
    
    Features:
    - Detaillierte Bearbeitung pro Sprache
    - Status-Workflow
    - JSON-Felder (Synonyme, Keywords, FAQs)
    """
    list_display = [
        "title",
        "language",
        "term_link",
        "slug",
        "short_def_preview",
        "status",
        "updated_at",
    ]
    list_filter = [
        "language",
        "status",
        "term__is_published",
        "term__categories__group",
    ]
    search_fields = [
        "title",
        "slug",
        "short_def",
        "long_def",
        "term__canonical_key",
    ]
    readonly_fields = ["updated_at", "created_at", "preview_url"]
    ordering = ["language", "title"]
    autocomplete_fields = ["term"]
    
    inlines = [GlossaryTermAliasInline]
    
    fieldsets = (
        (None, {
            "fields": ("term", "language", "status")
        }),
        ("Inhalt", {
            "fields": ("title", "slug", "short_def", "long_def")
        }),
        ("SEO & AI", {
            "fields": ("synonyms", "keywords", "faqs"),
            "description": "JSON-Listen für Suche und KI-Optimierung"
        }),
        ("Meta-Tags", {
            "fields": ("meta_title", "meta_description"),
            "classes": ("collapse",)
        }),
        ("Metadaten", {
            "fields": ("preview_url", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    
    def term_link(self, obj):
        """Link zum Term-Admin."""
        url = reverse("admin:main_glossaryterm_change", args=[obj.term.pk])
        return format_html('<a href="{}">{}</a>', url, obj.term.canonical_key)
    term_link.short_description = "Begriff"
    
    def short_def_preview(self, obj):
        """Gekürzte Vorschau der Kurzdefinition."""
        if len(obj.short_def) > 50:
            return f"{obj.short_def[:50]}..."
        return obj.short_def
    short_def_preview.short_description = "Kurzdefinition"
    
    def preview_url(self, obj):
        """Link zur Frontend-Seite."""
        if obj.pk:
            url = obj.get_absolute_url()
            return format_html('<a href="{}" target="_blank">{}</a>', url, url)
        return "-"
    preview_url.short_description = "Vorschau-URL"
    
    actions = [
        "set_status_draft",
        "set_status_needs_review",
        "set_status_approved",
        "set_status_published",
    ]
    
    @admin.action(description="Status → Draft")
    def set_status_draft(self, request, queryset):
        updated = queryset.update(status="draft")
        self.message_user(request, f"{updated} Übersetzung(en) auf 'Draft' gesetzt.")
    
    @admin.action(description="Status → Needs Review")
    def set_status_needs_review(self, request, queryset):
        updated = queryset.update(status="needs_review")
        self.message_user(request, f"{updated} Übersetzung(en) auf 'Needs Review' gesetzt.")
    
    @admin.action(description="Status → Approved")
    def set_status_approved(self, request, queryset):
        updated = queryset.update(status="approved")
        self.message_user(request, f"{updated} Übersetzung(en) auf 'Approved' gesetzt.")
    
    @admin.action(description="Status → Published")
    def set_status_published(self, request, queryset):
        updated = queryset.update(status="published")
        self.message_user(request, f"{updated} Übersetzung(en) auf 'Published' gesetzt.")


# ============================================
# GLOSSARY ALIAS ADMIN
# ============================================

@admin.register(GlossaryTermAlias)
class GlossaryTermAliasAdmin(admin.ModelAdmin):
    """Admin für Glossar-Aliase (301 Redirects)."""
    list_display = ["slug", "language", "translation_link", "created_at"]
    list_filter = ["language"]
    search_fields = ["slug", "translation__title", "translation__slug"]
    ordering = ["language", "slug"]
    autocomplete_fields = ["translation"]
    
    def translation_link(self, obj):
        """Link zur Ziel-Übersetzung."""
        url = reverse("admin:main_glossarytermtranslation_change", args=[obj.translation.pk])
        return format_html('<a href="{}">{}</a>', url, obj.translation.title)
    translation_link.short_description = "Ziel"
