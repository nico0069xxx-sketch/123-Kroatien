#!/usr/bin/env python3
"""
Erweitert chatbot_api View mit Smart-Search
"""

old_view = '''def chatbot_api(request):
    from .chatbot import get_chatbot_response
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        language = request.session.get('site_language', 'ge')
        response = get_chatbot_response(message, language)
        return JsonResponse({'response': response})
    return JsonResponse({'error': 'Invalid request'}, status=400)'''

new_view = '''def chatbot_api(request):
    from .chatbot import get_chatbot_response, is_property_search, extract_search_criteria
    if request.method == 'POST':
        data = json.loads(request.body)
        message = data.get('message', '')
        language = request.session.get('site_language', 'ge')
        
        # Prüfen ob es eine Immobiliensuche ist
        if is_property_search(message):
            criteria = extract_search_criteria(message, language)
            
            # Immobilien filtern
            listings = Listing.objects.filter(is_published=True)
            
            if criteria.get('property_type'):
                listings = listings.filter(property_type=criteria['property_type'])
            if criteria.get('property_status'):
                listings = listings.filter(property_status=criteria['property_status'])
            if criteria.get('price_max'):
                listings = listings.filter(property_price__lte=criteria['price_max'])
            if criteria.get('price_min'):
                listings = listings.filter(property_price__gte=criteria['price_min'])
            if criteria.get('bedrooms_min'):
                listings = listings.filter(bedrooms__gte=criteria['bedrooms_min'])
            if criteria.get('location'):
                listings = listings.filter(location__icontains=criteria['location'])
            
            # Ergebnisse formatieren
            results = []
            for listing in listings[:6]:
                # Sprachspezifischer Content
                if language == 'ge' and listing.german_content:
                    content = json.loads(listing.german_content)
                elif language == 'en' and listing.english_content:
                    content = json.loads(listing.english_content)
                elif language == 'hr' and listing.croatian_content:
                    content = json.loads(listing.croatian_content)
                else:
                    content = listing.get_json()
                
                results.append({
                    'id': listing.id,
                    'title': content.get('property_title', listing.property_title),
                    'price': listing.property_price,
                    'location': listing.location,
                    'bedrooms': listing.bedrooms,
                    'image': listing.photo_main.url if listing.photo_main else None,
                })
            
            # Antwort mit Suchergebnissen
            search_responses = {
                'ge': f"Ich habe {len(results)} passende Immobilien gefunden!",
                'en': f"I found {len(results)} matching properties!",
                'hr': f"Pronašao sam {len(results)} odgovarajućih nekretnina!",
            }
            response_text = search_responses.get(language, search_responses['ge'])
            
            if len(results) == 0:
                no_results = {
                    'ge': "Leider keine passenden Immobilien gefunden. Versuche andere Kriterien.",
                    'en': "No matching properties found. Try different criteria.",
                    'hr': "Nažalost, nisu pronađene odgovarajuće nekretnine.",
                }
                response_text = no_results.get(language, no_results['ge'])
            
            return JsonResponse({
                'response': response_text,
                'is_search': True,
                'results': results
            })
        
        # Normale Chatbot-Antwort
        response = get_chatbot_response(message, language)
        return JsonResponse({'response': response, 'is_search': False})
    return JsonResponse({'error': 'Invalid request'}, status=400)'''

with open("main/views.py", "r", encoding="utf-8") as f:
    content = f.read()

if old_view in content:
    content = content.replace(old_view, new_view)
    with open("main/views.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ chatbot_api View erweitert!")
else:
    print("⚠️  View nicht gefunden oder bereits geändert")
