from django.db import models
from datetime import datetime
from accounts.models import Agent
import json
from .image_utils import compress_image
# Create your models here.

class Listing(models.Model):
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company_logo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    portrait_photo = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True, null=True)
    oib_number = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    domain = models.CharField(max_length=200, blank=True, null=True)
    realtor = models.ForeignKey(Agent, on_delete=models.DO_NOTHING, blank=True, null=True)
    property_title = models.CharField(max_length=200, blank=True)
    property_description = models.TextField(blank=True)
    property_type = models.CharField(max_length=200, blank=True)
    property_status = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    bedrooms = models.IntegerField(blank=True)
    bathrooms = models.IntegerField(default=0, blank=True)
    floors = models.IntegerField()
    garage = models.IntegerField(default=0)
    area = models.IntegerField()
    size = models.DecimalField(max_digits=5, decimal_places=1)
    property_price = models.IntegerField(default=0, blank=True)
    property_id = models.IntegerField(default="1", blank=True)
    video_url = models.CharField(max_length=200, blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    photo_1 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)   ## blank=True used to make this field optional
    photo_2 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_3 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_4 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_5 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    photo_6 = models.ImageField(upload_to='photos/%Y/%m/%d/', blank=True)
    
    # Foto-Beschriftungen
    photo_main_caption = models.CharField(max_length=200, blank=True, verbose_name="Hauptfoto Beschriftung")
    photo_1_caption = models.CharField(max_length=200, blank=True, verbose_name="Foto 2 Beschriftung")
    photo_2_caption = models.CharField(max_length=200, blank=True, verbose_name="Foto 3 Beschriftung")
    photo_3_caption = models.CharField(max_length=200, blank=True, verbose_name="Foto 4 Beschriftung")
    photo_4_caption = models.CharField(max_length=200, blank=True, verbose_name="Foto 5 Beschriftung")
    photo_5_caption = models.CharField(max_length=200, blank=True, verbose_name="Foto 6 Beschriftung")
    photo_6_caption = models.CharField(max_length=200, blank=True, verbose_name="Foto 7 Beschriftung")
    
    # Status-System
    LISTING_STATUS = [
        ('pruefung', 'Zur Pruefung'),
        ('aktiv', 'Aktiv (Online)'),
        ('verkauft', 'Verkauft'),
        ('pausiert', 'Pausiert'),
        ('abgelehnt', 'Abgelehnt'),
    ]
    
    listing_status = models.CharField(max_length=20, choices=LISTING_STATUS, default='pruefung')
    is_published = models.BooleanField(default=False)
    
    # Pruefungs-Infos
    pruefung_fehler = models.TextField(blank=True, null=True)
    pruefung_notizen = models.TextField(blank=True, null=True)
    geprueft_am = models.DateTimeField(blank=True, null=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    address = models.CharField(max_length=200, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    zipcode = models.CharField(max_length=20, blank=True)
    neighborhood = models.CharField(max_length=100, blank=True)

    #translate
    english_content = models.TextField(blank=True)
    german_content = models.TextField(blank=True)
    french_content = models.TextField(blank=True)
    greek_content = models.TextField(blank=True)
    croatian_content = models.TextField(blank=True)
    polish_content = models.TextField(blank=True)
    czech_content = models.TextField(blank=True)
    russian_content = models.TextField(blank=True)
    swedish_content = models.TextField(blank=True)
    norway_content = models.TextField(blank=True)
    slovak_content = models.TextField(blank=True)
    dutch_content = models.TextField(blank=True)
    
    
    def save(self, *args, **kwargs):
        """Überschreibt save() um Bilder automatisch zu komprimieren."""
        # Liste aller Bildfelder
        image_fields = [
            'company_logo', 'portrait_photo', 'photo_main',
            'photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6'
        ]
        
        for field_name in image_fields:
            image = getattr(self, field_name, None)
            if image and hasattr(image, 'file'):
                try:
                    # Nur neue Uploads komprimieren (nicht bereits gespeicherte)
                    if hasattr(image.file, 'content_type'):
                        compressed = compress_image(image)
                        setattr(self, field_name, compressed)
                except Exception as e:
                    print(f"Komprimierung von {field_name} fehlgeschlagen: {e}")
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.property_title
    
    def get_json(self):
        return {
            "oib_number": self.oib_number,
            "property_title": self.property_title,
            "property_description": self.property_description,
            "property_type": self.property_type,
            "property_status": self.property_status,
            "location": self.location,
            "bedrooms": self.bedrooms,
            "bathrooms": float(self.bathrooms),
            "floors": self.floors,
            "garage": self.garage,
            "area": self.area,
            "size": float(self.size),
            "property_price": self.property_price,
            "address": self.address,
            "country": self.country,
            "city": self.city,
            "state": self.state,
            "zipcode": self.zipcode,
            "neighborhood": self.neighborhood,
        }

# Hinweis: Falls listing_status und pruefung_fehler noch nicht existieren,
# fuege diese Felder zur Listing-Klasse hinzu (vor __str__)
