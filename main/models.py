from django.db import models

class StaticContent(models.Model):
    key = models.CharField(max_length=100, unique=True)  # z.B. "faq_title"
    page = models.CharField(max_length=50)  # z.B. "faq", "owner", etc.
    
    # Alle 12 Sprachen
    german = models.TextField(blank=True, null=True)
    english = models.TextField(blank=True, null=True)
    french = models.TextField(blank=True, null=True)
    greek = models.TextField(blank=True, null=True)
    croatian = models.TextField(blank=True, null=True)
    polish = models.TextField(blank=True, null=True)
    czech = models.TextField(blank=True, null=True)
    russian = models.TextField(blank=True, null=True)
    swedish = models.TextField(blank=True, null=True)
    norwegian = models.TextField(blank=True, null=True)
    slovak = models.TextField(blank=True, null=True)
    dutch = models.TextField(blank=True, null=True)
    
    def get_translation(self, lang_code):
        lang_map = {
            'ge': self.german,
            'en': self.english,
            'fr': self.french,
            'gr': self.greek,
            'hr': self.croatian,
            'pl': self.polish,
            'cz': self.czech,
            'ru': self.russian,
            'sw': self.swedish,
            'no': self.norwegian,
            'sk': self.slovak,
            'nl': self.dutch,
        }
        return lang_map.get(lang_code) or self.german or self.english
    
    def __str__(self):
        return f"{self.page} - {self.key}"
    
    class Meta:
        verbose_name = "Statischer Inhalt"
        verbose_name_plural = "Statische Inhalte"


# Professional Models importieren
from main.professional_models import (
    Professional,
    RealEstateAgentProfile,
    ConstructionCompanyProfile,
    LawyerProfile,
    TaxAdvisorProfile,
    ArchitectProfile,
    ProfessionalContent,
)

# Import Glossar Models für Django Migration
from .glossary_models import *
