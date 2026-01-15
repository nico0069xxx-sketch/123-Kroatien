"""
XML Import Schnittstellen für 123-Kroatien.eu

1. OpenImmo Import - Standard für deutsche/österreichische Immobilienportale
2. Simple XML Import - Einfaches Format für WordPress-Seiten kroatischer Makler

Autor: 123-Kroatien.eu Team
"""

import xml.etree.ElementTree as ET
from django.db import transaction
from listings.models import Listing
from accounts.models import Agent
from main.professional_models import Professional
import os
import requests
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class OpenImmoImporter:
    """
    OpenImmo XML Import
    Standard-Format für Immobilien-Datenaustausch
    """
    
    # Mapping von OpenImmo-Objektarten zu unseren Typen
    OBJEKTART_MAPPING = {
        'zimmer': 'Apartment',
        'wohnung': 'Apartment',
        'haus': 'House',
        'grundstueck': 'Land',
        'buero_praxen': 'Commercial',
        'einzelhandel': 'Commercial',
        'gastgewerbe': 'Commercial',
        'hallen_lager_prod': 'Commercial',
        'land_und_forstwirtschaft': 'Land',
        'parken': 'Parking',
        'sonstige': 'Other',
        'freizeitimmobilie_gewerblich': 'Villa',
        'zinshaus_renditeobjekt': 'Commercial',
    }
    
    # Mapping von Vermarktungsart
    VERMARKTUNG_MAPPING = {
        'KAUF': 'For Sale',
        'MIETE': 'For Rent',
        'MIETE_PACHT': 'For Rent',
        'ERBPACHT': 'For Sale',
        'LEASING': 'For Rent',
    }
    
    def __init__(self, professional_id=None, agent_id=None):
        """
        Initialize with a professional or agent who owns the imported listings
        """
        self.professional = None
        self.agent = None
        
        if professional_id:
            try:
                self.professional = Professional.objects.get(id=professional_id)
            except Professional.DoesNotExist:
                logger.error(f"Professional {professional_id} nicht gefunden")
        
        if agent_id:
            try:
                self.agent = Agent.objects.get(id=agent_id)
            except Agent.DoesNotExist:
                logger.error(f"Agent {agent_id} nicht gefunden")
    
    def parse_file(self, file_path):
        """Parse OpenImmo XML file"""
        try:
            tree = ET.parse(file_path)
            return tree.getroot()
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            return None
    
    def parse_string(self, xml_string):
        """Parse OpenImmo XML string"""
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            return None
    
    def _get_text(self, element, path, default=''):
        """Safely get text from XML element"""
        if element is None:
            return default
        found = element.find(path)
        if found is not None and found.text:
            return found.text.strip()
        return default
    
    def _get_attr(self, element, path, attr, default=''):
        """Safely get attribute from XML element"""
        if element is None:
            return default
        found = element.find(path)
        if found is not None:
            return found.get(attr, default)
        return default
    
    def _get_float(self, element, path, default=0.0):
        """Safely get float from XML element"""
        text = self._get_text(element, path)
        try:
            return float(text.replace(',', '.')) if text else default
        except ValueError:
            return default
    
    def _get_int(self, element, path, default=0):
        """Safely get int from XML element"""
        text = self._get_text(element, path)
        try:
            return int(float(text.replace(',', '.'))) if text else default
        except ValueError:
            return default
    
    def extract_property(self, immobilie_elem):
        """
        Extract property data from an <immobilie> element
        Returns dict with Listing model fields
        """
        data = {}
        
        # Geo-Daten
        geo = immobilie_elem.find('.//geo')
        if geo is not None:
            data['zipcode'] = self._get_text(geo, 'plz')
            data['city'] = self._get_text(geo, 'ort')
            data['state'] = self._get_text(geo, 'bundesland')
            data['address'] = self._get_text(geo, 'strasse')
            data['neighborhood'] = self._get_text(geo, 'regionaler_zusatz')
            data['country'] = self._get_text(geo, 'land/iso_land') or 'Kroatien'
        
        # Kontakt/Anbieter
        kontakt = immobilie_elem.find('.//kontaktperson')
        if kontakt is not None:
            data['anbieter_name'] = self._get_text(kontakt, 'name')
            data['anbieter_email'] = self._get_text(kontakt, 'email_direkt')
            data['anbieter_telefon'] = self._get_text(kontakt, 'tel_durchw')
        
        # Objektart bestimmen
        objektart_elem = immobilie_elem.find('.//objektart')
        if objektart_elem is not None:
            for child in objektart_elem:
                objektart = child.tag.lower()
                data['type'] = self.OBJEKTART_MAPPING.get(objektart, 'Other')
                break
        
        # Vermarktungsart
        vermarktung = immobilie_elem.find('.//vermarktungsart')
        if vermarktung is not None:
            if vermarktung.get('KAUF') == 'true':
                data['status'] = 'For Sale'
            elif vermarktung.get('MIETE_PACHT') == 'true' or vermarktung.get('MIETE') == 'true':
                data['status'] = 'For Rent'
            else:
                data['status'] = 'For Sale'
        
        # Preise
        preise = immobilie_elem.find('.//preise')
        if preise is not None:
            kaufpreis = self._get_float(preise, 'kaufpreis')
            kaltmiete = self._get_float(preise, 'kaltmiete')
            warmmiete = self._get_float(preise, 'warmmiete')
            
            if kaufpreis > 0:
                data['price'] = int(kaufpreis)
            elif warmmiete > 0:
                data['price'] = int(warmmiete)
            elif kaltmiete > 0:
                data['price'] = int(kaltmiete)
        
        # Flächen
        flaechen = immobilie_elem.find('.//flaechen')
        if flaechen is not None:
            data['size'] = self._get_float(flaechen, 'wohnflaeche') or self._get_float(flaechen, 'gesamtflaeche')
            data['area'] = self._get_float(flaechen, 'grundstuecksflaeche')
            data['bedrooms'] = self._get_int(flaechen, 'anzahl_schlafzimmer')
            data['bathrooms'] = self._get_float(flaechen, 'anzahl_badezimmer')
            data['floors'] = self._get_int(flaechen, 'anzahl_etagen') or 1
            
            zimmer = self._get_float(flaechen, 'anzahl_zimmer')
            if zimmer > 0 and data.get('bedrooms', 0) == 0:
                data['bedrooms'] = int(zimmer)
        
        # Ausstattung
        ausstattung = immobilie_elem.find('.//ausstattung')
        if ausstattung is not None:
            # Garage
            stellplatz = ausstattung.find('.//stellplatzart')
            if stellplatz is not None:
                garage_types = ['TIEFGARAGE', 'GARAGE', 'CARPORT']
                for gtype in garage_types:
                    if stellplatz.get(gtype) == 'true':
                        data['garage'] = 1
                        break
        
        # Freitexte / Beschreibung
        freitexte = immobilie_elem.find('.//freitexte')
        if freitexte is not None:
            data['title'] = self._get_text(freitexte, 'objekttitel')
            data['description'] = self._get_text(freitexte, 'objektbeschreibung')
            
            # Weitere Texte als Teil der Beschreibung
            lage = self._get_text(freitexte, 'lage')
            ausstattung_text = self._get_text(freitexte, 'ausstatt_beschr')
            sonstiges = self._get_text(freitexte, 'sonstige_angaben')
            
            if lage or ausstattung_text or sonstiges:
                extra = []
                if lage:
                    extra.append(f"Lage: {lage}")
                if ausstattung_text:
                    extra.append(f"Ausstattung: {ausstattung_text}")
                if sonstiges:
                    extra.append(f"Sonstiges: {sonstiges}")
                if data.get('description'):
                    data['description'] += "\n\n" + "\n\n".join(extra)
                else:
                    data['description'] = "\n\n".join(extra)
        
        # Verwaltung (externe ID)
        verwaltung = immobilie_elem.find('.//verwaltung_techn')
        if verwaltung is not None:
            data['external_id'] = self._get_text(verwaltung, 'objektnr_extern')
            data['internal_id'] = self._get_text(verwaltung, 'objektnr_intern')
        
        # Bilder
        anhaenge = immobilie_elem.find('.//anhaenge')
        if anhaenge is not None:
            images = []
            for anhang in anhaenge.findall('anhang'):
                if anhang.get('gruppe') == 'BILD' or anhang.get('gruppe') == 'TITELBILD':
                    pfad = self._get_text(anhang, 'daten/pfad')
                    if pfad:
                        images.append(pfad)
            data['images'] = images[:7]  # Max 7 Bilder (1 Haupt + 6 weitere)
        
        return data
    
    @transaction.atomic
    def import_from_file(self, file_path):
        """
        Import all properties from OpenImmo XML file
        Returns tuple (success_count, error_count, errors)
        """
        root = self.parse_file(file_path)
        if root is None:
            return 0, 1, ["Could not parse XML file"]
        
        return self._import_from_root(root)
    
    @transaction.atomic
    def import_from_string(self, xml_string):
        """
        Import all properties from OpenImmo XML string
        Returns tuple (success_count, error_count, errors)
        """
        root = self.parse_string(xml_string)
        if root is None:
            return 0, 1, ["Could not parse XML string"]
        
        return self._import_from_root(root)
    
    def _import_from_root(self, root):
        """Import from parsed XML root"""
        success_count = 0
        error_count = 0
        errors = []
        
        # Find all immobilie elements
        immobilien = root.findall('.//immobilie')
        
        for imm in immobilien:
            try:
                data = self.extract_property(imm)
                listing = self._create_listing(data)
                if listing:
                    success_count += 1
                else:
                    error_count += 1
                    errors.append(f"Could not create listing for: {data.get('title', 'Unknown')}")
            except Exception as e:
                error_count += 1
                errors.append(str(e))
                logger.exception("Error importing property")
        
        return success_count, error_count, errors
    
    def _create_listing(self, data):
        """Create or update a Listing from extracted data"""
        if not data.get('title'):
            data['title'] = f"{data.get('type', 'Immobilie')} in {data.get('city', 'Kroatien')}"
        
        # Check if listing with external_id exists
        external_id = data.pop('external_id', None)
        internal_id = data.pop('internal_id', None)
        images = data.pop('images', [])
        
        # Remove non-model fields
        data.pop('anbieter_name', None)
        data.pop('anbieter_email', None)
        data.pop('anbieter_telefon', None)
        
        # Set defaults
        data.setdefault('type', 'Other')
        data.setdefault('status', 'For Sale')
        data.setdefault('bedrooms', 1)
        data.setdefault('bathrooms', 1)
        data.setdefault('floors', 1)
        data.setdefault('garage', 0)
        data.setdefault('size', 0)
        data.setdefault('area', 0)
        data.setdefault('price', 0)
        data.setdefault('country', 'Kroatien')
        data.setdefault('is_published', True)
        
        # Assign to professional or agent
        if self.professional:
            data['realtor'] = self.professional
        elif self.agent:
            data['realtor'] = self.agent
        
        listing = Listing.objects.create(**data)
        
        # TODO: Handle image downloads if needed
        
        return listing


class SimpleXMLImporter:
    """
    Einfache XML-Schnittstelle für WordPress-Seiten kroatischer Makler
    Flexibles Format das verschiedene Strukturen unterstützt
    """
    
    # Mögliche Tag-Namen für Felder (mehrere Varianten)
    FIELD_MAPPINGS = {
        'title': ['title', 'naziv', 'naslov', 'name', 'objekttitel'],
        'description': ['description', 'opis', 'beschreibung', 'content', 'tekst'],
        'price': ['price', 'cijena', 'preis', 'cena', 'cost'],
        'size': ['size', 'povrsina', 'flaeche', 'area', 'm2', 'sqm', 'wohnflaeche'],
        'bedrooms': ['bedrooms', 'sobe', 'zimmer', 'rooms', 'schlafzimmer', 'spavace_sobe'],
        'bathrooms': ['bathrooms', 'kupatila', 'badezimmer', 'baths', 'kupaonice'],
        'city': ['city', 'grad', 'ort', 'stadt', 'mjesto', 'location'],
        'address': ['address', 'adresa', 'strasse', 'ulica'],
        'type': ['type', 'tip', 'vrsta', 'objektart', 'category'],
        'status': ['status', 'stanje', 'vermarktungsart', 'prodaja_najam'],
        'image': ['image', 'slika', 'bild', 'photo', 'foto', 'img'],
        'images': ['images', 'slike', 'bilder', 'photos', 'fotos', 'gallery'],
    }
    
    TYPE_MAPPING = {
        # Kroatisch
        'stan': 'Apartment',
        'kuca': 'House',
        'kuća': 'House',
        'vila': 'Villa',
        'zemljiste': 'Land',
        'zemljište': 'Land',
        'poslovni': 'Commercial',
        'poslovni prostor': 'Commercial',
        # Deutsch
        'wohnung': 'Apartment',
        'haus': 'House',
        'villa': 'Villa',
        'grundstück': 'Land',
        'gewerbe': 'Commercial',
        # English
        'apartment': 'Apartment',
        'house': 'House',
        'land': 'Land',
        'commercial': 'Commercial',
    }
    
    STATUS_MAPPING = {
        # Kroatisch
        'prodaja': 'For Sale',
        'najam': 'For Rent',
        'iznajmljivanje': 'For Rent',
        # Deutsch
        'kauf': 'For Sale',
        'miete': 'For Rent',
        'verkauf': 'For Sale',
        # English
        'sale': 'For Sale',
        'rent': 'For Rent',
        'for sale': 'For Sale',
        'for rent': 'For Rent',
    }
    
    def __init__(self, professional_id=None, agent_id=None):
        self.professional = None
        self.agent = None
        
        if professional_id:
            try:
                self.professional = Professional.objects.get(id=professional_id)
            except Professional.DoesNotExist:
                pass
        
        if agent_id:
            try:
                self.agent = Agent.objects.get(id=agent_id)
            except Agent.DoesNotExist:
                pass
    
    def _find_field(self, element, field_name):
        """Find a field value trying multiple possible tag names"""
        possible_names = self.FIELD_MAPPINGS.get(field_name, [field_name])
        
        for name in possible_names:
            # Try direct child
            found = element.find(name)
            if found is not None and found.text:
                return found.text.strip()
            
            # Try case-insensitive
            for child in element:
                if child.tag.lower() == name.lower():
                    if child.text:
                        return child.text.strip()
        
        return None
    
    def _find_images(self, element):
        """Find all image URLs in element"""
        images = []
        possible_names = self.FIELD_MAPPINGS.get('images', []) + self.FIELD_MAPPINGS.get('image', [])
        
        for name in possible_names:
            # Single image
            found = element.find(name)
            if found is not None:
                if found.text:
                    images.append(found.text.strip())
                # Check for src attribute
                src = found.get('src') or found.get('url')
                if src:
                    images.append(src)
            
            # Multiple images
            for child in element.findall(f'.//{name}'):
                if child.text:
                    images.append(child.text.strip())
                src = child.get('src') or child.get('url')
                if src:
                    images.append(src)
        
        return list(set(images))[:7]  # Remove duplicates, max 7
    
    def parse_file(self, file_path):
        """Parse XML file"""
        try:
            tree = ET.parse(file_path)
            return tree.getroot()
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            return None
    
    def parse_string(self, xml_string):
        """Parse XML string"""
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            return None
    
    def extract_property(self, prop_elem):
        """Extract property from XML element"""
        data = {}
        
        # Basic fields
        data['title'] = self._find_field(prop_elem, 'title')
        data['description'] = self._find_field(prop_elem, 'description')
        data['city'] = self._find_field(prop_elem, 'city')
        data['address'] = self._find_field(prop_elem, 'address')
        
        # Numeric fields
        price = self._find_field(prop_elem, 'price')
        if price:
            try:
                data['price'] = int(float(price.replace(',', '.').replace('€', '').replace('EUR', '').strip()))
            except ValueError:
                data['price'] = 0
        
        size = self._find_field(prop_elem, 'size')
        if size:
            try:
                data['size'] = float(size.replace(',', '.').replace('m²', '').replace('m2', '').strip())
            except ValueError:
                data['size'] = 0
        
        bedrooms = self._find_field(prop_elem, 'bedrooms')
        if bedrooms:
            try:
                data['bedrooms'] = int(float(bedrooms))
            except ValueError:
                data['bedrooms'] = 1
        
        bathrooms = self._find_field(prop_elem, 'bathrooms')
        if bathrooms:
            try:
                data['bathrooms'] = float(bathrooms)
            except ValueError:
                data['bathrooms'] = 1
        
        # Type mapping
        prop_type = self._find_field(prop_elem, 'type')
        if prop_type:
            data['type'] = self.TYPE_MAPPING.get(prop_type.lower(), 'Other')
        else:
            data['type'] = 'Other'
        
        # Status mapping
        status = self._find_field(prop_elem, 'status')
        if status:
            data['status'] = self.STATUS_MAPPING.get(status.lower(), 'For Sale')
        else:
            data['status'] = 'For Sale'
        
        # Images
        data['images'] = self._find_images(prop_elem)
        
        return data
    
    @transaction.atomic
    def import_from_file(self, file_path):
        """Import from XML file"""
        root = self.parse_file(file_path)
        if root is None:
            return 0, 1, ["Could not parse XML file"]
        
        return self._import_from_root(root)
    
    @transaction.atomic
    def import_from_string(self, xml_string):
        """Import from XML string"""
        root = self.parse_string(xml_string)
        if root is None:
            return 0, 1, ["Could not parse XML string"]
        
        return self._import_from_root(root)
    
    def _import_from_root(self, root):
        """Import all properties from XML root"""
        success_count = 0
        error_count = 0
        errors = []
        
        # Try to find property elements (various possible names)
        property_tags = ['property', 'immobilie', 'nekretnina', 'listing', 'item', 'objekt']
        
        properties = []
        for tag in property_tags:
            properties.extend(root.findall(f'.//{tag}'))
        
        # If no specific property tags, try direct children
        if not properties:
            properties = list(root)
        
        for prop in properties:
            try:
                data = self.extract_property(prop)
                listing = self._create_listing(data)
                if listing:
                    success_count += 1
                else:
                    error_count += 1
            except Exception as e:
                error_count += 1
                errors.append(str(e))
        
        return success_count, error_count, errors
    
    def _create_listing(self, data):
        """Create Listing from data"""
        images = data.pop('images', [])
        
        # Defaults
        data.setdefault('title', 'Nekretnina')
        data.setdefault('type', 'Other')
        data.setdefault('status', 'For Sale')
        data.setdefault('bedrooms', 1)
        data.setdefault('bathrooms', 1)
        data.setdefault('floors', 1)
        data.setdefault('garage', 0)
        data.setdefault('size', 0)
        data.setdefault('area', 0)
        data.setdefault('price', 0)
        data.setdefault('country', 'Kroatien')
        data.setdefault('is_published', True)
        
        if self.professional:
            data['realtor'] = self.professional
        elif self.agent:
            data['realtor'] = self.agent
        
        listing = Listing.objects.create(**data)
        return listing


def import_from_url(url, importer_class, professional_id=None, agent_id=None):
    """
    Import XML from URL
    
    Args:
        url: URL to XML file
        importer_class: OpenImmoImporter or SimpleXMLImporter
        professional_id: Optional Professional ID
        agent_id: Optional Agent ID
    
    Returns:
        tuple (success_count, error_count, errors)
    """
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        importer = importer_class(professional_id=professional_id, agent_id=agent_id)
        return importer.import_from_string(response.text)
    
    except requests.RequestException as e:
        return 0, 1, [f"Could not fetch URL: {e}"]
