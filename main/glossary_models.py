# main/glossary_models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.text import slugify

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


def validate_short_def_120(value):
    if value and len(value) > 120:
        raise ValidationError(f"short_def max 120 Zeichen. Aktuell: {len(value)}")


def normalize_slug(text):
    if not text:
        return ""
    replacements = {
        'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
        'Ä': 'ae', 'Ö': 'oe', 'Ü': 'ue',
        'č': 'c', 'ć': 'c', 'š': 's', 'ž': 'z', 'đ': 'd',
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return slugify(text)


class TermCategory(models.Model):
    group = models.CharField(max_length=30, choices=GROUP_CHOICES)
    key = models.CharField(max_length=60, unique=True)
    label = models.CharField(max_length=120)
    label_en = models.CharField(max_length=120, blank=True)
    label_hr = models.CharField(max_length=120, blank=True)
    order = models.PositiveIntegerField(default=100)

    class Meta:
        verbose_name = "Taxonomie-Kategorie"
        verbose_name_plural = "Taxonomie-Kategorien"
        ordering = ["group", "order", "label"]

    def __str__(self):
        return f"{self.get_group_display()}: {self.label} ({self.key})"

    def get_label_for_language(self, lang):
        if lang == 'en' and self.label_en:
            return self.label_en
        elif lang == 'hr' and self.label_hr:
            return self.label_hr
        return self.label


class GlossaryTerm(models.Model):
    canonical_key = models.SlugField(max_length=120, unique=True)
    categories = models.ManyToManyField(TermCategory, blank=True, related_name="terms")
    related_terms = models.ManyToManyField("self", symmetrical=False, blank=True, related_name="related_from")
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Glossar-Begriff"
        verbose_name_plural = "Glossar-Begriffe"
        ordering = ["canonical_key"]

    def __str__(self):
        return self.canonical_key

    def get_translation(self, lang):
        return self.translations.filter(language=lang).first()


class GlossaryTermTranslation(models.Model):
    term = models.ForeignKey(GlossaryTerm, on_delete=models.CASCADE, related_name="translations")
    language = models.CharField(max_length=2, choices=LANG_CHOICES)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    short_def = models.CharField(max_length=180, validators=[validate_short_def_120])
    long_def = models.TextField(blank=True)
    synonyms = models.JSONField(default=list, blank=True)
    keywords = models.JSONField(default=list, blank=True)
    faqs = models.JSONField(default=list, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")
    meta_title = models.CharField(max_length=70, blank=True)
    meta_description = models.CharField(max_length=160, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Glossar-Übersetzung"
        verbose_name_plural = "Glossar-Übersetzungen"
        unique_together = [("language", "slug"), ("term", "language")]
        ordering = ["language", "title"]
        indexes = [
            models.Index(fields=["language", "slug"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"[{self.language.upper()}] {self.title}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = normalize_slug(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        country = COUNTRY_NAMES.get(self.language, 'kroatien')
        glossary_segment = GLOSSARY_URLS.get(self.language, 'glossar')
        return f"/{self.language}/{country}/{glossary_segment}/{self.slug}/"


class GlossaryTermAlias(models.Model):
    language = models.CharField(max_length=2, choices=LANG_CHOICES)
    slug = models.SlugField(max_length=200)
    translation = models.ForeignKey(GlossaryTermTranslation, on_delete=models.CASCADE, related_name="aliases")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Glossar-Alias"
        verbose_name_plural = "Glossar-Aliase"
        unique_together = [("language", "slug")]

    def __str__(self):
        return f"[{self.language.upper()}] {self.slug} -> {self.translation.slug}"