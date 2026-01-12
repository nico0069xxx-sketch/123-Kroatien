# -*- coding: utf-8 -*-
"""Automatska provjera podataka o nekretninama"""

# Gueltige Regionen (erweitert)
VALID_LOCATIONS = [
    # Deutsche Namen
    'Istrien', 'Primorje', 'Lika-Senj', 'Zadar', 'Sibenik-Knin',
    'Split-Dalmatien', 'Dubrovnik-Neretva', 'Karlovac', 
    'Gespanschaft Zagreb', 'Stadt Zagreb', 'Krapina-Zagorje',
    'Varazdin', 'Koprivnica-Krizevci', 'Bjelovar-Bilogora',
    'Virovitica-Podravina', 'Pozega-Slawonien', 'Brod-Posavina',
    'Osijek-Baranja', 'Vukovar-Syrmien', 'Medimurje',
    # Staedte (wichtig!)
    'Split', 'Dubrovnik', 'Zagreb', 'Rijeka', 'Pula', 'Zadar',
    'Opatija', 'Rovinj', 'Porec', 'Umag', 'Sibenik', 'Trogir',
    'Makarska', 'Hvar', 'Korcula', 'Brac', 'Vis', 'Krk', 'Cres',
    'Losinj', 'Rab', 'Pag', 'Vodice', 'Primosten', 'Cavtat',
    'Mlini', 'Slano', 'Ston', 'Novalja', 'Nin', 'Biograd',
    # Kroatische Regionsnamen
    'Istra', 'Dalmacija', 'Slavonija', 'Hrvatsko Zagorje',
    'Kvarner', 'Lika', 'Gorski Kotar', 'Medimurje',
]

VALID_PROPERTY_TYPES = [
    'House', 'Appartment', 'New Building', 'Property', 'Villa',
    'Haus', 'Wohnung', 'Neubau', 'Grundstueck', 'Grundstück',
    'Kuca', 'Stan', 'Novogradnja', 'Zemljiste', 'Vila',
    'Apartment', 'Land', 'Office', 'Commercial',
]

VALID_STATUS = [
    'Sale', 'Rent', 'For Sale', 'For Rent',
    'Verkauf', 'Miete', 'Zu verkaufen', 'Zu vermieten',
    'Prodaja', 'Najam', 'Na prodaju', 'Za najam',
]


def validate_listing(listing):
    """Provjerava nekretninu. Vraca listu gresaka."""
    fehler = []
    
    # 1. Tip nekretnine
    if not listing.property_type:
        fehler.append("Nedostaje tip nekretnine (kuca, stan, zemljiste...)")
    elif listing.property_type not in VALID_PROPERTY_TYPES:
        fehler.append(f"Nepoznat tip nekretnine: {listing.property_type}")
    
    # 2. Prodaja/Najam
    if not listing.property_status:
        fehler.append("Nedostaje status (prodaja ili najam)")
    elif listing.property_status not in VALID_STATUS:
        fehler.append(f"Nepoznat status: {listing.property_status}")
    
    # 3. Lokacija (flexibel)
    if not listing.location:
        fehler.append("Nedostaje lokacija/regija")
    else:
        # Sehr flexible Pruefung
        loc = listing.location.lower().strip()
        valid = [v.lower() for v in VALID_LOCATIONS]
        if loc not in valid:
            # Pruefe ob Teil einer gueltigen Region
            gefunden = False
            for v in valid:
                if loc in v or v in loc:
                    gefunden = True
                    break
            if not gefunden and len(loc) < 3:
                fehler.append(f"Nepoznata lokacija: {listing.location}")
    
    # 4. Povrsina
    if not listing.area or listing.area <= 0:
        fehler.append("Nedostaje povrsina (m2)")
    
    # 5. Spavace sobe
    if listing.bedrooms is None:
        fehler.append("Nedostaje broj spavacih soba")
    
    # 6. Kupaonice
    if listing.bathrooms is None:
        fehler.append("Nedostaje broj kupaonica")
    
    # 7. Cijena
    if not listing.property_price or listing.property_price <= 0:
        fehler.append("Nedostaje cijena")
    
    # 8. Fotografija
    if not listing.photo_main:
        fehler.append("Nedostaje glavna fotografija")
    
    # 9. Opis (min 80 Zeichen ODER 3 Saetze)
    opis = listing.property_description or ""
    if len(opis) < 80:
        recenice = len([s for s in opis.replace('!', '.').replace('?', '.').split('.') if s.strip()])
        if recenice < 3:
            fehler.append(f"Opis prekratak ({len(opis)} znakova) - potrebno min. 80 znakova ili 3 recenice")
    
    # 10. Naslov
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
