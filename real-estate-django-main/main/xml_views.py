"""
XML Import Views für 123-Kroatien.eu
Admin-Bereich für den Import von Immobilien via XML
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json

from main.xml_import import OpenImmoImporter, SimpleXMLImporter, import_from_url
from main.professional_models import Professional


@login_required(login_url='account:login')
def xml_import_dashboard(request, id):
    """
    Dashboard für XML-Import
    """
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        messages.error(request, "Profil nicht gefunden.")
        return redirect('main:home')
    
    # Security check
    if professional.user != request.user and not request.user.is_superuser:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    context = {
        'professional': professional,
    }
    return render(request, 'main/xml_import_dashboard.html', context)


@login_required(login_url='account:login')
@require_http_methods(["POST"])
def xml_import_file(request, id):
    """
    Import XML from uploaded file
    """
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profil nicht gefunden'})
    
    # Security check
    if professional.user != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Keine Berechtigung'})
    
    if 'xml_file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'Keine Datei hochgeladen'})
    
    xml_file = request.FILES['xml_file']
    import_type = request.POST.get('import_type', 'simple')
    
    try:
        xml_content = xml_file.read().decode('utf-8')
    except UnicodeDecodeError:
        try:
            xml_file.seek(0)
            xml_content = xml_file.read().decode('iso-8859-1')
        except:
            return JsonResponse({'success': False, 'error': 'Datei konnte nicht gelesen werden'})
    
    # Choose importer
    if import_type == 'openimmo':
        importer = OpenImmoImporter(professional_id=str(professional.id))
    else:
        importer = SimpleXMLImporter(professional_id=str(professional.id))
    
    success, errors_count, error_messages = importer.import_from_string(xml_content)
    
    return JsonResponse({
        'success': True,
        'imported': success,
        'errors': errors_count,
        'error_messages': error_messages[:10]  # Max 10 Fehlermeldungen
    })


@login_required(login_url='account:login')
@require_http_methods(["POST"])
def xml_import_url(request, id):
    """
    Import XML from URL
    """
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profil nicht gefunden'})
    
    # Security check
    if professional.user != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Keine Berechtigung'})
    
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    url = data.get('url', '')
    import_type = data.get('import_type', 'simple')
    
    if not url:
        return JsonResponse({'success': False, 'error': 'Keine URL angegeben'})
    
    # Choose importer class
    if import_type == 'openimmo':
        importer_class = OpenImmoImporter
    else:
        importer_class = SimpleXMLImporter
    
    success, errors_count, error_messages = import_from_url(
        url, 
        importer_class, 
        professional_id=str(professional.id)
    )
    
    return JsonResponse({
        'success': True,
        'imported': success,
        'errors': errors_count,
        'error_messages': error_messages[:10]
    })


# ============================================
# RSS Feed für Immobilien-Export
# ============================================

from django.http import HttpResponse
from listings.models import Listing


def rss_listings(request):
    """
    RSS Feed aller Immobilien
    """
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')[:50]
    
    rss_items = []
    for listing in listings:
        item = f"""
        <item>
            <title><![CDATA[{listing.title}]]></title>
            <link>https://123-kroatien.eu/property-details/{listing.id}/</link>
            <description><![CDATA[{listing.description[:500] if listing.description else ''}...]]></description>
            <pubDate>{listing.list_date.strftime('%a, %d %b %Y %H:%M:%S +0000')}</pubDate>
            <guid>https://123-kroatien.eu/property-details/{listing.id}/</guid>
            <price>{listing.price} EUR</price>
            <city>{listing.city or ''}</city>
            <type>{listing.type or ''}</type>
            <bedrooms>{listing.bedrooms}</bedrooms>
            <bathrooms>{listing.bathrooms}</bathrooms>
            <size>{listing.size} m²</size>
        </item>
        """
        rss_items.append(item)
    
    rss_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
    <channel>
        <title>123-Kroatien.eu - Immobilien</title>
        <link>https://123-kroatien.eu</link>
        <description>Aktuelle Immobilien in Kroatien</description>
        <language>de</language>
        <lastBuildDate>{listings.first().list_date.strftime('%a, %d %b %Y %H:%M:%S +0000') if listings else ''}</lastBuildDate>
        <atom:link href="https://123-kroatien.eu/rss/listings/" rel="self" type="application/rss+xml"/>
        {''.join(rss_items)}
    </channel>
</rss>"""
    
    return HttpResponse(rss_content, content_type='application/rss+xml')


def xml_sitemap(request):
    """
    XML Sitemap für Suchmaschinen
    """
    listings = Listing.objects.filter(is_published=True)
    professionals = Professional.objects.filter(is_active=True)
    
    urls = []
    
    # Static pages
    static_pages = ['', 'about/', 'contact/', 'listing/', 'faq/', 'blog/']
    for page in static_pages:
        urls.append(f"""
        <url>
            <loc>https://123-kroatien.eu/{page}</loc>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>""")
    
    # Listings
    for listing in listings:
        urls.append(f"""
        <url>
            <loc>https://123-kroatien.eu/property-details/{listing.id}/</loc>
            <lastmod>{listing.list_date.strftime('%Y-%m-%d')}</lastmod>
            <changefreq>weekly</changefreq>
            <priority>0.9</priority>
        </url>""")
    
    # Professionals
    for prof in professionals:
        urls.append(f"""
        <url>
            <loc>https://123-kroatien.eu/agent/{prof.id}/</loc>
            <changefreq>monthly</changefreq>
            <priority>0.7</priority>
        </url>""")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {''.join(urls)}
</urlset>"""
    
    return HttpResponse(sitemap, content_type='application/xml')


def robots_txt(request):
    """
    robots.txt für Suchmaschinen
    """
    content = """User-agent: *
Allow: /

Sitemap: https://123-kroatien.eu/sitemap.xml

Disallow: /admin/
Disallow: /nik-verwaltung-2026/
Disallow: /accounts/
Disallow: /portal/
"""
    return HttpResponse(content, content_type='text/plain')
