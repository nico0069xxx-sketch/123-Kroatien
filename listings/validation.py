# -*- coding: utf-8 -*-
"""Automatska provjera podataka o nekretninama / Automatische Pruefung"""

# Gueltige kroatische Regionen
VALID_LOCATIONS = [
    'Istrien', 'Primorje', 'Lika-Senj', 'Zadar', 'Sibenik-Knin',
    'Split-Dalmatien', 'Dubrovnik-Neretva', 'Karlovac', 
    'Gespanschaft Zagreb', 'Stadt Zagreb', 'Krapina-Zagorje',
    'Varazdin', 'Koprivnica-Krizevci', 'Bjelovar-Bilogora',
    'Virovitica-Podravina', 'Pozega-Slawonien', 'Brod-Posavina',
    'Osijek-Baranja', 'Vukovar-Syrmien', 'Medimurje',
    # Mit Sonderzeichen
    'Sibenik-Knin', 'Pozega-Slawonien', 'Medimurje', 'Varazdin',
    'Koprivnica-Krizevci',
    # Kroatische Namen
    'Istra', 'Primorsko-goranska', 'Licko-senjska', 'Zadarska',
    'Sibensko-kninska', 'Splitsko-dalmatinska', 'Dubrovacko-neretvanska',
    'Karlovacka', 'Zagrebacka', 'Grad Zagreb', 'Krapinsko-zagorska',
    'Varazdinska', 'Koprivnicko-krizevacka', 'Bjelovarsko-bilogorska',
    'Viroviticko-podravska', 'Pozesko-slavonska', 'Brodsko-posavska',
    'Osjecko-baranjska', 'Vukovarsko-srijemska', 'Medimurska',
]

VALID_PROPERTY_TYPES = ['House', 'Appartment', 'New Building', 'Property', 
                        'Haus', 'Wohnung', 'Neubau', 'Grundstueck', 'Villa',
                        'Kuca', 'Stan', 'Novogradnja', 'Zemljiste']

VALID_STATUS = ['Sale', 'Rent', 'Verkauf', 'Miete', 'Prodaja', 'Najam']


def validate_listing(listing):
    """
    Provjerava nekretninu. Vraca listu gresaka (prazna = sve OK).
    """
    fehler = []
    
    # 1. Tip nekretnine / Immobilientyp
    if not listing.property_type:
        fehler.append("Nedostaje tip nekretnine (kuca, stan, zemljiste...)")
    elif listing.property_type not in VALID_PROPERTY_TYPES:
        fehler.append(f"Nepoznat tip nekretnine: {listing.property_type}")
    
    # 2. Prodaja/Najam
    if not listing.property_status:
        fehler.append("Nedostaje status (prodaja ili najam)")
    elif listing.property_status not in VALID_STATUS:
        fehler.append(f"Nepoznat status: {listing.property_status}")
    
    # 3. Lokacija / Region
    if not listing.location:
        fehler.append("Nedostaje lokacija/regija")
    else:
        location_lower = listing.location.lower().replace('š', 's').replace('ć', 'c').replace('č', 'c').replace('ž', 'z').replace('đ', 'd')
        valid_lower = [loc.lower().replace('š', 's').replace('ć', 'c').replace('č', 'c').replace('ž', 'z').replace('đ', 'd') for loc in VALID_LOCATIONS]
        if location_lower not in valid_lower:
            fehler.append(f"Nepoznata regija: {listing.location}")
    
    # 4. Povrsina / Flaeche
    if not listing.area or listing.area <= 0:
        fehler.append("Nedostaje povrsina zemljista (m2)")
    
    # 5. Spavace sobe / Schlafzimmer
    if listing.bedrooms is None:
        fehler.append("Nedostaje broj spavacih soba")
    elif listing.bedrooms < 0 or listing.bedrooms > 20:
        fehler.append(f"Neispravan broj spavacih soba: {listing.bedrooms}")
    
    # 6. Kupaonice / Badezimmer
    if listing.bathrooms is None:
        fehler.append("Nedostaje broj kupaonica")
    elif listing.bathrooms < 0 or listing.bathrooms > 10:
        fehler.append(f"Neispravan broj kupaonica: {listing.bathrooms}")
    
    # 7. Cijena / Preis
    if not listing.property_price or listing.property_price <= 0:
        fehler.append("Nedostaje cijena")
    
    # 8. Fotografija / Foto
    if not listing.photo_main:
        fehler.append("Nedostaje glavna fotografija")
    
    # 9. Opis / Beschreibung (min 80 znakova ILI 3 recenice)
    opis = listing.property_description or ""
    if len(opis) < 80:
        recenice = len([s for s in opis.replace('!', '.').replace('?', '.').split('.') if s.strip()])
        if recenice < 3:
            fehler.append(f"Opis prekratak ({len(opis)} znakova, {recenice} recenica) - potrebno min. 80 znakova ili 3 recenice")
    
    # 10. Naslov / Titel
    if not listing.property_title or len(listing.property_title) < 5:
        fehler.append("Nedostaje naslov ili je prekratak")
    
    return fehler


def check_and_update_listing(listing):
    """Provjerava listing i postavlja status."""
    fehler = validate_listing(listing)
    
    if fehler:
        listing.pruefung_fehler = "\n".join(fehler)
        listing.listing_status = 'pruefung'
        listing.is_published = False
    else:
        listing.pruefung_fehler = None
    
    listing.save()
    return fehler
