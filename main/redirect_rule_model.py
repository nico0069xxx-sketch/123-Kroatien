# core/models.py (or redirects/models.py) – RedirectRule
from django.db import models
from django.core.validators import RegexValidator

HTTP_STATUS_CHOICES = (
    (301, "301 Permanent (SEO default)"),
    (308, "308 Permanent (preserve method)"),
    (302, "302 Temporary"),
    (307, "307 Temporary (preserve method)"),
)

source_validator = RegexValidator(
    regex=r"^/.*$",
    message="source_path must start with '/' and be a path only (no domain)."
)

class RedirectRule(models.Model):
    """Portal-wide redirect registry.

    Use cases:
    - Legacy URL migrations
    - Renamed slugs/categories
    - Consolidations of landing pages

    Safety:
    - Restrict to path-only sources to prevent open redirects.
    - target_url can be absolute or relative; validate in middleware.
    """

    is_active = models.BooleanField(default=True)

    # Path-only source, e.g. "/ge/kroatien/glossar/alt/"
    source_path = models.CharField(
        max_length=512,
        unique=True,
        validators=[source_validator],
        help_text="Exact incoming request.path to match (case-sensitive)."
    )

    # Target may be absolute (https://...) or relative (/ge/...)
    target_url = models.CharField(
        max_length=1024,
        help_text="Redirect destination. Use absolute URL only if required."
    )

    status_code = models.PositiveSmallIntegerField(
        choices=HTTP_STATUS_CHOICES,
        default=301
    )

    # Optional scoping / governance
    note = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["is_active", "source_path"]),
        ]
        verbose_name = "Redirect rule"
        verbose_name_plural = "Redirect rules"

    def __str__(self):
        return f"{self.source_path} -> {self.target_url} ({self.status_code})"
