import qrcode
import io
import base64
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET
from django_ratelimit.decorators import ratelimit
from listings.models import Listing


def generate_qr_code(url):
    """Generiert einen QR-Code als Base64-String"""
    qr = qrcode.QRCode(version=1, box_size=4, border=2)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode()


@ratelimit(key='ip', rate='10/m', method='GET', block=True)
@require_GET
def expose_view(request, listing_id):
    """Exposé-Ansicht mit Rate-Limiting"""
    listing = get_object_or_404(Listing, id=listing_id, is_published=True)
    
    # Sprache aus Session
    lang = request.session.get('site_language', 'ge')
    
    # QR-Code zur Online-Ansicht generieren
    online_url = f"https://123-kroatien.eu/{lang}/property-details/{listing_id}/"
    qr_code_base64 = generate_qr_code(online_url)
    
    # Alle Bilder sammeln
    images = []
    if listing.photo_main:
        images.append(listing.photo_main.url)
    for i in range(1, 21):
        photo = getattr(listing, f'photo_{i}', None)
        if photo:
            images.append(photo.url)
    
    # Übersetzungen für das Exposé
    EXPOSE_TRANSLATIONS = {
        "ge": {
            "title": "Immobilien-Exposé",
            "price": "Preis",
            "size": "Wohnfläche",
            "plot": "Grundstück",
            "rooms": "Zimmer",
            "bedrooms": "Schlafzimmer",
            "bathrooms": "Badezimmer",
            "type": "Objektart",
            "status": "Status",
            "location": "Lage",
            "description": "Beschreibung",
            "features": "Ausstattung",
            "contact": "Kontakt",
            "phone": "Telefon",
            "email": "E-Mail",
            "print": "Drucken",
            "share": "Teilen",
            "scan_qr": "QR-Code scannen für Online-Ansicht",
            "generated": "Erstellt über",
            "sale": "Zum Verkauf",
            "rent": "Zur Miete",
        },
        "en": {
            "title": "Property Exposé",
            "price": "Price",
            "size": "Living Area",
            "plot": "Plot Size",
            "rooms": "Rooms",
            "bedrooms": "Bedrooms",
            "bathrooms": "Bathrooms",
            "type": "Property Type",
            "status": "Status",
            "location": "Location",
            "description": "Description",
            "features": "Features",
            "contact": "Contact",
            "phone": "Phone",
            "email": "Email",
            "print": "Print",
            "share": "Share",
            "scan_qr": "Scan QR code for online view",
            "generated": "Generated via",
            "sale": "For Sale",
            "rent": "For Rent",
        },
        "hr": {
            "title": "Izložba nekretnine",
            "price": "Cijena",
            "size": "Stambena površina",
            "plot": "Površina zemljišta",
            "rooms": "Sobe",
            "bedrooms": "Spavaće sobe",
            "bathrooms": "Kupaonice",
            "type": "Vrsta nekretnine",
            "status": "Status",
            "location": "Lokacija",
            "description": "Opis",
            "features": "Značajke",
            "contact": "Kontakt",
            "phone": "Telefon",
            "email": "E-mail",
            "print": "Ispis",
            "share": "Podijeli",
            "scan_qr": "Skenirajte QR kod za online prikaz",
            "generated": "Generirano putem",
            "sale": "Na prodaju",
            "rent": "Za najam",
        },
    }
    
    # Default zu Deutsch wenn Sprache nicht vorhanden
    trans = EXPOSE_TRANSLATIONS.get(lang, EXPOSE_TRANSLATIONS["ge"])
    
    context = {
        'listing': listing,
        'images': images,
        'qr_code': qr_code_base64,
        'online_url': online_url,
        'trans': trans,
        'language': lang,
    }
    
    return render(request, 'main/expose.html', context)


@ratelimit(key='ip', rate='20/m', method='GET', block=True)
def expose_captcha_check(request):
    """AJAX endpoint für Captcha-Validierung vor dem Exposé-Zugriff"""
    # Einfache Rate-Limit Prüfung - bei zu vielen Anfragen wird blockiert
    return JsonResponse({'status': 'ok'})
