# XML Export für Django Immobilien-Marktplatz
# OpenImmo 1.2.7 Standard + Einfaches XML-Format

from xml.etree.ElementTree import Element, SubElement, tostring
from xml.dom import minidom
from datetime import datetime


class OpenImmoXMLGenerator:
    """
    Generator für OpenImmo 1.2.7 XML-Format
    Standard für Immobilien-Exporte in DACH-Region
    """
    
    def __init__(self, listings, base_url=""):
        self.listings = listings
        self.base_url = base_url
        
    def generate(self):
        """Generiert OpenImmo XML für alle Listings"""
        
        # Root Element
        openimmo = Element('openimmo')
        openimmo.set('xmlns', 'http://www.openimmo.de')
        openimmo.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        openimmo.set('xsi:schemaLocation', 'http://www.openimmo.de openimmo_127b.xsd')
        
        # Uebertragung (Metadata)
        uebertragung = SubElement(openimmo, 'uebertragung')
        SubElement(uebertragung, 'art').text = 'ONLINE'
        SubElement(uebertragung, 'umfang').text = 'VOLL'
        SubElement(uebertragung, 'modus').text = 'NEW'
        SubElement(uebertragung, 'version').text = '1.2.7'
        SubElement(uebertragung, 'sendersoftware').text = 'Kroatien Immobilien Marktplatz'
        SubElement(uebertragung, 'senderversion').text = '1.0'
        SubElement(uebertragung, 'techn_email').text = 'office@123-kroatien.eu'
        SubElement(uebertragung, 'timestamp').text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Anbieter
        anbieter = SubElement(openimmo, 'anbieter')
        
        # Gruppiere Listings nach Makler
        listings_by_agent = {}
        for listing in self.listings:
            agent_id = listing.realtor.id if listing.realtor else 'no_agent'
            if agent_id not in listings_by_agent:
                listings_by_agent[agent_id] = []
            listings_by_agent[agent_id].append(listing)
        
        # Für jeden Makler
        for agent_id, agent_listings in listings_by_agent.items():
            if agent_id == 'no_agent':
                continue
                
            listing = agent_listings[0]
            agent = listing.realtor
            
            # Anbieternummer
            SubElement(anbieter, 'anbieternr').text = str(agent.oib_number) if agent.oib_number else str(agent.id)
            
            # Firma
            firma = SubElement(anbieter, 'firma')
            SubElement(firma, 'name').text = agent.company_name or f"{agent.first_name} {agent.last_name}"
            if agent.oib_number:
                SubElement(firma, 'lizenzkennung').text = agent.oib_number
            
            # Anhang (Logo)
            if agent.company_logo:
                anhang = SubElement(anbieter, 'anhang')
                SubElement(anhang, 'anhangtitel').text = 'Logo'
                SubElement(anhang, 'format').text = 'jpg'
                daten = SubElement(anhang, 'daten')
                SubElement(daten, 'pfad').text = f"{self.base_url}{agent.company_logo.url}"
            
            # Immobilien des Maklers
            for listing in agent_listings:
                self._add_immobilie(anbieter, listing)
        
        return self._prettify(openimmo)
    
    def _add_immobilie(self, anbieter, listing):
        """Fügt eine Immobilie zum XML hinzu"""
        
        immobilie = SubElement(anbieter, 'immobilie')
        
        # Verwaltung Techn
        verwaltung_techn = SubElement(immobilie, 'verwaltung_techn')
        SubElement(verwaltung_techn, 'objektnr_intern').text = str(listing.property_id) if listing.property_id else str(listing.id)
        SubElement(verwaltung_techn, 'objektnr_extern').text = str(listing.id)
        SubElement(verwaltung_techn, 'aktion').text = 'CHANGE' if listing.is_published else 'DELETE'
        SubElement(verwaltung_techn, 'aktiv_von').text = listing.list_date.strftime('%Y-%m-%d') if listing.list_date else ''
        SubElement(verwaltung_techn, 'openimmo_obid').text = str(listing.id)
        SubElement(verwaltung_techn, 'sprache').text = 'HRV'  # Kroatisch
        
        # Objektkategorie
        objektkategorie = SubElement(immobilie, 'objektkategorie')
        nutzungsart = SubElement(objektkategorie, 'nutzungsart')
        
        # Typ basierend auf property_type
        property_type = (listing.property_type or '').lower()
        if 'house' in property_type or 'villa' in property_type:
            SubElement(nutzungsart, 'wohnen').set('HAUS', 'true')
        elif 'apartment' in property_type:
            SubElement(nutzungsart, 'wohnen').set('WOHNUNG', 'true')
        elif 'office' in property_type:
            SubElement(nutzungsart, 'gewerbe').set('BUERO_PRAXEN', 'true')
        else:
            SubElement(nutzungsart, 'wohnen').set('HAUS', 'true')
        
        # Vermarktungsart
        vermarktungsart = SubElement(objektkategorie, 'vermarktungsart')
        if listing.property_status and 'rent' in listing.property_status.lower():
            SubElement(vermarktungsart, 'miete_pacht').set('miete_pacht', 'true')
        else:
            SubElement(vermarktungsart, 'kauf').set('kauf', 'true')
        
        # Objektart
        objektart = SubElement(objektkategorie, 'objektart')
        if 'house' in property_type or 'villa' in property_type:
            SubElement(objektart, 'haus').set('haustyp', 'EINFAMILIENHAUS')
        elif 'apartment' in property_type:
            SubElement(objektart, 'wohnung').set('wohnungtyp', 'ETAGE')
        
        # Geo (Adresse)
        geo = SubElement(immobilie, 'geo')
        SubElement(geo, 'plz').text = listing.zipcode or ''
        SubElement(geo, 'ort').text = listing.city or ''
        SubElement(geo, 'strasse').text = listing.address or ''
        SubElement(geo, 'land').set('iso_land', 'HRV')  # Kroatien
        SubElement(geo, 'regionaler_zusatz').text = listing.state or ''
        
        # Geokoordinaten (optional, wenn verfügbar)
        # geokoordinaten = SubElement(geo, 'geokoordinaten')
        # SubElement(geokoordinaten, 'breitengrad').text = ''
        # SubElement(geokoordinaten, 'laengengrad').text = ''
        
        # Kontaktperson
        kontaktperson = SubElement(immobilie, 'kontaktperson')
        if listing.realtor:
            SubElement(kontaktperson, 'name').text = f"{listing.realtor.first_name} {listing.realtor.last_name}"
            SubElement(kontaktperson, 'email_zentrale').text = listing.email or listing.realtor.email
            if listing.realtor.mobile:
                SubElement(kontaktperson, 'tel_handy').text = listing.realtor.mobile
            SubElement(kontaktperson, 'firma').text = listing.company_name or listing.realtor.company_name
        
        # Preise
        preise = SubElement(immobilie, 'preise')
        if listing.property_status and 'rent' in listing.property_status.lower():
            SubElement(preise, 'nettokaltmiete').text = str(listing.property_price)
            SubElement(preise, 'waehrung').set('iso_waehrung', 'EUR')
        else:
            SubElement(preise, 'kaufpreis').text = str(listing.property_price)
            SubElement(preise, 'waehrung').set('iso_waehrung', 'EUR')
        
        # Flaechen
        flaechen = SubElement(immobilie, 'flaechen')
        if listing.size:
            SubElement(flaechen, 'wohnflaeche').text = str(listing.size)
        if listing.area:
            SubElement(flaechen, 'grundstuecksflaeche').text = str(listing.area)
        if listing.bedrooms:
            SubElement(flaechen, 'anzahl_zimmer').text = str(listing.bedrooms)
        if listing.bathrooms:
            SubElement(flaechen, 'anzahl_badezimmer').text = str(listing.bathrooms)
        
        # Ausstattung
        ausstattung = SubElement(immobilie, 'ausstattung')
        if listing.garage and listing.garage > 0:
            SubElement(ausstattung, 'anzahl_stellplaetze').text = str(listing.garage)
        
        # Zustand & Entwicklung
        zustand_angaben = SubElement(immobilie, 'zustand_angaben')
        # Optional: SubElement(zustand_angaben, 'baujahr').text = ''
        
        # Freitexte
        freitexte = SubElement(immobilie, 'freitexte')
        SubElement(freitexte, 'objekttitel').text = listing.property_title or ''
        
        beschreibung = SubElement(freitexte, 'objektbeschreibung')
        beschreibung.text = listing.property_description or ''
        
        if listing.location:
            SubElement(freitexte, 'lage').text = listing.location
        
        # Anhaenge (Bilder)
        if listing.photo_main:
            self._add_anhang(immobilie, listing.photo_main.url, 'Hauptbild', gruppe='BILD')
        
        for i, photo_field in enumerate(['photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6'], 1):
            photo = getattr(listing, photo_field, None)
            if photo:
                self._add_anhang(immobilie, photo.url, f'Bild {i}', gruppe='BILD')
        
        # Video
        if listing.video_url:
            self._add_anhang(immobilie, listing.video_url, 'Video', gruppe='FILM')
    
    def _add_anhang(self, immobilie, url, titel, gruppe='BILD'):
        """Fügt einen Anhang (Bild/Video) hinzu"""
        anhang = SubElement(immobilie, 'anhang')
        SubElement(anhang, 'anhangtitel').text = titel
        SubElement(anhang, 'format').text = url.split('.')[-1] if '.' in url else 'jpg'
        SubElement(anhang, 'gruppe').text = gruppe
        
        daten = SubElement(anhang, 'daten')
        SubElement(daten, 'pfad').text = f"{self.base_url}{url}"
    
    def _prettify(self, elem):
        """Formatiert XML schön"""
        rough_string = tostring(elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')


class SimpleXMLGenerator:
    """
    Einfacher XML-Generator als Alternative
    Leichter zu lesen und anzupassen
    """
    
    def __init__(self, listings, base_url=""):
        self.listings = listings
        self.base_url = base_url
    
    def generate(self):
        """Generiert einfaches XML für alle Listings"""
        
        root = Element('listings')
        root.set('version', '1.0')
        root.set('generated', datetime.now().isoformat())
        root.set('count', str(len(self.listings)))
        
        for listing in self.listings:
            self._add_listing(root, listing)
        
        return self._prettify(root)
    
    def _add_listing(self, root, listing):
        """Fügt ein Listing zum XML hinzu"""
        
        item = SubElement(root, 'listing')
        item.set('id', str(listing.id))
        item.set('published', str(listing.is_published).lower())
        
        # Basis-Informationen
        SubElement(item, 'property_id').text = str(listing.property_id) if listing.property_id else ''
        SubElement(item, 'title').text = listing.property_title or ''
        SubElement(item, 'description').text = listing.property_description or ''
        SubElement(item, 'type').text = listing.property_type or ''
        SubElement(item, 'status').text = listing.property_status or ''
        SubElement(item, 'location').text = listing.location or ''
        
        # Preis
        price = SubElement(item, 'price')
        price.set('currency', 'EUR')
        price.text = str(listing.property_price)
        
        # Details
        details = SubElement(item, 'details')
        SubElement(details, 'bedrooms').text = str(listing.bedrooms) if listing.bedrooms else '0'
        SubElement(details, 'bathrooms').text = str(listing.bathrooms) if listing.bathrooms else '0'
        SubElement(details, 'floors').text = str(listing.floors) if listing.floors else '0'
        SubElement(details, 'garage').text = str(listing.garage) if listing.garage else '0'
        SubElement(details, 'area').text = str(listing.area) if listing.area else '0'
        SubElement(details, 'size').text = str(listing.size) if listing.size else '0'
        
        # Adresse
        address = SubElement(item, 'address')
        SubElement(address, 'street').text = listing.address or ''
        SubElement(address, 'city').text = listing.city or ''
        SubElement(address, 'state').text = listing.state or ''
        SubElement(address, 'zipcode').text = listing.zipcode or ''
        SubElement(address, 'country').text = listing.country or 'Croatia'
        SubElement(address, 'neighborhood').text = listing.neighborhood or ''
        
        # Makler/Agent
        if listing.realtor:
            agent = SubElement(item, 'agent')
            SubElement(agent, 'name').text = f"{listing.realtor.first_name} {listing.realtor.last_name}"
            SubElement(agent, 'email').text = listing.email or listing.realtor.email or ''
            SubElement(agent, 'company').text = listing.company_name or listing.realtor.company_name or ''
            SubElement(agent, 'oib_number').text = listing.oib_number or listing.realtor.oib_number or ''
            SubElement(agent, 'domain').text = listing.domain or listing.realtor.domain or ''
            if listing.realtor.mobile:
                SubElement(agent, 'phone').text = listing.realtor.mobile
        
        # Bilder
        images = SubElement(item, 'images')
        if listing.photo_main:
            img = SubElement(images, 'image')
            img.set('type', 'main')
            img.text = f"{self.base_url}{listing.photo_main.url}"
        
        for i, photo_field in enumerate(['photo_1', 'photo_2', 'photo_3', 'photo_4', 'photo_5', 'photo_6'], 1):
            photo = getattr(listing, photo_field, None)
            if photo:
                img = SubElement(images, 'image')
                img.set('type', f'photo_{i}')
                img.text = f"{self.base_url}{photo.url}"
        
        # Video
        if listing.video_url:
            SubElement(item, 'video_url').text = listing.video_url
        
        # Datum
        SubElement(item, 'list_date').text = listing.list_date.isoformat() if listing.list_date else ''
    
    def _prettify(self, elem):
        """Formatiert XML schön"""
        rough_string = tostring(elem, encoding='utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding='utf-8').decode('utf-8')
