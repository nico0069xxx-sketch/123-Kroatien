"""
Automatische Bildkomprimierung für Django-Uploads und URL-Downloads
- Konvertiert zu WebP (beste Komprimierung) oder JPEG
- Reduziert Dateigröße um 70-90%
- Behält gute Qualität bei
"""
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.files.base import ContentFile
import sys
import requests
import logging

logger = logging.getLogger(__name__)

# Konfiguration
MAX_WIDTH = 1920  # Maximale Breite
MAX_HEIGHT = 1080  # Maximale Höhe
QUALITY = 82  # Qualität (1-100)
OUTPUT_FORMAT = 'WEBP'  # WEBP oder JPEG


def compress_image(uploaded_image, max_width=MAX_WIDTH, max_height=MAX_HEIGHT, quality=QUALITY):
    """
    Komprimiert ein hochgeladenes Bild.
    
    Args:
        uploaded_image: Django UploadedFile
        max_width: Maximale Breite in Pixel
        max_height: Maximale Höhe in Pixel  
        quality: Komprimierungsqualität (1-100)
    
    Returns:
        InMemoryUploadedFile: Komprimiertes Bild
    """
    if not uploaded_image:
        return uploaded_image
    
    try:
        # Bild öffnen
        img = Image.open(uploaded_image)
        
        # RGBA zu RGB konvertieren (für JPEG/WebP)
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Größe anpassen wenn nötig
        original_width, original_height = img.size
        
        if original_width > max_width or original_height > max_height:
            ratio = min(max_width / original_width, max_height / original_height)
            new_size = (int(original_width * ratio), int(original_height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # In Buffer speichern
        output = BytesIO()
        
        if OUTPUT_FORMAT == 'WEBP':
            img.save(output, format='WEBP', quality=quality, optimize=True)
            content_type = 'image/webp'
            ext = '.webp'
        else:
            img.save(output, format='JPEG', quality=quality, optimize=True)
            content_type = 'image/jpeg'
            ext = '.jpg'
        
        output.seek(0)
        
        # Neuen Dateinamen erstellen
        original_name = uploaded_image.name
        name_without_ext = original_name.rsplit('.', 1)[0] if '.' in original_name else original_name
        new_name = f"{name_without_ext}{ext}"
        
        compressed = InMemoryUploadedFile(
            file=output,
            field_name=uploaded_image.field_name if hasattr(uploaded_image, 'field_name') else 'image',
            name=new_name,
            content_type=content_type,
            size=sys.getsizeof(output),
            charset=None
        )
        
        return compressed
        
    except Exception as e:
        print(f"Bildkomprimierung fehlgeschlagen: {e}")
        return uploaded_image


def download_and_compress_image(url, filename=None, max_width=MAX_WIDTH, max_height=MAX_HEIGHT, quality=QUALITY):
    """
    Lädt ein Bild von einer URL herunter und komprimiert es.
    
    Args:
        url: Bild-URL
        filename: Optionaler Dateiname (sonst aus URL extrahiert)
        max_width: Maximale Breite
        max_height: Maximale Höhe
        quality: Komprimierungsqualität
    
    Returns:
        ContentFile: Komprimiertes Bild als Django ContentFile oder None bei Fehler
    """
    if not url:
        return None
    
    try:
        # Bild herunterladen
        response = requests.get(url, timeout=30, stream=True)
        response.raise_for_status()
        
        # Bild öffnen
        img = Image.open(BytesIO(response.content))
        
        # RGBA zu RGB konvertieren
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[3] if len(img.split()) == 4 else None)
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Größe anpassen wenn nötig
        original_width, original_height = img.size
        
        if original_width > max_width or original_height > max_height:
            ratio = min(max_width / original_width, max_height / original_height)
            new_size = (int(original_width * ratio), int(original_height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            logger.info(f"Bild von {original_width}x{original_height} auf {new_size[0]}x{new_size[1]} skaliert")
        
        # In Buffer speichern
        output = BytesIO()
        
        if OUTPUT_FORMAT == 'WEBP':
            img.save(output, format='WEBP', quality=quality, optimize=True)
            ext = '.webp'
        else:
            img.save(output, format='JPEG', quality=quality, optimize=True)
            ext = '.jpg'
        
        output.seek(0)
        
        # Dateiname bestimmen
        if not filename:
            filename = url.split('/')[-1].split('?')[0]
        name_without_ext = filename.rsplit('.', 1)[0] if '.' in filename else filename
        new_filename = f"{name_without_ext}{ext}"
        
        original_size = len(response.content)
        compressed_size = output.getbuffer().nbytes
        savings = ((original_size - compressed_size) / original_size) * 100 if original_size > 0 else 0
        
        logger.info(f"Bild komprimiert: {original_size/1024:.1f}KB -> {compressed_size/1024:.1f}KB ({savings:.1f}% gespart)")
        
        return ContentFile(output.read(), name=new_filename)
        
    except requests.RequestException as e:
        logger.error(f"Fehler beim Herunterladen von {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Fehler bei Bildverarbeitung von {url}: {e}")
        return None


def get_image_info(image_path):
    """
    Gibt Informationen über ein Bild zurück.
    """
    try:
        img = Image.open(image_path)
        return {
            'width': img.width,
            'height': img.height,
            'format': img.format,
            'mode': img.mode,
        }
    except Exception as e:
        return {'error': str(e)}
