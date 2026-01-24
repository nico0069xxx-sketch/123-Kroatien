# main/glossary_admin.py
from django.contrib import admin
from .glossary_models import GlossaryTerm, GlossaryTermTranslation, GlossaryTermAlias, TermCategory


class GlossaryTermTranslationInline(admin.TabularInline):
    model = GlossaryTermTranslation
    extra = 0
    fields = ["language", "title", "slug", "short_def", "status"]


@admin.register(TermCategory)
class TermCategoryAdmin(admin.ModelAdmin):
    list_display = ["key", "group", "label", "order"]
    list_filter = ["group"]
    ordering = ["group", "order"]


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ["canonical_key", "is_published", "updated_at"]
    list_filter = ["is_published", "categories__group"]
    search_fields = ["canonical_key", "translations__title"]
    filter_horizontal = ["categories"]
    inlines = [GlossaryTermTranslationInline]


@admin.register(GlossaryTermTranslation)
class GlossaryTermTranslationAdmin(admin.ModelAdmin):
    list_display = ["title", "language", "slug", "status", "updated_at"]
    list_filter = ["language", "status"]
    search_fields = ["title", "slug", "short_def"]
    autocomplete_fields = ["term"]


@admin.register(GlossaryTermAlias)
class GlossaryTermAliasAdmin(admin.ModelAdmin):
    list_display = ["slug", "language", "translation"]
    list_filter = ["language"]
    autocomplete_fields = ["translation"]