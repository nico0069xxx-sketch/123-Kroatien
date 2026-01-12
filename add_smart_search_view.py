#!/usr/bin/env python3
"""
Fügt Smart-Search View zu views.py hinzu
"""

view_code = '''

# =============================================================================
# AI SMART-SEARCH VIEW
# =============================================================================
from main.chatbot import extract_search_criteria, is_property_search, smart_search_response

@login_required(login_url='main:login_required')
def smart_search(request):
    """
    AI Smart-Search: Natürliche Sprache -> Immobiliensuche
    """
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            query = data.get('query', '')
            language = request.session.get('site_language', 'ge')
            
            if not query:
                return JsonResponse({'status': 'error', 'message': 'Keine Suchanfrage'})
            
            # AI extrahiert Suchkriterien
            criteria = extract_search_criteria(query, language)
            
            # Immobilien filtern
            listings = Listing.objects.filter(is_published=True)
            
            if criteria.get('property_type'):
                listings = listings.filter(property_type=criteria['property_type'])
            
            if criteria.get('property_status'):
                listings = listings.filter(property_status=criteria['property_status'])
            
            if criteria.get('price_min'):
                listings = listings.filter(property_price__gte=criteria['price_min'])
            
            if criteria.get('price_max'):
                listings = listings.filter(property_price__lte=criteria['price_max'])
            
            if criteria.get('bedrooms_min'):
                listings = listings.filter(bedrooms__gte=criteria['bedrooms_min'])
            
            if criteria.get('bathrooms_min'):
                listings = listings.filter(bathrooms__gte=criteria['bathrooms_min'])
            
            if criteria.get('area_min'):
                listings = listings.filter(area__gte=criteria['area_min'])
            
            if criteria.get('location'):
                listings = listings.filter(location__icontains=criteria['location'])
            
            # Features in Beschreibung suchen
            features = criteria.get('features', [])
            for feature in features:
                listings = listings.filter(property_description__icontains=feature)
            
            # Ergebnisse formatieren
            results = []
            user_language = request.session.get('site_language', 'ge')
            
            for listing in listings[:12]:  # Max 12 Ergebnisse
                # Sprachspezifischen Content laden
                if user_language == 'ge' and listing.german_content:
                    content = json.loads(listing.german_content)
                elif user_language == 'en' and listing.english_content:
                    content = json.loads(listing.english_content)
                elif user_language == 'hr' and listing.croatian_content:
                    content = json.loads(listing.croatian_content)
                else:
                    content = listing.get_json()
                
                results.append({
                    'id': listing.id,
                    'title': content.get('property_title', listing.property_title),
                    'price': listing.property_price,
                    'location': listing.location,
                    'bedrooms': listing.bedrooms,
                    'bathrooms': listing.bathrooms,
                    'area': listing.area,
                    'image': listing.photo_main.url if listing.photo_main else None,
                    'type': listing.property_type,
                    'status': listing.property_status,
                })
            
            response_text = smart_search_response(query, len(results), language)
            
            return JsonResponse({
                'status': 'success',
                'message': response_text,
                'criteria': criteria,
                'results': results,
                'count': len(results)
            })
            
        except Exception as e:
            print(f"Smart-Search Error: {e}")
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
'''

# views.py lesen
with open("main/views.py", "r", encoding="utf-8") as f:
    content = f.read()

# Prüfen ob Smart-Search View schon existiert
if "def smart_search" not in content:
    content += view_code
    with open("main/views.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Smart-Search View zu views.py hinzugefügt!")
else:
    print("⚠️  Smart-Search View existiert bereits")
