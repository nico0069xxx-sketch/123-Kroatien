from django.http import HttpResponse
from django.views.decorators.http import require_GET
from listings.models import Listing
from datetime import datetime
import xml.etree.ElementTree as ET
from xml.dom import minidom

def prettify_xml(elem):
    """Return a pretty-printed XML string."""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


@require_GET
def openimmo_export(request):
    """
    OpenImmo XML Export - Deutscher Standard
    """
    # Root Element
    openimmo = ET.Element('openimmo')
    openimmo.set('xmlns', 'http://www.openimmo.de')
    
    # Anbieter
    anbieter = ET.SubElement(openimmo, 'anbieter')
    
    anbieternr = ET.SubElement(anbieter, 'anbieternr')
    anbieternr.text = '123-KROATIEN'
    
    firma = ET.SubElement(anbieter, 'firma')
    firma.text = '123-kroatien.eu'
    
    openimmo_anid = ET.SubElement(anbieter, 'openimmo_anid')
    openimmo_anid.text = '123KROATIEN'
    
    # Immobilien
    listings = Listing.objects.filter(is_published=True)
    
    for listing in listings:
        immobilie = ET.SubElement(anbieter, 'immobilie')
        
        # Objektkategorie
        objektkategorie = ET.SubElement(immobilie, 'objektkategorie')
        
        nutzungsart = ET.SubElement(objektkategorie, 'nutzungsart')
        nutzungsart.set('WOHNEN', 'true' if listing.property_type in ['House', 'Appartment', 'Haus', 'Wohnung', 'Neubau'] else 'false')
        nutzungsart.set('GEWERBE', 'true' if listing.property_type == 'Office' else 'false')
        
        vermarktungsart = ET.SubElement(objektkategorie, 'vermarktungsart')
        vermarktungsart.set('KAUF', 'true' if listing.property_status == 'Sale' else 'false')
        vermarktungsart.set('MIETE_PACHT', 'true' if listing.property_status == 'Rent' else 'false')
        
        objektart = ET.SubElement(objektkategorie, 'objektart')
        if listing.property_type in ['House', 'Haus']:
            haus = ET.SubElement(objektart, 'haus')
            haus.set('haustyp', 'EINFAMILIENHAUS')
        elif listing.property_type in ['Appartment', 'Wohnung']:
            wohnung = ET.SubElement(objektart, 'wohnung')
            wohnung.set('wohnungtyp', 'ETAGE')
        elif listing.property_type in ['Grundstueck', 'Grundstück']:
            grundstueck = ET.SubElement(objektart, 'grundstueck')
            grundstueck.set('grundst_typ', 'WOHNEN')
        elif listing.property_type == 'Neubau':
            haus = ET.SubElement(objektart, 'haus')
            haus.set('haustyp', 'NEUBAU')
        else:
            haus = ET.SubElement(objektart, 'haus')
        
        # Geo
        geo = ET.SubElement(immobilie, 'geo')
        
        plz = ET.SubElement(geo, 'plz')
        plz.text = listing.zipcode or ''
        
        ort = ET.SubElement(geo, 'ort')
        ort.text = listing.city or ''
        
        strasse = ET.SubElement(geo, 'strasse')
        strasse.text = listing.address or ''
        
        land = ET.SubElement(geo, 'land')
        land.set('iso_land', 'HRV')
        land.text = 'Kroatien'
        
        # Kontaktperson
        kontaktperson = ET.SubElement(immobilie, 'kontaktperson')
        
        name_kontakt = ET.SubElement(kontaktperson, 'name')
        name_kontakt.text = str(listing.realtor) if listing.realtor else '123-kroatien.eu'
        
        email_kontakt = ET.SubElement(kontaktperson, 'email_zentrale')
        email_kontakt.text = listing.email or 'office@123-kroatien.eu'
        
        # Preise
        preise = ET.SubElement(immobilie, 'preise')
        
        kaufpreis = ET.SubElement(preise, 'kaufpreis')
        kaufpreis.set('auf_anfrage', 'false')
        kaufpreis.text = str(listing.property_price) if listing.property_price else '0'
        
        waehrung = ET.SubElement(preise, 'waehrung')
        waehrung.set('iso_waehrung', 'EUR')
        
        # Flächen
        flaechen = ET.SubElement(immobilie, 'flaechen')
        
        wohnflaeche = ET.SubElement(flaechen, 'wohnflaeche')
        wohnflaeche.text = str(listing.size) if listing.size else '0'
        
        grundstuecksflaeche = ET.SubElement(flaechen, 'grundstuecksflaeche')
        grundstuecksflaeche.text = str(listing.area) if listing.area else '0'
        
        anzahl_zimmer = ET.SubElement(flaechen, 'anzahl_zimmer')
        anzahl_zimmer.text = str(listing.bedrooms) if listing.bedrooms else '0'
        
        anzahl_badezimmer = ET.SubElement(flaechen, 'anzahl_badezimmer')
        anzahl_badezimmer.text = str(listing.bathrooms) if listing.bathrooms else '0'
        
        # Freitexte
        freitexte = ET.SubElement(immobilie, 'freitexte')
        
        objekttitel = ET.SubElement(freitexte, 'objekttitel')
        objekttitel.text = listing.property_title or ''
        
        objektbeschreibung = ET.SubElement(freitexte, 'objektbeschreibung')
        objektbeschreibung.text = listing.property_description or ''
        
        # Anhaenge (Bilder)
        anhaenge = ET.SubElement(immobilie, 'anhaenge')
        
        if listing.photo_main:
            anhang = ET.SubElement(anhaenge, 'anhang')
            anhang.set('location', 'EXTERN')
            anhang.set('gruppe', 'BILD')
            
            anhangtitel = ET.SubElement(anhang, 'anhangtitel')
            anhangtitel.text = 'Hauptbild'
            
            format_elem = ET.SubElement(anhang, 'format')
            format_elem.text = 'image/jpeg'
            
            daten = ET.SubElement(anhang, 'daten')
            pfad = ET.SubElement(daten, 'pfad')
            pfad.text = f'https://123-kroatien.eu{listing.photo_main.url}'
        
        # Verwaltung Techn
        verwaltung_techn = ET.SubElement(immobilie, 'verwaltung_techn')
        
        objektnr_intern = ET.SubElement(verwaltung_techn, 'objektnr_intern')
        objektnr_intern.text = str(listing.id)
        
        objektnr_extern = ET.SubElement(verwaltung_techn, 'objektnr_extern')
        objektnr_extern.text = f'123KRO-{listing.id}'
        
        stand_vom = ET.SubElement(verwaltung_techn, 'stand_vom')
        stand_vom.text = datetime.now().strftime('%Y-%m-%d')
    
    xml_string = prettify_xml(openimmo)
    
    response = HttpResponse(xml_string, content_type='application/xml; charset=utf-8')
    response['Content-Disposition'] = 'inline; filename="openimmo_export.xml"'
    return response


@require_GET
def croatia_simple_export(request):
    """
    Einfache Kroatien XML-Schnittstelle
    Für kroatische Makler
    """
    # Root Element
    root = ET.Element('nekretnine')
    root.set('portal', '123-kroatien.eu')
    root.set('datum', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    root.set('verzija', '1.0')
    
    # Portal Info
    portal_info = ET.SubElement(root, 'portal_info')
    
    naziv = ET.SubElement(portal_info, 'naziv')
    naziv.text = '123-kroatien.eu'
    
    email = ET.SubElement(portal_info, 'email')
    email.text = 'office@123-kroatien.eu'
    
    web = ET.SubElement(portal_info, 'web')
    web.text = 'https://123-kroatien.eu'
    
    # Immobilien
    listings = Listing.objects.filter(is_published=True)
    
    nekretnine_lista = ET.SubElement(root, 'nekretnine_lista')
    nekretnine_lista.set('ukupno', str(listings.count()))
    
    for listing in listings:
        nekretnina = ET.SubElement(nekretnine_lista, 'nekretnina')
        nekretnina.set('id', str(listing.id))
        
        # Basis Info
        naslov = ET.SubElement(nekretnina, 'naslov')
        naslov.text = listing.property_title or ''
        
        opis = ET.SubElement(nekretnina, 'opis')
        opis.text = listing.property_description or ''
        
        # Tip
        tip = ET.SubElement(nekretnina, 'tip')
        type_mapping = {
            'House': 'kuca', 'Haus': 'kuca',
            'Appartment': 'stan', 'Wohnung': 'stan',
            'Neubau': 'novogradnja',
            'Grundstueck': 'zemljiste', 'Grundstück': 'zemljiste',
            'Villa': 'vila', 'Office': 'poslovni_prostor'
        }
        tip.text = type_mapping.get(listing.property_type, 'ostalo')
        
        # Status
        status = ET.SubElement(nekretnina, 'status')
        status.text = 'prodaja' if listing.property_status == 'Sale' else 'najam'
        
        # Cijena
        cijena = ET.SubElement(nekretnina, 'cijena')
        cijena.set('valuta', 'EUR')
        cijena.text = str(listing.property_price) if listing.property_price else '0'
        
        # Lokacija
        lokacija = ET.SubElement(nekretnina, 'lokacija')
        
        grad = ET.SubElement(lokacija, 'grad')
        grad.text = listing.city or ''
        
        adresa = ET.SubElement(lokacija, 'adresa')
        adresa.text = listing.address or ''
        
        postanski_broj = ET.SubElement(lokacija, 'postanski_broj')
        postanski_broj.text = listing.zipcode or ''
        
        drzava = ET.SubElement(lokacija, 'drzava')
        drzava.text = 'Hrvatska'
        
        # Povrsina
        povrsina = ET.SubElement(nekretnina, 'povrsina')
        
        stambena = ET.SubElement(povrsina, 'stambena_povrsina')
        stambena.set('jedinica', 'm2')
        stambena.text = str(listing.size) if listing.size else '0'
        
        zemljiste_pov = ET.SubElement(povrsina, 'povrsina_zemljista')
        zemljiste_pov.set('jedinica', 'm2')
        zemljiste_pov.text = str(listing.area) if listing.area else '0'
        
        # Sobe
        sobe = ET.SubElement(nekretnina, 'sobe')
        
        spavace = ET.SubElement(sobe, 'spavace_sobe')
        spavace.text = str(listing.bedrooms) if listing.bedrooms else '0'
        
        kupaonice = ET.SubElement(sobe, 'kupaonice')
        kupaonice.text = str(listing.bathrooms) if listing.bathrooms else '0'
        
        # Slike
        slike = ET.SubElement(nekretnina, 'slike')
        
        if listing.photo_main:
            slika = ET.SubElement(slike, 'slika')
            slika.set('glavna', 'true')
            slika.text = f'https://123-kroatien.eu{listing.photo_main.url}'
        
        # Kontakt
        kontakt = ET.SubElement(nekretnina, 'kontakt')
        
        agent_ime = ET.SubElement(kontakt, 'ime')
        agent_ime.text = str(listing.realtor) if listing.realtor else '123-kroatien.eu'
        
        agent_email = ET.SubElement(kontakt, 'email')
        agent_email.text = listing.email or 'office@123-kroatien.eu'
        
        # Link
        link = ET.SubElement(nekretnina, 'link')
        link.text = f'https://123-kroatien.eu/ge/listing/{listing.id}/'
    
    xml_string = prettify_xml(root)
    
    response = HttpResponse(xml_string, content_type='application/xml; charset=utf-8')
    response['Content-Disposition'] = 'inline; filename="croatia_export.xml"'
    return response
