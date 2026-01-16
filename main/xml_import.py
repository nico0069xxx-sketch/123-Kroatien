"""
XML Import Schnittstellen für 123-Kroatien.eu
"""

import xml.etree.ElementTree as ET
from django.db import transaction
from listings.models import Listing
from accounts.models import Agent
from main.professional_models import Professional
import requests
import logging

logger = logging.getLogger(__name__)


class OpenImmoImporter:
    """OpenImmo XML Import"""
    
    OBJEKTART_MAPPING = {
        'zimmer': 'Apartment', 'wohnung': 'Apartment', 'haus': 'House',
        'grundstueck': 'Land', 'buero_praxen': 'Commercial',
        'einzelhandel': 'Commercial', 'gastgewerbe': 'Commercial',
        'freizeitimmobilie_gewerblich': 'Villa', 'sonstige': 'Other',
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
    
    def parse_string(self, xml_string):
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError as e:
            logger.error(f"XML Parse Error: {e}")
            return None
    
    def _get_text(self, element, path, default=''):
        if element is None:
            return default
        found = element.find(path)
        if found is not None and found.text:
            return found.text.strip()
        return default
    
    def _get_float(self, element, path, default=0.0):
        text = self._get_text(element, path)
        try:
            return float(text.replace(',', '.')) if text else default
        except ValueError:
            return default
    
    def _get_int(self, element, path, default=0):
        text = self._get_text(element, path)
        try:
            return int(float(text.replace(',', '.'))) if text else default
        except ValueError:
            return default
    
    def extract_property(self, immobilie_elem):
        data = {}
        
        geo = immobilie_elem.find('.//geo')
        if geo is not None:
            data['zipcode'] = self._get_text(geo, 'plz')
            data['city'] = self._get_text(geo, 'ort')
            data['state'] = self._get_text(geo, 'bundesland')
            data['address'] = self._get_text(geo, 'strasse')
            data['country'] = self._get_text(geo, 'land/iso_land') or 'Kroatien'
        
        objektart_elem = immobilie_elem.find('.//objektart')
        if objektart_elem is not None:
            for child in objektart_elem:
                data['type'] = self.OBJEKTART_MAPPING.get(child.tag.lower(), 'Other')
                break
        
        vermarktung = immobilie_elem.find('.//vermarktungsart')
        if vermarktung is not None:
            if vermarktung.get('KAUF') == 'true':
                data['status'] = 'For Sale'
            else:
                data['status'] = 'For Rent'
        
        preise = immobilie_elem.find('.//preise')
        if preise is not None:
            kaufpreis = self._get_float(preise, 'kaufpreis')
            if kaufpreis > 0:
                data['price'] = int(kaufpreis)
        
        flaechen = immobilie_elem.find('.//flaechen')
        if flaechen is not None:
            data['size'] = self._get_float(flaechen, 'wohnflaeche')
            data['area'] = self._get_float(flaechen, 'grundstuecksflaeche')
            data['bedrooms'] = self._get_int(flaechen, 'anzahl_schlafzimmer') or self._get_int(flaechen, 'anzahl_zimmer')
            data['bathrooms'] = self._get_float(flaechen, 'anzahl_badezimmer')
        
        freitexte = immobilie_elem.find('.//freitexte')
        if freitexte is not None:
            data['title'] = self._get_text(freitexte, 'objekttitel')
            data['description'] = self._get_text(freitexte, 'objektbeschreibung')
        
        return data
    
    @transaction.atomic
    def import_from_string(self, xml_string):
        root = self.parse_string(xml_string)
        if root is None:
            return 0, 1, ["Could not parse XML"]
        
        success_count = 0
        error_count = 0
        errors = []
        
        for imm in root.findall('.//immobilie'):
            try:
                data = self.extract_property(imm)
                listing = self._create_listing(data)
                if listing:
                    success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(str(e))
        
        return success_count, error_count, errors
    
    def _create_listing(self, data):
        data.setdefault('title', 'Immobilie')
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
        
        return Listing.objects.create(**data)


class SimpleXMLImporter:
    """Einfaches XML fuer WordPress-Seiten kroatischer Makler"""
    
    FIELD_MAPPINGS = {
        'title': ['title', 'naziv', 'naslov', 'name', 'objekttitel'],
        'description': ['description', 'opis', 'beschreibung', 'content'],
        'price': ['price', 'cijena', 'preis', 'cena'],
        'size': ['size', 'povrsina', 'flaeche', 'area', 'm2'],
        'bedrooms': ['bedrooms', 'sobe', 'zimmer', 'rooms'],
        'bathrooms': ['bathrooms', 'kupatila', 'badezimmer'],
        'city': ['city', 'grad', 'ort', 'mjesto', 'location'],
        'type': ['type', 'tip', 'vrsta', 'objektart'],
        'status': ['status', 'stanje', 'prodaja_najam'],
    }
    
    TYPE_MAPPING = {
        'stan': 'Apartment', 'kuca': 'House', 'vila': 'Villa',
        'zemljiste': 'Land', 'wohnung': 'Apartment', 'haus': 'House',
        'apartment': 'Apartment', 'house': 'House', 'land': 'Land',
    }
    
    STATUS_MAPPING = {
        'prodaja': 'For Sale', 'najam': 'For Rent',
        'kauf': 'For Sale', 'miete': 'For Rent',
        'sale': 'For Sale', 'rent': 'For Rent',
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
    
    def parse_string(self, xml_string):
        try:
            return ET.fromstring(xml_string)
        except ET.ParseError:
            return None
    
    def _find_field(self, element, field_name):
        possible_names = self.FIELD_MAPPINGS.get(field_name, [field_name])
        for name in possible_names:
            found = element.find(name)
            if found is not None and found.text:
                return found.text.strip()
            for child in element:
                if child.tag.lower() == name.lower() and child.text:
                    return child.text.strip()
        return None
    
    def extract_property(self, prop_elem):
        data = {}
        data['title'] = self._find_field(prop_elem, 'title')
        data['description'] = self._find_field(prop_elem, 'description')
        data['city'] = self._find_field(prop_elem, 'city')
        
        price = self._find_field(prop_elem, 'price')
        if price:
            try:
                data['price'] = int(float(price.replace(',', '.').replace('EUR', '').strip()))
            except:
                data['price'] = 0
        
        size = self._find_field(prop_elem, 'size')
        if size:
            try:
                data['size'] = float(size.replace(',', '.').replace('m2', '').strip())
            except:
                data['size'] = 0
        
        bedrooms = self._find_field(prop_elem, 'bedrooms')
        if bedrooms:
            try:
                data['bedrooms'] = int(float(bedrooms))
            except:
                data['bedrooms'] = 1
        
        prop_type = self._find_field(prop_elem, 'type')
        data['type'] = self.TYPE_MAPPING.get(prop_type.lower() if prop_type else '', 'Other')
        
        status = self._find_field(prop_elem, 'status')
        data['status'] = self.STATUS_MAPPING.get(status.lower() if status else '', 'For Sale')
        
        return data
    
    @transaction.atomic
    def import_from_string(self, xml_string):
        root = self.parse_string(xml_string)
        if root is None:
            return 0, 1, ["Could not parse XML"]
        
        success_count = 0
        error_count = 0
        errors = []
        
        property_tags = ['property', 'immobilie', 'nekretnina', 'listing', 'item']
        properties = []
        for tag in property_tags:
            properties.extend(root.findall(f'.//{tag}'))
        if not properties:
            properties = list(root)
        
        for prop in properties:
            try:
                data = self.extract_property(prop)
                listing = self._create_listing(data)
                if listing:
                    success_count += 1
            except Exception as e:
                error_count += 1
                errors.append(str(e))
        
        return success_count, error_count, errors
    
    def _create_listing(self, data):
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
        
        return Listing.objects.create(**data)


def import_from_url(url, importer_class, professional_id=None, agent_id=None):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        importer = importer_class(professional_id=professional_id, agent_id=agent_id)
        return importer.import_from_string(response.text)
    except requests.RequestException as e:
        return 0, 1, [f"Could not fetch URL: {e}"]
