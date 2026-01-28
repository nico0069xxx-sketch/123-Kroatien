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
    lang = request.session.get("site_language", "ge")

    # KI-übersetzten Content laden
    from main.ai_listing_helper import get_listing_content_with_ai
    listing.json_content = get_listing_content_with_ai(listing, lang)
    
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
        "fr": {
            "title": "Exposé immobilier",
            "price": "Prix",
            "size": "Surface habitable",
            "plot": "Terrain",
            "rooms": "Pièces",
            "bedrooms": "Chambres",
            "bathrooms": "Salles de bain",
            "type": "Type de bien",
            "status": "Statut",
            "location": "Emplacement",
            "description": "Description",
            "features": "Caractéristiques",
            "contact": "Contact",
            "phone": "Téléphone",
            "email": "E-mail",
            "print": "Imprimer",
            "share": "Partager",
            "scan_qr": "Scannez le code QR pour voir en ligne",
            "generated": "Généré via",
            "sale": "À vendre",
            "rent": "À louer",
        },
        "nl": {
            "title": "Woningbrochure",
            "price": "Prijs",
            "size": "Woonoppervlak",
            "plot": "Perceel",
            "rooms": "Kamers",
            "bedrooms": "Slaapkamers",
            "bathrooms": "Badkamers",
            "type": "Type woning",
            "status": "Status",
            "location": "Locatie",
            "description": "Beschrijving",
            "features": "Kenmerken",
            "contact": "Contact",
            "phone": "Telefoon",
            "email": "E-mail",
            "print": "Afdrukken",
            "share": "Delen",
            "scan_qr": "Scan QR-code voor online weergave",
            "generated": "Gegenereerd via",
            "sale": "Te koop",
            "rent": "Te huur",
        },
        "pl": {
            "title": "Prospekt nieruchomości",
            "price": "Cena",
            "size": "Powierzchnia mieszkalna",
            "plot": "Działka",
            "rooms": "Pokoje",
            "bedrooms": "Sypialnie",
            "bathrooms": "Łazienki",
            "type": "Typ nieruchomości",
            "status": "Status",
            "location": "Lokalizacja",
            "description": "Opis",
            "features": "Cechy",
            "contact": "Kontakt",
            "phone": "Telefon",
            "email": "E-mail",
            "print": "Drukuj",
            "share": "Udostępnij",
            "scan_qr": "Zeskanuj kod QR aby zobaczyć online",
            "generated": "Wygenerowano przez",
            "sale": "Na sprzedaż",
            "rent": "Do wynajęcia",
        },
        "cz": {
            "title": "Prospekt nemovitosti",
            "price": "Cena",
            "size": "Obytná plocha",
            "plot": "Pozemek",
            "rooms": "Pokoje",
            "bedrooms": "Ložnice",
            "bathrooms": "Koupelny",
            "type": "Typ nemovitosti",
            "status": "Stav",
            "location": "Poloha",
            "description": "Popis",
            "features": "Vlastnosti",
            "contact": "Kontakt",
            "phone": "Telefon",
            "email": "E-mail",
            "print": "Tisk",
            "share": "Sdílet",
            "scan_qr": "Naskenujte QR kód pro online zobrazení",
            "generated": "Vygenerováno přes",
            "sale": "Na prodej",
            "rent": "K pronájmu",
        },
        "sk": {
            "title": "Prospekt nehnuteľnosti",
            "price": "Cena",
            "size": "Obytná plocha",
            "plot": "Pozemok",
            "rooms": "Izby",
            "bedrooms": "Spálne",
            "bathrooms": "Kúpeľne",
            "type": "Typ nehnuteľnosti",
            "status": "Stav",
            "location": "Poloha",
            "description": "Popis",
            "features": "Vlastnosti",
            "contact": "Kontakt",
            "phone": "Telefón",
            "email": "E-mail",
            "print": "Tlač",
            "share": "Zdieľať",
            "scan_qr": "Naskenujte QR kód pre online zobrazenie",
            "generated": "Vygenerované cez",
            "sale": "Na predaj",
            "rent": "Na prenájom",
        },
        "ru": {
            "title": "Буклет недвижимости",
            "price": "Цена",
            "size": "Жилая площадь",
            "plot": "Участок",
            "rooms": "Комнаты",
            "bedrooms": "Спальни",
            "bathrooms": "Ванные",
            "type": "Тип недвижимости",
            "status": "Статус",
            "location": "Расположение",
            "description": "Описание",
            "features": "Особенности",
            "contact": "Контакт",
            "phone": "Телефон",
            "email": "E-mail",
            "print": "Печать",
            "share": "Поделиться",
            "scan_qr": "Сканируйте QR-код для онлайн просмотра",
            "generated": "Создано через",
            "sale": "Продажа",
            "rent": "Аренда",
        },
        "gr": {
            "title": "Φυλλάδιο ακινήτου",
            "price": "Τιμή",
            "size": "Επιφάνεια",
            "plot": "Οικόπεδο",
            "rooms": "Δωμάτια",
            "bedrooms": "Υπνοδωμάτια",
            "bathrooms": "Μπάνια",
            "type": "Τύπος ακινήτου",
            "status": "Κατάσταση",
            "location": "Τοποθεσία",
            "description": "Περιγραφή",
            "features": "Χαρακτηριστικά",
            "contact": "Επικοινωνία",
            "phone": "Τηλέφωνο",
            "email": "E-mail",
            "print": "Εκτύπωση",
            "share": "Κοινοποίηση",
            "scan_qr": "Σαρώστε τον κωδικό QR για online προβολή",
            "generated": "Δημιουργήθηκε μέσω",
            "sale": "Πωλείται",
            "rent": "Ενοικιάζεται",
        },
        "sw": {
            "title": "Fastighetsbroschyr",
            "price": "Pris",
            "size": "Boarea",
            "plot": "Tomt",
            "rooms": "Rum",
            "bedrooms": "Sovrum",
            "bathrooms": "Badrum",
            "type": "Fastighetstyp",
            "status": "Status",
            "location": "Plats",
            "description": "Beskrivning",
            "features": "Egenskaper",
            "contact": "Kontakt",
            "phone": "Telefon",
            "email": "E-post",
            "print": "Skriv ut",
            "share": "Dela",
            "scan_qr": "Skanna QR-koden för online visning",
            "generated": "Genererad via",
            "sale": "Till salu",
            "rent": "Att hyra",
        },
        "no": {
            "title": "Eiendomsbrosjyre",
            "price": "Pris",
            "size": "Boligareal",
            "plot": "Tomt",
            "rooms": "Rom",
            "bedrooms": "Soverom",
            "bathrooms": "Bad",
            "type": "Eiendomstype",
            "status": "Status",
            "location": "Beliggenhet",
            "description": "Beskrivelse",
            "features": "Egenskaper",
            "contact": "Kontakt",
            "phone": "Telefon",
            "email": "E-post",
            "print": "Skriv ut",
            "share": "Del",
            "scan_qr": "Skann QR-koden for online visning",
            "generated": "Generert via",
            "sale": "Til salgs",
            "rent": "Til leie",
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
