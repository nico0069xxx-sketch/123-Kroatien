# core/admin.py (or redirects/admin.py) – RedirectRule admin
from django.contrib import admin
from .models import RedirectRule

@admin.register(RedirectRule)
class RedirectRuleAdmin(admin.ModelAdmin):
    list_display = ("source_path", "target_url", "status_code", "is_active", "updated_at")
    list_filter = ("is_active", "status_code")
    search_fields = ("source_path", "target_url", "note")
    ordering = ("-updated_at",)
    readonly_fields = ("created_at", "updated_at")
