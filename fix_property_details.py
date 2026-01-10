import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
django.setup()

# Fix the property_details view
old_code = '''def property_details(request, id):
    return render(request, 'main/single-detail.html', {'listing': Listing.objects.get(id=id)})'''

new_code = '''def property_details(request, id):
    import json
    listing = Listing.objects.get(id=id)
    user_language = request.session.get('site_language', 'en')
    
    if user_language == 'ge': listing.json_content = json.loads(listing.german_content) if listing.german_content else listing.get_json()
    elif user_language == 'fr': listing.json_content = json.loads(listing.french_content) if listing.french_content else listing.get_json()
    elif user_language == 'gr': listing.json_content = json.loads(listing.greek_content) if listing.greek_content else listing.get_json()
    elif user_language == 'hr': listing.json_content = json.loads(listing.croatian_content) if listing.croatian_content else listing.get_json()
    elif user_language == 'pl': listing.json_content = json.loads(listing.polish_content) if listing.polish_content else listing.get_json()
    elif user_language == 'cz': listing.json_content = json.loads(listing.czech_content) if listing.czech_content else listing.get_json()
    elif user_language == 'ru': listing.json_content = json.loads(listing.russian_content) if listing.russian_content else listing.get_json()
    elif user_language == 'sw': listing.json_content = json.loads(listing.swedish_content) if listing.swedish_content else listing.get_json()
    elif user_language == 'no': listing.json_content = json.loads(listing.norway_content) if listing.norway_content else listing.get_json()
    elif user_language == 'sk': listing.json_content = json.loads(listing.slovak_content) if listing.slovak_content else listing.get_json()
    elif user_language == 'nl': listing.json_content = json.loads(listing.dutch_content) if listing.dutch_content else listing.get_json()
    else: listing.json_content = json.loads(listing.english_content) if listing.english_content else listing.get_json()
    
    return render(request, 'main/single-detail.html', {'listing': listing})'''

with open('main/views.py', 'r') as f:
    content = f.read()

content = content.replace(old_code, new_code)

with open('main/views.py', 'w') as f:
    f.write(content)

print('✅ property_details View repariert!')
