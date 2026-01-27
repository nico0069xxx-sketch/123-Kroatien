from django.db import models
from listings.image_utils import compress_image
from datetime import datetime
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.

class Realtor(models.Model):
    name = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    is_mvp = models.BooleanField(default=False)  ## Seller of the month
    hire_date = models.DateTimeField(default=datetime.now, blank=True)


    def save(self, *args, **kwargs):
        """Komprimiert Bilder automatisch beim Speichern."""
        if self.photo and hasattr(self.photo, 'file'):
            try:
                if hasattr(self.photo.file, 'content_type'):
                    self.photo = compress_image(self.photo)
            except Exception as e:
                print(f"Komprimierung fehlgeschlagen: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Interface(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    # description = RichTextField(blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    description2 = RichTextUploadingField(
        blank=True, null=True, config_name='special', 
        external_plugin_resources=[(
            'youtube', 
            '/static/ckeditor_plugins/youtube/', 
            'plugin.js',
        )],
    )
    is_published = models.BooleanField(default=True)
    created = models.DateTimeField(default=datetime.now, blank=True)


    def save(self, *args, **kwargs):
        """Komprimiert Bilder automatisch beim Speichern."""
        if self.photo and hasattr(self.photo, 'file'):
            try:
                if hasattr(self.photo.file, 'content_type'):
                    self.photo = compress_image(self.photo)
            except Exception as e:
                print(f"Komprimierung fehlgeschlagen: {e}")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


