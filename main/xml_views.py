"""
XML Import Views fuer 123-Kroatien.eu
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
import json

from main.xml_import import OpenImmoImporter, SimpleXMLImporter, import_from_url
from main.professional_models import Professional
from listings.models import Listing


@login_required(login_url='account:login')
def xml_import_dashboard(request, id):
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        messages.error(request, "Profil nicht gefunden.")
        return redirect('main:home')
    
    if professional.user != request.user and not request.user.is_superuser:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    return render(request, 'main/xml_import_dashboard.html', {'professional': professional})


@login_required(login_url='account:login')
@require_http_methods(["POST"])
def xml_import_file(request, id):
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profil nicht gefunden'})
    
    if professional.user != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Keine Berechtigung'})
    
    if 'xml_file' not in request.FILES:
        return JsonResponse({'success': False, 'error': 'Keine Datei'})
    
    xml_file = request.FILES['xml_file']
    import_type = request.POST.get('import_type', 'simple')
    
    try:
        xml_content = xml_file.read().decode('utf-8')
    except UnicodeDecodeError:
        try:
            xml_file.seek(0)
            xml_content = xml_file.read().decode('iso-8859-1')
        except:
            return JsonResponse({'success': False, 'error': 'Datei nicht lesbar'})
    
    if import_type == 'openimmo':
        importer = OpenImmoImporter(professional_id=str(professional.id))
    else:
        importer = SimpleXMLImporter(professional_id=str(professional.id))
    
    success, errors_count, error_messages = importer.import_from_string(xml_content)
    
    return JsonResponse({
        'success': True,
        'imported': success,
        'errors': errors_count,
        'error_messages': error_messages[:10]
    })


@login_required(login_url='account:login')
@require_http_methods(["POST"])
def xml_import_url(request, id):
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Profil nicht gefunden'})
    
    if professional.user != request.user and not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'Keine Berechtigung'})
    
    data = json.loads(request.body) if request.content_type == 'application/json' else request.POST
    url = data.get('url', '')
    import_type = data.get('import_type', 'simple')
    
    if not url:
        return JsonResponse({'success': False, 'error': 'Keine URL'})
    
    importer_class = OpenImmoImporter if import_type == 'openimmo' else SimpleXMLImporter
    
    success, errors_count, error_messages = import_from_url(
        url, importer_class, professional_id=str(professional.id)
    )
    
    return JsonResponse({
        'success': True,
        'imported': success,
        'errors': errors_count,
        'error_messages': error_messages[:10]
    })


def rss_listings(request):
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')[:50]
    
    items = []
    for l in listings:
        items.append(f"""<item>
            <title><![CDATA[{l.title}]]></title>
            <link>https://123-kroatien.eu/property-details/{l.id}/</link>
            <description><![CDATA[{(l.description or '')[:500]}]]></description>
            <price>{l.price} EUR</price>
            <city>{l.city or ''}</city>
        </item>""")
    
    rss = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
    <channel>
        <title>123-Kroatien.eu - Immobilien</title>
        <link>https://123-kroatien.eu</link>
        <description>Immobilien in Kroatien</description>
        {''.join(items)}
    </channel>
</rss>"""
    
    return HttpResponse(rss, content_type='application/rss+xml')


def xml_sitemap(request):
    listings = Listing.objects.filter(is_published=True)
    professionals = Professional.objects.filter(is_active=True)
    
    urls = []
    for page in ['', 'about/', 'contact/', 'listing/', 'faq/']:
        urls.append(f"<url><loc>https://123-kroatien.eu/{page}</loc></url>")
    
    for l in listings:
        urls.append(f"<url><loc>https://123-kroatien.eu/property-details/{l.id}/</loc></url>")
    
    for p in professionals:
        urls.append(f"<url><loc>https://123-kroatien.eu/agent/{p.id}/</loc></url>")
    
    sitemap = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    {''.join(urls)}
</urlset>"""
    
    return HttpResponse(sitemap, content_type='application/xml')


def robots_txt(request):
    content = """User-agent: *
Allow: /
Sitemap: https://123-kroatien.eu/sitemap.xml
Disallow: /admin/
Disallow: /nik-verwaltung-2026/

# AI Crawlers - GEO
Llms-txt: https://123-kroatien.eu/llms.txt
"""
    return HttpResponse(content, content_type='text/plain')


def llms_txt(request):
    """Serve llms.txt for AI crawlers (GEO - Generative Engine Optimization)"""
    import os
    from django.conf import settings
    
    llms_path = os.path.join(settings.BASE_DIR, 'llms.txt')
    try:
        with open(llms_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        content = "# 123-kroatien.eu\n\n> Immobilienportal für Kroatien"
    
    return HttpResponse(content, content_type='text/plain; charset=utf-8')
