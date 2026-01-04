# Django Views für XML-Export
# Fügen Sie diese Views zu Ihrer listings/views.py oder main/views.py hinzu

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from listings.models import Listing
# Importieren Sie die XML-Generatoren (Pfad anpassen!)
# from .xml_export import OpenImmoXMLGenerator, SimpleXMLGenerator


def listings_xml_openimmo(request):
    """
    XML-Export im OpenImmo 1.2.7 Format
    URL: /api/listings/xml/ oder /api/listings/openimmo/
    """
    # Nur veröffentlichte Listings
    listings = Listing.objects.filter(is_published=True).select_related('realtor')
    
    # Base URL für Bilder (Ihre Domain)
    base_url = request.build_absolute_uri('/')[:-1]  # z.B. https://123-kroatien.eu
    
    # XML generieren
    generator = OpenImmoXMLGenerator(listings, base_url=base_url)
    xml_content = generator.generate()
    
    # Response mit korrektem Content-Type
    response = HttpResponse(xml_content, content_type='application/xml; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="openimmo_export.xml"'
    
    return response


def listings_xml_simple(request):
    """
    XML-Export im einfachen Format
    URL: /api/listings/simple-xml/
    """
    # Nur veröffentlichte Listings
    listings = Listing.objects.filter(is_published=True).select_related('realtor')
    
    # Base URL für Bilder
    base_url = request.build_absolute_uri('/')[:-1]
    
    # XML generieren
    generator = SimpleXMLGenerator(listings, base_url=base_url)
    xml_content = generator.generate()
    
    # Response
    response = HttpResponse(xml_content, content_type='application/xml; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="listings_export.xml"'
    
    return response


# Optional: Filter-Optionen
def listings_xml_openimmo_filtered(request):
    """
    XML-Export mit Filter-Optionen
    URL: /api/listings/xml/?agent_id=123&property_type=House
    """
    # Basis Query
    listings = Listing.objects.filter(is_published=True).select_related('realtor')
    
    # Filter nach Agent/Makler
    agent_id = request.GET.get('agent_id')
    if agent_id:
        listings = listings.filter(realtor__id=agent_id)
    
    # Filter nach Immobilientyp
    property_type = request.GET.get('property_type')
    if property_type:
        listings = listings.filter(property_type=property_type)
    
    # Filter nach Status (Sale/Rent)
    property_status = request.GET.get('property_status')
    if property_status:
        listings = listings.filter(property_status=property_status)
    
    # Filter nach Stadt
    city = request.GET.get('city')
    if city:
        listings = listings.filter(city=city)
    
    # Base URL
    base_url = request.build_absolute_uri('/')[:-1]
    
    # XML generieren
    generator = OpenImmoXMLGenerator(listings, base_url=base_url)
    xml_content = generator.generate()
    
    # Response
    response = HttpResponse(xml_content, content_type='application/xml; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="openimmo_export.xml"'
    
    return response
