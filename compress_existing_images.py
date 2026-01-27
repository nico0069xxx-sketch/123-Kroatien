"""
Script zum Komprimieren der bestehenden großen Bilder
Einmalige Ausführung!
"""
from PIL import Image
import os

# Konfiguration
IMAGES_DIR = os.path.join(os.path.dirname(__file__), 'static', 'images')
MAX_WIDTH = 1920
MAX_HEIGHT = 1080
QUALITY = 82

# Bilder die komprimiert werden sollen
TARGET_IMAGES = [
    '1.png', '2.png', '3.png', '4.png', '5.png',  # Hero Slider
    'bg10.png', 'bg12.png', 'bg13.png', 'bg14.png', 'bg15.png',  # Hintergründe
]

def compress_image(filepath):
    """Komprimiert ein Bild zu WebP"""
    try:
        original_size = os.path.getsize(filepath)
        
        img = Image.open(filepath)
        original_dims = img.size
        
        # RGBA zu RGB
        if img.mode in ('RGBA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Größe anpassen
        if img.width > MAX_WIDTH or img.height > MAX_HEIGHT:
            ratio = min(MAX_WIDTH / img.width, MAX_HEIGHT / img.height)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
        
        # Als WebP speichern
        webp_path = filepath.rsplit('.', 1)[0] + '.webp'
        img.save(webp_path, 'WEBP', quality=QUALITY, optimize=True)
        
        new_size = os.path.getsize(webp_path)
        savings = ((original_size - new_size) / original_size) * 100
        
        print(f"✅ {os.path.basename(filepath)}")
        print(f"   {original_dims[0]}x{original_dims[1]} → {img.size[0]}x{img.size[1]}")
        print(f"   {original_size/1024/1024:.2f} MB → {new_size/1024:.0f} KB ({savings:.0f}% gespart)")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ {filepath}: {e}")
        return False

def main():
    print("=" * 50)
    print("🖼️  Bildkomprimierung für 123-Kroatien.eu")
    print("=" * 50)
    print()
    
    total_saved = 0
    
    for filename in TARGET_IMAGES:
        filepath = os.path.join(IMAGES_DIR, filename)
        if os.path.exists(filepath):
            original_size = os.path.getsize(filepath)
            if compress_image(filepath):
                webp_path = filepath.rsplit('.', 1)[0] + '.webp'
                new_size = os.path.getsize(webp_path)
                total_saved += original_size - new_size
    
    print("=" * 50)
    print(f"💾 Gesamt gespart: {total_saved/1024/1024:.2f} MB")
    print()
    print("⚠️  WICHTIG: Jetzt die Templates anpassen!")
    print("   .png → .webp in home.html und custom.css")
    print("=" * 50)

if __name__ == '__main__':
    main()
