# main/glossary_models.py
"""
Glossar-Datenmodell für Kroatien Immobilienportal
SEO- und KI-optimiert, 12 Sprachen, Enterprise-Grade

Struktur:
- GlossaryTerm: Sprachunabhängige Term-Identität (canonical_key)
- GlossaryTermTranslation: Sprachspezifische Inhalte & SEO-Slugs
- GlossaryTermAlias: Alias-Redirects pro Sprache (301)
- TermCategory: Taxonomien (audience, topic, asset_type)
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify
import re


# ============================================
# KONSTANTEN
# ============================================

LANG_CHOICES = [
    ("ge", "Deutsch"),
    ("en", "English"),
    ("hr", "Hrvatski"),
    ("fr", "Français"),
    ("nl", "Nederlands"),
    ("pl", "Polski"),
    ("cz", "Čeština"),
    ("sk", "Slovenčina"),
    ("ru", "Русский"),
    ("gr", "Ελληνικά"),
    ("sw", "Svenska"),
    ("no", "Norsk"),
]

STATUS_CHOICES = [
    ("draft", "Draft"),
    ("needs_review", "Needs Review"),
    ("approved", "Approved"),
    ("published", "Published"),
]

GROUP_CHOICES = [
    ("audience", "Audience"),
    ("topic", "Topic"),
    ("asset_type", "Asset Type"),
]

# Glossar-Pfad je Sprache
GLOSSARY_URLS = {
    "ge": "glossar",
    "en": "glossary",
    "hr": "pojmovnik",
    "fr": "glossaire",
    "nl": "woordenlijst",
    "pl": "slownik",
    "cz": "glosar",
    "sk": "slovnik",
    "ru": "glossarij",
    "gr": "glossari",
    "sw": "ordlista",
    "no": "ordliste",
}

GLOSSARY_URLS_REVERSE = {v: k for k, v in GLOSSARY_URLS.items()}

# Länder-Namen in allen Sprachen
COUNTRY_NAMES = {
    "ge": "kroatien",
    "en": "croatia",
    "hr": "hrvatska",
    "fr": "croatie",
    "nl": "kroatie",
    "pl": "chorwacja",
    "cz": "chorvatsko",
    "sk": "chorvatsko",
    "ru": "horvatiya",
    "gr": "kroatia",
    "sw": "kroatien",
    "no": "kroatia",
}


# ============================================
# VALIDATOREN
# ============================================

def validate_short_def_120(value: str):
    """Validiert, dass short_def maximal 120 Zeichen hat (Mobile/Tooltip)."""
    if value and len(value) > 120:
        raise ValidationError(
            f"short_def darf max. 120 Zeichen haben (Mobile/Tooltip). Aktuell: {len(value)} Zeichen."
        )


def normalize_slug(text: str) -> str:
    """
    Normalisiert Text zu URL-sicherem Slug.
    - Umlaute: ä->ae, ö->oe, ü->ue, ß->ss
    - ASCII, lowercase, hyphenated
    """
    if not text:
        return ""
    
    # Umlaut-Ersetzungen
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue',
        'č': 'c', 'ć': 'c', 'š': 's', 'ž': 'z', 'đ': 'd',
        'Č': 'c', 'Ć': 'c', 'Š': 's', 'Ž': 'z', 'Đ': 'd',
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return slugify(text)


# ============================================
# MODELS
# ============================================

class TermCategory(models.Model):
    """
    Taxonomien für Filter und Navigation.
    
    Gruppen:
    - audience: Zielgruppe (investor, holiday-buyer, luxury)
    - topic: Thema (legal, tax, purchase-process, etc.)
    - asset_type: Objekttyp (apartment, villa, house, etc.)
    """
    group = models.CharField(
        max_length=30,
        choices=GROUP_CHOICES,
        verbose_name="Gruppe"
    )
    key = models.CharField(
        max_length=60,
        unique=True,
        verbose_name="Schlüssel",
        help_text="Eindeutiger technischer Schlüssel, z.B. 'investor', 'legal', 'villa'"
    )
    label = models.CharField(
        max_length=120,
        verbose_name="Label (DE)",
        help_text="Anzeigename auf Deutsch"
    )
    label_en = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Label (EN)"
    )
    label_hr = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Label (HR)"
    )
    order = models.PositiveIntegerField(
        default=100,
        verbose_name="Sortierung"
    )
    
    class Meta:
        verbose_name = "Taxonomie-Kategorie"
        verbose_name_plural = "Taxonomie-Kategorien"
        ordering = ["group", "order", "label"]
    
    def __str__(self):
        return f"{self.get_group_display()}: {self.label} ({self.key})"
    
    def get_label_for_language(self, lang: str) -> str:
        """Gibt das Label für die angegebene Sprache zurück."""
        if lang == 'en' and self.label_en:
            return self.label_en
        elif lang == 'hr' and self.label_hr:
            return self.label_hr
        return self.label  # Fallback zu Deutsch


class GlossaryTerm(models.Model):
    """
    Sprachunabhängige Term-Identität.
    
    Der canonical_key ist stabil und wird nach Veröffentlichung nie geändert.
    Alle Übersetzungen referenzieren diesen Term.
    """
    canonical_key = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name="Canonical Key",
        help_text="Stabiler interner Schlüssel (nie ändern nach Publish!), z.B. 'land-registry'"
    )
    categories = models.ManyToManyField(
        TermCategory,
        blank=True,
        related_name="terms",
        verbose_name="Kategorien"
    )
    is_published = models.BooleanField(
        default=False,
        verbose_name="Veröffentlicht",
        help_text="Steuert Sichtbarkeit in Index und Sitemap"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Glossar-Begriff"
        verbose_name_plural = "Glossar-Begriffe"
        ordering = ["canonical_key"]
    
    def __str__(self):
        return self.canonical_key
    
    def get_translation(self, lang: str):
        """Gibt die Übersetzung für eine Sprache zurück, falls vorhanden."""
        return self.translations.filter(language=lang).first()
    
    def get_published_translations(self):
        """Gibt alle veröffentlichten/genehmigten Übersetzungen zurück."""
        return self.translations.filter(status__in=['approved', 'published'])


class GlossaryTermTranslation(models.Model):
    """
    Sprachspezifische Inhalte & SEO-Slug.
    
    Jede Sprache hat eigene:
    - title: Anzeige-Titel
    - slug: URL-Slug (pro Sprache einzigartig)
    - short_def: Kurzdefinition (max 120 Zeichen, für Mobile/Tooltips)
    - long_def: Ausführliche Definition
    - synonyms: Alternative Begriffe (für Suche & AI)
    - keywords: SEO-Keywords
    - faqs: Häufige Fragen als JSON
    """
    term = models.ForeignKey(
        GlossaryTerm,
        on_delete=models.CASCADE,
        related_name="translations",
        verbose_name="Begriff"
    )
    language = models.CharField(
        max_length=2,
        choices=LANG_CHOICES,
        verbose_name="Sprache"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Titel"
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name="URL-Slug",
        help_text="Sprachspezifischer Slug für die URL"
    )
    short_def = models.CharField(
        max_length=180,
        validators=[validate_short_def_120],
        verbose_name="Kurzdefinition",
        help_text="Max. 120 Zeichen (für Mobile & Tooltips)"
    )
    long_def = models.TextField(
        blank=True,
        verbose_name="Ausführliche Definition"
    )
    
    # AI/SEO Felder (JSON)
    synonyms = models.JSONField(
        default=list,
        blank=True,
        verbose_name="Synonyme",
        help_text='Liste von Synonymen, z.B. ["Grundbuchauszug", "Grundbucheintrag"]'
    )
    keywords = models.JSONField(
        default=list,
        blank=True,
        verbose_name="SEO-Keywords",
        help_text='Liste von Keywords für SEO/AI'
    )
    faqs = models.JSONField(
        default=list,
        blank=True,
        verbose_name="FAQs",
        help_text='Liste von FAQs, z.B. [{"q": "Frage?", "a": "Antwort"}]'
    )
    
    # Workflow
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        verbose_name="Status"
    )
    
    # Meta-Informationen
    meta_title = models.CharField(
        max_length=70,
        blank=True,
        verbose_name="Meta Title",
        help_text="SEO-Titel (max 70 Zeichen)"
    )
    meta_description = models.CharField(
        max_length=160,
        blank=True,
        verbose_name="Meta Description",
        help_text="SEO-Beschreibung (max 160 Zeichen)"
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Glossar-Übersetzung"
        verbose_name_plural = "Glossar-Übersetzungen"
        unique_together = [
            ("language", "slug"),   # Einzigartiger URL pro Sprache
            ("term", "language"),   # Eine Übersetzung pro Sprache pro Begriff
        ]
        ordering = ["language", "title"]
        indexes = [
            models.Index(fields=["language", "slug"]),
            models.Index(fields=["status"]),
            models.Index(fields=["updated_at"]),
        ]
    
    def __str__(self):
        return f"[{self.language.upper()}] {self.title}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = normalize_slug(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Gibt die vollständige URL für diesen Begriff zurück."""
        country = COUNTRY_NAMES.get(self.language, 'kroatien')
        glossary_segment = GLOSSARY_URLS.get(self.language, 'glossar')
        return f"/{self.language}/{country}/{glossary_segment}/{self.slug}/"
    
    def get_canonical_url(self):
        """Alias für get_absolute_url (für SEO-Templates)."""
        return self.get_absolute_url()


class GlossaryTermAlias(models.Model):
    """
    Alias-Redirects pro Sprache (Synonyme/Legacy Slugs) -> canonical Translation.
    
    Wird verwendet für:
    - Synonym-Slugs (z.B. "grundbuchauszug" -> "grundbuch")
    - Legacy-URLs nach Slug-Änderungen
    - Alternative Schreibweisen
    
    Alle Aliases führen zu einem 301-Redirect auf die canonical URL.
    """
    language = models.CharField(
        max_length=2,
        choices=LANG_CHOICES,
        verbose_name="Sprache"
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name="Alias-Slug",
        help_text="Der alternative Slug, der umgeleitet werden soll"
    )
    translation = models.ForeignKey(
        GlossaryTermTranslation,
        on_delete=models.CASCADE,
        related_name="aliases",
        verbose_name="Ziel-Übersetzung"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Glossar-Alias"
        verbose_name_plural = "Glossar-Aliase"
        unique_together = [("language", "slug")]
        indexes = [
            models.Index(fields=["language", "slug"]),
        ]
    
    def __str__(self):
        return f"[{self.language.upper()}] {self.slug} → {self.translation.slug}"
