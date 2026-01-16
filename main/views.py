from django.views.decorators.csrf import csrf_exempt
from main.professional_models import Professional

from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from django.contrib import messages
from django.utils import translation
from django.http import HttpResponse
import feedparser
from django.http import HttpResponseRedirect
from accounts.models import Agent
from pages.models import Translation
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
import json
import os

# Create your views here.

# FAQ-Überschriften Übersetzungen
FAQ_HEADINGS = {
    'ge': {'short': 'Kurzantwort:', 'details': 'Details', 'facts': 'Wichtige Fakten', 'advice': 'Praktischer Rat'},
    'en': {'short': 'Short Answer:', 'details': 'Details', 'facts': 'Key Facts', 'advice': 'Practical Advice'},
    'hr': {'short': 'Kratak odgovor:', 'details': 'Detalji', 'facts': 'Važne činjenice', 'advice': 'Praktični savjet'},
    'fr': {'short': 'Réponse courte:', 'details': 'Détails', 'facts': 'Faits importants', 'advice': 'Conseil pratique'},
    'nl': {'short': 'Kort antwoord:', 'details': 'Details', 'facts': 'Belangrijke feiten', 'advice': 'Praktisch advies'},
    'pl': {'short': 'Krótka odpowiedź:', 'details': 'Szczegóły', 'facts': 'Ważne fakty', 'advice': 'Praktyczna rada'},
    'cz': {'short': 'Stručná odpověď:', 'details': 'Podrobnosti', 'facts': 'Důležitá fakta', 'advice': 'Praktická rada'},
    'sk': {'short': 'Stručná odpoveď:', 'details': 'Podrobnosti', 'facts': 'Dôležité fakty', 'advice': 'Praktická rada'},
    'ru': {'short': 'Краткий ответ:', 'details': 'Подробности', 'facts': 'Важные факты', 'advice': 'Практический совет'},
    'gr': {'short': 'Σύντομη απάντηση:', 'details': 'Λεπτομέρειες', 'facts': 'Σημαντικά στοιχεία', 'advice': 'Πρακτική συμβουλή'},
    'sw': {'short': 'Kort svar:', 'details': 'Detaljer', 'facts': 'Viktiga fakta', 'advice': 'Praktiskt råd'},
    'no': {'short': 'Kort svar:', 'details': 'Detaljer', 'facts': 'Viktige fakta', 'advice': 'Praktisk råd'},
}

def translate_faq_headings(html, lang):
    if lang == 'ge' or lang not in FAQ_HEADINGS:
        return html
    h = FAQ_HEADINGS[lang]
    de = FAQ_HEADINGS['ge']
    html = html.replace(de['short'], h['short'])
    html = html.replace('>'+de['details']+'<', '>'+h['details']+'<')
    html = html.replace('>'+de['facts']+'<', '>'+h['facts']+'<')
    html = html.replace('>'+de['advice']+'<', '>'+h['advice']+'<')
    return html


@login_required(login_url='account:login')
def home(request):
    site_language = request.session.get('site_language')
    if not site_language:
        request.session['site_language'] = 'ge'
    latest_8_listings = Listing.objects.filter(is_published=True).order_by('-list_date')[:8]
    user_language = request.session.get('site_language', 'en')
    for listing in latest_8_listings:
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

    lang = request.session.get('site_language', 'ge')
    context = {
        'latest_8_listings': latest_8_listings,
    }
    return render(request, 'main/home.html', context)

@login_required(login_url='main:login_required')
def about(request):
    return render(request, 'main/about-us.html')

@login_required(login_url='main:login_required')
def contact(request):
    return render(request, 'main/contact.html')

@login_required(login_url='main:login_required')
def add_property(request):
    if request.method == 'POST':
        agent = Agent.objects.get(user=request.user)
        listing = Listing()
        listing.company_name = agent.company_name
        listing.company_logo = agent.company_logo
        listing.portrait_photo = agent.portrait_photo
        listing.oib_number = agent.oib_number
        listing.email = agent.user.email
        listing.domain = agent.domain
        listing.realtor = Agent.objects.get(user=request.user)
        listing.property_title = request.POST['property-title']
        listing.property_description = request.POST['property-description']
        listing.property_type = request.POST['property-type']
        listing.property_status = request.POST['property-status']
        listing.location = request.POST['location']
        listing.bedrooms = request.POST['bedrooms']
        listing.bathrooms = request.POST['bathrooms']
        listing.floors = request.POST['floors']
        listing.garage = request.POST['garages']
        listing.area = request.POST['area']
        listing.size = request.POST['size']
        listing.property_price = request.POST['property_price']
        listing.property_id = request.POST['Property-ID']
        listing.video_url = request.POST['Video-URL']
        listing.photo_main = request.FILES.get('photo-main')
        listing.photo_1 = request.FILES.get('photo-1')
        listing.photo_2 = request.FILES.get('photo-2')
        listing.photo_3 = request.FILES.get('photo-3')
        listing.photo_4 = request.FILES.get('photo-4')
        listing.photo_5 = request.FILES.get('photo-5')
        listing.photo_6 = request.FILES.get('photo-6')
        listing.address = request.POST['address']
        listing.country = request.POST['country']
        listing.city = request.POST['city']
        listing.state = request.POST['state']
        listing.zipcode = request.POST['zip-code']
        listing.neighborhood = request.POST['neighborhood']
        listing.save()
        messages.success(request, "Property added sucsessfully")
        return redirect('main:add_property')

    return render(request, 'main/add-property.html')


@login_required(login_url='main:login_required')
def agency_details(request):
    agent = Agent.objects.get(user=request.user)
    listings = Listing.objects.filter(realtor=agent)
    user_language = request.session.get('site_language', 'en')
    for listing in listings:
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
    
    lang = request.session.get('site_language', 'ge')
    context = {
        'listings': listings,
        'agent': agent,
    }
    return render(request, 'main/agency-detail.html', context)

@login_required(login_url='main:login_required')
def blog(request):
    return render(request, 'main/blog.html')

@login_required(login_url='main:login_required')
def blog_single(request):
    return render(request, 'main/blog-single.html')

@login_required(login_url='main:login_required')
def blog_single_1(request):
    return render(request, 'main/blog-single-1.html')

@login_required(login_url='main:login_required')
def blog_single_2(request):
    return render(request, 'main/blog-single-2.html')

@login_required(login_url='main:login_required')
def blog_single_3(request):
    return render(request, 'main/blog-single-3.html')

@login_required(login_url='main:login_required')
def imprint(request):
    return render(request, 'main/imprint.html')

@login_required(login_url='main:login_required')
def data_protection(request):
    return render(request, 'main/data-protection.html')

@login_required(login_url='main:login_required')
def agb(request):
    return render(request, 'main/agb.html')

@login_required(login_url='main:login_required')
def cancellation_policy(request):
    return render(request, 'main/cancellation-policy.html')

@login_required(login_url='main:login_required')
def sitemap(request):
    return render(request, 'main/sitemap.html')

@login_required(login_url='main:login_required')
def service(request):
    return render(request, 'main/service.html')

@login_required(login_url='main:login_required')
def listings(request): 
    listings = Listing.objects.filter(is_published=True)

    property_status = request.GET.get('property_status', None)
    if property_status:
        listings = listings.filter(property_status=property_status)

    property_type = request.GET.get('property_type', None)
    if property_type:
        listings = listings.filter(property_type=property_type)

    area_from = request.GET.get('area_from', None)
    if area_from:
        listings = listings.filter(area__gte=area_from)

    location = request.GET.get('location', None)
    if location:
        listings = listings.filter(location=location)

    bedrooms = request.GET.get('bedrooms', None)
    if bedrooms:
        listings = listings.filter(bedrooms=bedrooms)

    bathrooms = request.GET.get('bathrooms', None)
    if bathrooms:
        listings = listings.filter(bathrooms=bathrooms)

    my_range = request.GET.get('my_range', None)
    if my_range:
        min_price, max_price = my_range.split(';')
        if min_price and max_price:
            listings = listings.filter(property_price__gte=int(min_price), property_price__lte=int(max_price))


    air_conditioning = request.GET.get('air_conditioning', None) 
    if air_conditioning: 
        listings = listings.filter(property_description__icontains='air conditioning')
    
    swimming_pool = request.GET.get('swimming_pool', None)
    if swimming_pool:
        listings = listings.filter(property_description__icontains='swimming pool')

    central_heating = request.GET.get('central_heating', None)
    if central_heating:
        listings = listings.filter(property_description__icontains='central heating')

    spa_message = request.GET.get('spa_message', None)
    if spa_message:
        listings = listings.filter(property_description__icontains='spa')

    pets_allow = request.GET.get('pets_allow', None)
    if pets_allow:
        listings = listings.filter(property_description__icontains='pets allow')

    gym = request.GET.get('gym', None)
    if gym:
        listings = listings.filter(property_description__icontains='gym')

    alarm = request.GET.get('alarm', None)
    if alarm:
        listings = listings.filter(property_description__icontains='alarm')

    window_covering = request.GET.get('window_covering', None)
    if window_covering:
        listings = listings.filter(property_description__icontains='window covering')

    free_wifi = request.GET.get('free_wifi', None)
    if free_wifi:
        listings = listings.filter(property_description__icontains='free wifi')

    car_parking = request.GET.get('car_parking', None)
    if car_parking:
        listings = listings.filter(property_description__icontains='car parking')


    sort_by = request.GET.get('sort_by', None)
    if sort_by:
        if sort_by == 'price_low_to_high':
            listings = listings.order_by('property_price')
        elif sort_by == 'price_high_to_low':
            listings = listings.order_by('-property_price')
        elif sort_by == 'sell_properties':
            # order the properties whose status is 'For Sale' first
            listings = listings.order_by('-property_status')
        elif sort_by == 'rent_properties':
            # order the properties whose status is 'For Rent' first
            listings = listings.order_by('property_status')
        

    house = Listing.objects.filter(property_type='House', is_published=True).count()
    apartment = Listing.objects.filter(property_type='Apartment', is_published=True).count()
    office = Listing.objects.filter(property_type='Office', is_published=True).count()
    villa = Listing.objects.filter(property_type='Villa', is_published=True).count()
    family_house = Listing.objects.filter(property_type='Family House', is_published=True).count()
    modern_house = Listing.objects.filter(property_type='Modern Villa', is_published=True).count()
    town_house = Listing.objects.filter(property_type='Town House', is_published=True).count()

    page = request.GET.get('page', 1)
    max_listings_per_page = 12
    #listings = listings[(int(page) - 1) * max_listings_per_page : int(page) * max_listings_per_page]

    user_language = request.session.get('site_language', 'en')
    listings_two_dimensional = []
    num = 1
    for listing in listings:
        if num % 2 != 0:
            listings_two_dimensional.append([listing])
        else:
            listings_two_dimensional[len(listings_two_dimensional) - 1].append(listing)
        num += 1
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
    lang = request.session.get('site_language', 'ge')
    context = {
        'listings': listings,
        'listings_two_dimensional': listings_two_dimensional,
        'apartment': apartment if apartment else 0,
        'house': house if house else 0,
        'office': office if office else 0,
        'villa': villa if villa else 0,
        'family_house': family_house if family_house else 0,
        'modern_villa': modern_house if modern_house else 0,
        'town_house': town_house if town_house else 0,
    }
    return render(request, 'main/listings.html', context)



@login_required(login_url='main:login_required')
def single_details(request, id):
    from main.ai_listing_helper import get_listing_content_with_ai
    user_language = request.session.get('site_language', 'en')
    listing = Listing.objects.get(id=id)
    listing.json_content = get_listing_content_with_ai(listing, user_language)
    lang = request.session.get('site_language', 'ge')
    context = {
        'listing': listing,
    }
    return render(request, 'main/single-detail.html', context)


@login_required(login_url='main:login_required')
def edit_property(request, id):
    listing = Listing.objects.get(id=id)
    if request.method == 'POST':
        listing.property_title = request.POST['property-title']
        listing.property_description = request.POST['property-description']
        listing.property_type = request.POST['property-type'] if request.POST['property-type'] else listing.property_type
        listing.property_status = request.POST['property-status'] if request.POST['property-status'] else listing.property_status
        listing.location = request.POST['location']
        listing.bedrooms = request.POST['bedrooms']
        listing.bathrooms = request.POST['bathrooms']
        listing.floors = request.POST['floors']
        listing.garage = request.POST['garages']
        listing.area = request.POST['area']
        listing.size = request.POST['size']
        listing.property_price = request.POST['property_price']
        listing.property_id = request.POST['Property-ID']
        listing.video_url = request.POST['Video-URL']
        listing.photo_main = request.FILES.get('photo-main') if request.FILES.get('photo-main') else listing.photo_main
        listing.photo_1 = request.FILES.get('photo-1') if request.FILES.get('photo-1') else listing.photo_1
        listing.photo_2 = request.FILES.get('photo-2') if request.FILES.get('photo-2') else listing.photo_2
        listing.photo_3 = request.FILES.get('photo-3') if request.FILES.get('photo-3') else listing.photo_3
        listing.photo_4 = request.FILES.get('photo-4') if request.FILES.get('photo-4') else listing.photo_4
        listing.photo_5 = request.FILES.get('photo-5') if request.FILES.get('photo-5') else listing.photo_5
        listing.photo_6 = request.FILES.get('photo-6') if request.FILES.get('photo-6') else listing.photo_6
        listing.address = request.POST['address']
        listing.country = request.POST['country'] if request.POST['country'] else listing.country
        listing.city = request.POST['city']
        listing.state = request.POST['state']
        listing.zipcode = request.POST['zip-code']
        listing.neighborhood = request.POST['neighborhood']
        listing.save()
        messages.success(request, "Property edit sucsessfully")
        return redirect('main:profile')

    lang = request.session.get('site_language', 'ge')
    context = {
        'listing': listing,
    }
    return render(request, 'main/edit-property.html', context)


@login_required(login_url='main:login_required')
def delete_property(request, id):
    listing = Listing.objects.get(id=id)
    if listing.realtor.user != request.user:
        messages.error(request, "You are not allowed to delete this property.")
        return redirect('main:profile')
    listing.delete()
    messages.success(request, "Property delete sucsessfully")
    return redirect('main:profile')

@login_required(login_url='main:login_required')
def faq(request):
    return render(request, 'main/faq.html')

@login_required(login_url='main:login_required')
def owner(request):
    return render(request, 'main/owner.html')

@login_required(login_url='main:login_required')
def real_estate_agent(request):
    return render(request, 'main/real-estate-agent.html')

@login_required(login_url='main:login_required')
def building_contractor(request):
    return render(request, 'main/building-contractor.html')

@login_required(login_url='main:login_required')
def realestate_contractor_registration(request):
    return render(request, 'main/realestate-contractor-registration.html')

@login_required(login_url='main:login_required')
def owner_form(request):
    return render(request, 'main/owner-form.html')

@login_required(login_url='main:login_required')
def send_owner_form(request):
    if request.method == 'POST':
        try:
            # Get form data
            salutation = request.POST.get('salutation', '').strip()
            firstname = request.POST.get('firstname', '').strip()
            lastname = request.POST.get('lastname', '').strip()
            city = request.POST.get('city', '').strip()
            zipcode = request.POST.get('zipcode', '').strip()
            street = request.POST.get('street', '').strip()
            housenumber = request.POST.get('housenumber', '').strip()
            telephone = request.POST.get('telephone', '').strip()
            mobile = request.POST.get('mobile', '').strip()
            email = request.POST.get('email', '').strip()
            location = request.POST.get('location', '').strip()
            property_type = request.POST.get('property_type', '').strip()
            other_specify = request.POST.get('other_specify', '').strip()
            property_condition = request.POST.get('property_condition', '').strip()
            year_built = request.POST.get('year_built', '').strip()
            living_area = request.POST.get('living_area', '').strip()
            land_area = request.POST.get('land_area', '').strip()
            rooms = request.POST.get('rooms', '').strip()
            bathrooms = request.POST.get('bathrooms', '').strip()
            heating = request.POST.get('heating', '').strip()
            heating_specify = request.POST.get('heating_specify', '').strip()
            energy_certificate = request.POST.get('energy_certificate', '').strip()
            price = request.POST.get('price', '').strip()
            description = request.POST.get('description', '').strip()
            special_features = request.POST.get('special_features', '').strip()
            amenities = request.POST.get('amenities', '').strip()
            renovations = request.POST.get('renovations', '').strip()
            reason_for_sale = request.POST.get('reason_for_sale', '').strip()
            
            # Handle file uploads
            images = request.FILES.getlist('images[]')
            image_files = []
            for image in images:
                if image.content_type not in ['image/jpeg', 'image/png']:
                    return JsonResponse({'status': 'error', 'message': 'Please upload only JPEG or PNG images.'})
                file_name = default_storage.save(image.name, ContentFile(image.read()))
                image_files.append(default_storage.path(file_name))
            
            # Create the email
            email_subject = 'Owner Form Submission'
            email_body_lines = []
            if salutation: email_body_lines.append(f"Anrede: {salutation}")
            if firstname: email_body_lines.append(f"Vorname: {firstname}")
            if lastname: email_body_lines.append(f"Nachname: {lastname}")
            if city: email_body_lines.append(f"Wohnort: {city}")
            if zipcode: email_body_lines.append(f"Postleitzahl: {zipcode}")
            if street: email_body_lines.append(f"Straße: {street}")
            if housenumber: email_body_lines.append(f"Hausnummer: {housenumber}")
            if telephone: email_body_lines.append(f"Telefonnummer: {telephone}")
            if mobile: email_body_lines.append(f"Mobilnummer: {mobile}")
            if email: email_body_lines.append(f"E-Mail Adresse: {email}")
            if location: email_body_lines.append(f"Ort der Immobilie: {location}")
            if property_type: email_body_lines.append(f"Art der Immobilie: {property_type}")
            if other_specify: email_body_lines.append(f"Andere (Bitte spezifizieren): {other_specify}")
            if property_condition: email_body_lines.append(f"Objekttyp: {property_condition}")
            if year_built: email_body_lines.append(f"Baujahr: {year_built}")
            if living_area: email_body_lines.append(f"Wohnfläche: {living_area}")
            if land_area: email_body_lines.append(f"Grundstücksfläche: {land_area}")
            if rooms: email_body_lines.append(f"Anzahl der Zimmer: {rooms}")
            if bathrooms: email_body_lines.append(f"Anzahl der Badezimmer: {bathrooms}")
            if heating: email_body_lines.append(f"Heizungsart: {heating}")
            if heating_specify: email_body_lines.append(f"Andere Heizungsart (Bitte spezifizieren): {heating_specify}")
            if energy_certificate: email_body_lines.append(f"Energieausweis vorhanden: {energy_certificate}")
            if price: email_body_lines.append(f"Verkaufspreis: `{price}€`")
            if description: email_body_lines.append(f"Beschreibung der Immobilie: {description}")
            if special_features: email_body_lines.append(f"Besondere Merkmale oder Ausstattungen: {special_features}")
            if amenities: email_body_lines.append(f"Annehmlichkeiten in der Nähe: {amenities}")
            if renovations: email_body_lines.append(f"Renovierungen oder Modernisierungen in den letzten Jahren: {renovations}")
            if reason_for_sale: email_body_lines.append(f"Grund für den Verkauf: {reason_for_sale}")
            email_body = "\n".join(email_body_lines)
            
            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email='service.mahamudh472@gmail.com',
                to=['office@123-kroatien.eu'],  # Add the recipient email(s) here
            )

            for file_path in image_files:
                email.attach_file(file_path)
                os.remove(file_path)  # Clean up the file after attaching it

            email.send()

            return JsonResponse({'status': 'success', 'message': 'Form submitted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@login_required(login_url='main:login_required')
def send_registration_email(request):
    if request.method == 'POST':
        try:
            # Get form data
            firstname = request.POST.get('firstname')
            postcode = request.POST.get('postcode')
            street = request.POST.get('street')
            housenumber = request.POST.get('housenumber')
            ort = request.POST.get('ort')
            telephone = request.POST.get('telephone')
            mobile = request.POST.get('mobile')
            email = request.POST.get('email')
            realtor = request.POST.get('realtor')
            construction = request.POST.get('construction')
            office = request.POST.get('office')
            oib = request.POST.get('oib')
            website = request.POST.get('website')
            contact_firstname = request.POST.get('contact_firstname')
            contact_lastname = request.POST.get('contact_lastname')
            contact_telephone = request.POST.get('contact_telephone')
            contact_mobile = request.POST.get('contact_mobile')
            contact_email = request.POST.get('contact_email')
            
            # Handle file upload
            business_license = request.FILES.get('business_license')
            if business_license:
                if business_license.content_type != 'application/pdf':
                    return JsonResponse({'status': 'error', 'message': 'Please upload a valid PDF file.'})
                
                # Save the uploaded file
                file_name = default_storage.save(business_license.name, ContentFile(business_license.read()))
                file_path = default_storage.path(file_name)
            else:
                file_path = None

            # Create the email
            email_subject = 'New Registration Form Submission'
            email_body = f"""
                Firmenname: {firstname}
                Postleitzahl: {postcode}
                Straße: {street}
                Hausnummer: {housenumber}
                Ort: {ort}
                Telefonnummer: {telephone}
                Mobilnummer: {mobile}
                E-Mail Adresse: {email}
                Immobilienmakler: {realtor}
                Bauunternehmen: {construction}
                Büroadresse: {office}
                OIB Nummer: {oib}
                Webadresse: {website}
                Ansprechpartner Vorname: {contact_firstname}
                Ansprechpartner Nachname: {contact_lastname}
                Ansprechpartner Telefonnummer: {contact_telephone}
                Ansprechpartner Mobilnummer: {contact_mobile}
                Ansprechpartner E-Mail Adresse: {contact_email}
            """

            email = EmailMessage(
                subject=email_subject,
                body=email_body,
                from_email='service.mahamudh472@gmail.com',
                to=['office@123-kroatien.eu'],  # Add the recipient email(s) here
            )

            if file_path:
                email.attach_file(file_path)
                os.remove(file_path)  # Clean up the file after attaching it

            email.send()

            return JsonResponse({'status': 'success', 'message': 'Form submitted successfully!'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required(login_url='main:login_required')
def send_email(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            # Prepare the email
            subject = 'Contact Form Submission'
            message = f"""
            Salutation: {data.get('salutation')}
            Company: {data.get('company')}
            First Name: {data.get('first_name')}
            Last Name: {data.get('last_name')}
            Street: {data.get('street')}
            ZIP: {data.get('zip')}
            City: {data.get('city')}
            Phone: {data.get('phone')}
            Fax: {data.get('fax')}
            Mobile: {data.get('mobile')}
            Email: {data.get('email')}
            Homepage: {data.get('homepage')}
            Message: {data.get('message')}
            """

            send_mail(
                subject,
                message,
                'service.mahamudh472@gmail.com',  
                ['office@123-kroatien.eu'],
                fail_silently=False,
            )

            return JsonResponse({'status': 'success'})
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# temporary
def loginRequired(request):
    return HttpResponse("Only logged in users can view this page.")


def set_language_from_url(request, user_language):
    request.session['site_language'] = user_language
    translation.activate(user_language)
    referer = request.META.get('HTTP_REFERER', '/')
    # Replace language prefix in URL
    import re
    new_url = re.sub(r'^(https?://[^/]+)?/(ge|en|hr|fr|gr|pl|cz|ru|sw|nb|sl|nl)/', f'/{user_language}/', referer)
    if new_url == referer:
        new_url = f'/{user_language}/'
    return HttpResponseRedirect(new_url)


def agent(request, id):
    # Try Professional first, then Agent
    professional = None
    agent_obj = None
    
    try:
        professional = Professional.objects.get(id=id)
    except (Professional.DoesNotExist, ValueError):
        try:
            agent_obj = Agent.objects.get(id=id)
        except Agent.DoesNotExist:
            from django.http import Http404
            raise Http404("Profil nicht gefunden")
    
    user_language = request.session.get("site_language", "ge")
    
    if professional:
        listings = Listing.objects.filter(email=professional.email) | Listing.objects.filter(oib_number=professional.oib_number)
    else:
        listings = Listing.objects.filter(realtor=agent_obj)
    
    for listing in listings:
        if user_language == "ge": listing.json_content = json.loads(listing.german_content) if listing.german_content else listing.get_json()
        elif user_language == "hr": listing.json_content = json.loads(listing.croatian_content) if listing.croatian_content else listing.get_json()
        elif user_language == "fr": listing.json_content = json.loads(listing.french_content) if listing.french_content else listing.get_json()
        elif user_language == "en": listing.json_content = json.loads(listing.english_content) if listing.english_content else listing.get_json()
        else: listing.json_content = listing.get_json()
    
    lang = request.session.get('site_language', 'ge')
    context = {
        "listings": listings,
        "agent": professional if professional else agent_obj,
        "professional": professional,
        "lang": user_language,
    }
    return render(request, "main/agent.html", context)


def edit_agent(request, id):
    # Try to find Professional first, fallback to Agent
    professional = None
    agent = None
    
    try:
        professional = Professional.objects.get(id=id)
    except (Professional.DoesNotExist, ValueError):
        try:
            agent = Agent.objects.get(id=id)
        except Agent.DoesNotExist:
            messages.error(request, "Profil nicht gefunden.")
            return redirect('main:home')
    
    if request.method == 'POST':
        if professional:
            # Update Professional - Basic Info
            professional.name = request.POST.get('name', professional.name)
            professional.city = request.POST.get('city', professional.city)
            professional.region = request.POST.get('region', professional.region)
            professional.address = request.POST.get('address', professional.address)
            professional.company_name = request.POST.get('company_name', professional.company_name)
            
            # Images
            if request.FILES.get('company_logo'):
                professional.company_logo = request.FILES.get('company_logo')
            if request.FILES.get('portrait_photo'):
                professional.portrait_photo = request.FILES.get('portrait_photo')
            if request.FILES.get('profile_image'):
                professional.profile_image = request.FILES.get('profile_image')
            
            # Extended company info (NEW)
            professional.slogan = request.POST.get('slogan', professional.slogan)
            professional.founded_year = request.POST.get('founded_year') or None
            professional.employee_count = request.POST.get('employee_count', professional.employee_count)
            professional.specializations = request.POST.get('specializations', professional.specializations)
            
            # Contact info
            professional.oib_number = request.POST.get('oib_number', professional.oib_number)
            professional.website = request.POST.get('domain', professional.website)
            professional.mobile = request.POST.get('mobile', professional.mobile)
            professional.fax = request.POST.get('fax', professional.fax)
            professional.phone = request.POST.get('phone', professional.phone)
            languages_list = request.POST.getlist('languages'); professional.languages = ', '.join(languages_list) if languages_list else professional.languages
            
            # Social Media
            professional.facebook = request.POST.get('facebook', professional.facebook)
            professional.instagram = request.POST.get('instagram', professional.instagram)
            professional.linkedin = request.POST.get('linkedin', professional.linkedin)
            professional.youtube = request.POST.get('youtube', professional.youtube)
            professional.twitter = request.POST.get('twitter', professional.twitter)
            professional.tiktok = request.POST.get('tiktok', professional.tiktok)
            
            # Description
            professional.description = request.POST.get('description', professional.description)
            professional.description_de = request.POST.get('description_de', professional.description_de)
            professional.description_hr = request.POST.get('description_hr', professional.description_hr)
            
            # Display toggles (checkboxes)
            professional.show_references = 'show_references' in request.POST
            professional.show_contact_form = 'show_contact_form' in request.POST
            professional.show_listings = 'show_listings' in request.POST
            professional.show_social_media = 'show_social_media' in request.POST
            professional.show_team = 'show_team' in request.POST
            
            professional.save()
            messages.success(request, "Profil erfolgreich aktualisiert")
            return redirect('main:agent', id=id)
        else:
            # Update Agent (legacy)
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            gender = request.POST['gender']
            city = request.POST['city']
            country = request.POST['country']
            company_name = request.POST['company_name']
            company_logo = request.FILES.get('company_logo') if request.FILES.get('company_logo') else agent.company_logo
            portrait_photo = request.FILES.get('portrait_photo') if request.FILES.get('portrait_photo') else agent.profile_image
            oib_number = request.POST['oib_number']
            domain = request.POST['domain']
            facebook = request.POST['facebook']
            instagram = request.POST['instagram']
            linkedin = request.POST['linkedin']
            youtube = request.POST['youtube']
            twitter = request.POST['twitter']
            description = request.POST['description']
            mobile = request.POST['mobile']
            fax = request.POST['fax']

            user = agent.user
            user.first_name = first_name
            user.last_name = last_name
            agent.first_name = first_name
            agent.last_name = last_name
            agent.gender = gender   
            agent.city = city
            agent.country = country
            agent.company_name = company_name
            agent.company_logo = company_logo
            agent.profile_image = portrait_photo
            agent.oib_number = oib_number
            agent.domain = domain
            agent.facebook = facebook
            agent.instagram = instagram
            agent.linkedin = linkedin
            agent.youtube = youtube
            agent.twitter = twitter
            agent.description = description
            agent.mobile = mobile
            agent.fax = fax
            user.save()
            agent.save()
            messages.success(request, "Profil erfolgreich aktualisiert")
            return redirect('main:agent', id=id)

    lang = request.session.get('site_language', 'ge')
    context = {
        'agent': agent,
        'professional': professional,
        'regions': Professional.REGIONS,
        'lang': lang,
    }
    
    # Use extended template for Professional, legacy template for Agent
    if professional:
        return render(request, 'main/edit-agent-professional.html', context)
    return render(request, 'main/edit-agent.html', context)


# Reference Projects Management Views
from main.professional_models import ReferenceProject

@login_required(login_url='account:login')
def reference_projects_list(request, id):
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        messages.error(request, "Profil nicht gefunden.")
        return redirect('main:home')
    
    if professional.user != request.user:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    projects = ReferenceProject.objects.filter(professional=professional)
    
    lang = request.session.get('site_language', 'ge')
    context = {
        'professional': professional,
        'projects': projects,
    }
    return render(request, 'main/reference_projects_list.html', context)


@login_required(login_url='account:login')
def reference_project_create(request, id):
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        messages.error(request, "Profil nicht gefunden.")
        return redirect('main:home')
    
    if professional.user != request.user:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    if request.method == 'POST':
        project = ReferenceProject(professional=professional)
        project.title = request.POST.get('title', '')
        project.description = request.POST.get('description', '')
        project.year = request.POST.get('year') or None
        project.location = request.POST.get('location', '')
        project.project_type = request.POST.get('project_type', '')
        project.sort_order = request.POST.get('sort_order') or 0
        project.is_featured = 'is_featured' in request.POST
        
        for i in range(1, 7):
            img_field = f'image_{i}'
            if request.FILES.get(img_field):
                setattr(project, img_field, request.FILES.get(img_field))
        
        project.save()
        messages.success(request, "Referenzprojekt erfolgreich erstellt!")
        return redirect('main:reference_projects_list', id=id)
    
    lang = request.session.get('site_language', 'ge')
    context = {
        'professional': professional,
        'is_edit': False,
    }
    return render(request, 'main/reference_project_form.html', context)


@login_required(login_url='account:login')
def reference_project_edit(request, id, project_id):
    try:
        professional = Professional.objects.get(id=id)
        project = ReferenceProject.objects.get(id=project_id, professional=professional)
    except (Professional.DoesNotExist, ReferenceProject.DoesNotExist):
        messages.error(request, "Projekt nicht gefunden.")
        return redirect('main:home')
    
    if professional.user != request.user:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    if request.method == 'POST':
        project.title = request.POST.get('title', project.title)
        project.description = request.POST.get('description', project.description)
        project.year = request.POST.get('year') or None
        project.location = request.POST.get('location', project.location)
        project.project_type = request.POST.get('project_type', project.project_type)
        project.sort_order = request.POST.get('sort_order') or 0
        project.is_featured = 'is_featured' in request.POST
        
        for i in range(1, 7):
            img_field = f'image_{i}'
            if request.FILES.get(img_field):
                setattr(project, img_field, request.FILES.get(img_field))
            if request.POST.get(f'delete_image_{i}'):
                setattr(project, img_field, None)
        
        project.save()
        messages.success(request, "Referenzprojekt erfolgreich aktualisiert!")
        return redirect('main:reference_projects_list', id=id)
    
    lang = request.session.get('site_language', 'ge')
    context = {
        'professional': professional,
        'project': project,
        'is_edit': True,
    }
    return render(request, 'main/reference_project_form.html', context)


@login_required(login_url='account:login')
def reference_project_delete(request, id, project_id):
    try:
        professional = Professional.objects.get(id=id)
        project = ReferenceProject.objects.get(id=project_id, professional=professional)
    except (Professional.DoesNotExist, ReferenceProject.DoesNotExist):
        messages.error(request, "Projekt nicht gefunden.")
        return redirect('main:home')
    
    if professional.user != request.user:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Referenzprojekt erfolgreich gelöscht!")
    
    return redirect('main:reference_projects_list', id=id)


# Professional Registration View (Bilingual: German & Croatian)
def professional_registration(request, lang='ge'):
    success = True
    if request.method == 'POST':
        try:
            data = request.POST
            prof_types = {'realtor':'Immobilienmakler','construction':'Bauunternehmen','lawyer':'Rechtsanwalt','tax_advisor':'Steuerberater','architect':'Architekt'}
            body = f"""
NEUE PROFESSIONAL-REGISTRIERUNG

Typ: {prof_types.get(data.get('professional_type',''), data.get('professional_type',''))}
Firmenname: {data.get('company_name','')}
PLZ: {data.get('postcode','')}
Strasse: {data.get('street','')} {data.get('housenumber','')}
Ort: {data.get('city','')}
Telefon: {data.get('telephone','')}
Mobil: {data.get('mobile','')}
E-Mail: {data.get('email','')}
Website: {data.get('website','')}
OIB: {data.get('oib','')}

ANSPRECHPARTNER:
Anrede: {data.get('contact_gender','')}
Name: {data.get('contact_firstname','')} {data.get('contact_lastname','')}
E-Mail: {data.get('contact_email','')}
Telefon: {data.get('contact_telephone','')}
"""
            send_mail('Neue Professional-Registrierung', body, 'service.mahamudh472@gmail.com', ['office@123-kroatien.eu'], fail_silently=False)
            success = True; print("=== SUCCESS IST TRUE ===")
        except Exception as e:
            print(f'Email error: {e}')
    lang = request.session.get('site_language', 'ge')
    context = {'lang': lang, 'success': success}
    if success: return redirect('main:registration-success')
    return render(request, 'main/professional_registration.html', context)


# =============================================================================
# AI SMART-SEARCH VIEW
# =============================================================================
from main.chatbot import extract_search_criteria, is_property_search, smart_search_response, get_chatbot_response_with_search

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

# =============================================================================
# RSS FEEDS - SEO & AI OPTIMIERT (12 Sprachen)
# =============================================================================
from django.http import HttpResponse
import feedparser
from django.utils import timezone
from datetime import datetime
import xml.etree.ElementTree as ET

# Sprach-spezifische Texte für RSS
RSS_TRANSLATIONS = {
    'ge': {
        'site_title': '123-Kroatien.eu - Immobilienmarktplatz Kroatien',
        'site_description': 'Der führende Immobilienmarktplatz für Kroatien. Finden Sie Häuser, Wohnungen und Grundstücke an der Adria.',
        'listings_title': 'Neue Immobilien in Kroatien',
        'listings_description': 'Aktuelle Immobilienangebote aus Kroatien - Häuser, Wohnungen, Villen und Grundstücke',
    },
    'en': {
        'site_title': '123-Kroatien.eu - Croatia Real Estate Marketplace',
        'site_description': 'The leading real estate marketplace for Croatia. Find houses, apartments and land on the Adriatic coast.',
        'listings_title': 'New Properties in Croatia',
        'listings_description': 'Current real estate offers from Croatia - houses, apartments, villas and land',
    },
    'hr': {
        'site_title': '123-Kroatien.eu - Tržište nekretnina u Hrvatskoj',
        'site_description': 'Vodeće tržište nekretnina za Hrvatsku. Pronađite kuće, stanove i zemljišta na Jadranu.',
        'listings_title': 'Nove nekretnine u Hrvatskoj',
        'listings_description': 'Aktualne ponude nekretnina iz Hrvatske - kuće, stanovi, vile i zemljišta',
    },
    'fr': {
        'site_title': '123-Kroatien.eu - Marché immobilier Croatie',
        'site_description': 'Le premier marché immobilier pour la Croatie. Trouvez maisons, appartements et terrains sur la côte Adriatique.',
        'listings_title': 'Nouvelles propriétés en Croatie',
        'listings_description': 'Offres immobilières actuelles de Croatie - maisons, appartements, villas et terrains',
    },
    'nl': {
        'site_title': '123-Kroatien.eu - Vastgoedmarkt Kroatië',
        'site_description': 'De toonaangevende vastgoedmarkt voor Kroatië. Vind huizen, appartementen en grond aan de Adriatische kust.',
        'listings_title': 'Nieuwe woningen in Kroatië',
        'listings_description': 'Actuele vastgoedaanbiedingen uit Kroatië - huizen, appartementen, villa\'s en grond',
    },
    'pl': {
        'site_title': '123-Kroatien.eu - Rynek nieruchomości Chorwacja',
        'site_description': 'Wiodący rynek nieruchomości w Chorwacji. Znajdź domy, mieszkania i działki nad Adriatykiem.',
        'listings_title': 'Nowe nieruchomości w Chorwacji',
        'listings_description': 'Aktualne oferty nieruchomości z Chorwacji - domy, mieszkania, wille i działki',
    },
    'cz': {
        'site_title': '123-Kroatien.eu - Realitní trh Chorvatsko',
        'site_description': 'Přední realitní trh pro Chorvatsko. Najděte domy, byty a pozemky na Jadranu.',
        'listings_title': 'Nové nemovitosti v Chorvatsku',
        'listings_description': 'Aktuální nabídky nemovitostí z Chorvatska - domy, byty, vily a pozemky',
    },
    'sk': {
        'site_title': '123-Kroatien.eu - Realitný trh Chorvátsko',
        'site_description': 'Popredný realitný trh pre Chorvátsko. Nájdite domy, byty a pozemky na Jadrane.',
        'listings_title': 'Nové nehnuteľnosti v Chorvátsku',
        'listings_description': 'Aktuálne ponuky nehnuteľností z Chorvátska - domy, byty, vily a pozemky',
    },
    'ru': {
        'site_title': '123-Kroatien.eu - Рынок недвижимости Хорватии',
        'site_description': 'Ведущий рынок недвижимости Хорватии. Найдите дома, квартиры и участки на Адриатике.',
        'listings_title': 'Новая недвижимость в Хорватии',
        'listings_description': 'Актуальные предложения недвижимости из Хорватии - дома, квартиры, виллы и участки',
    },
    'gr': {
        'site_title': '123-Kroatien.eu - Αγορά ακινήτων Κροατία',
        'site_description': 'Η κορυφαία αγορά ακινήτων για την Κροατία. Βρείτε σπίτια, διαμερίσματα και οικόπεδα στην Αδριατική.',
        'listings_title': 'Νέα ακίνητα στην Κροατία',
        'listings_description': 'Τρέχουσες προσφορές ακινήτων από την Κροατία - σπίτια, διαμερίσματα, βίλες και οικόπεδα',
    },
    'sw': {
        'site_title': '123-Kroatien.eu - Fastighetsmarknad Kroatien',
        'site_description': 'Den ledande fastighetsmarknaden för Kroatien. Hitta hus, lägenheter och mark vid Adriatiska havet.',
        'listings_title': 'Nya fastigheter i Kroatien',
        'listings_description': 'Aktuella fastighetserbjudanden från Kroatien - hus, lägenheter, villor och mark',
    },
    'no': {
        'site_title': '123-Kroatien.eu - Eiendomsmarked Kroatia',
        'site_description': 'Det ledende eiendomsmarkedet for Kroatia. Finn hus, leiligheter og tomter ved Adriaterhavet.',
        'listings_title': 'Nye eiendommer i Kroatia',
        'listings_description': 'Aktuelle eiendomstilbud fra Kroatia - hus, leiligheter, villaer og tomter',
    },
}

COUNTRY_NAMES = {
    'ge': 'kroatien', 'en': 'croatia', 'hr': 'hrvatska', 'fr': 'croatie',
    'nl': 'kroatie', 'pl': 'chorwacja', 'cz': 'chorvatsko', 'sk': 'chorvatsko',
    'ru': 'horvatiya', 'gr': 'kroatia', 'sw': 'kroatien', 'no': 'kroatia',
}


def rss_listings(request, lang='ge'):
    """
    RSS Feed für Immobilien-Listings
    SEO + AI optimiert
    """
    trans = RSS_TRANSLATIONS.get(lang, RSS_TRANSLATIONS['ge'])
    country = COUNTRY_NAMES.get(lang, 'kroatien')
    base_url = request.build_absolute_uri('/').rstrip('/')
    
    # XML erstellen
    rss = ET.Element('rss', version='2.0')
    rss.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    rss.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    
    channel = ET.SubElement(rss, 'channel')
    
    # Channel Info
    ET.SubElement(channel, 'title').text = trans['listings_title']
    ET.SubElement(channel, 'description').text = trans['listings_description']
    ET.SubElement(channel, 'link').text = f"{base_url}/{lang}/"
    ET.SubElement(channel, 'language').text = lang if lang != 'ge' else 'de'
    ET.SubElement(channel, 'lastBuildDate').text = timezone.now().strftime('%a, %d %b %Y %H:%M:%S %z')
    ET.SubElement(channel, 'generator').text = '123-Kroatien.eu RSS Generator'
    
    # Atom self link
    atom_link = ET.SubElement(channel, 'atom:link')
    atom_link.set('href', f"{base_url}/{lang}/rss/listings/")
    atom_link.set('rel', 'self')
    atom_link.set('type', 'application/rss+xml')
    
    # Image
    image = ET.SubElement(channel, 'image')
    ET.SubElement(image, 'url').text = f"{base_url}/static/images/logo-black2.png"
    ET.SubElement(image, 'title').text = trans['site_title']
    ET.SubElement(image, 'link').text = f"{base_url}/{lang}/"
    
    # Listings holen
    listings = Listing.objects.filter(is_published=True).order_by('-list_date')[:50]
    
    for listing in listings:
        # Sprachspezifischen Content laden
        if lang == 'ge' and listing.german_content:
            content = json.loads(listing.german_content)
        elif lang == 'en' and listing.english_content:
            content = json.loads(listing.english_content)
        elif lang == 'hr' and listing.croatian_content:
            content = json.loads(listing.croatian_content)
        elif lang == 'fr' and listing.french_content:
            content = json.loads(listing.french_content)
        elif lang == 'nl' and listing.dutch_content:
            content = json.loads(listing.dutch_content)
        elif lang == 'pl' and listing.polish_content:
            content = json.loads(listing.polish_content)
        elif lang == 'cz' and listing.czech_content:
            content = json.loads(listing.czech_content)
        elif lang == 'sk' and listing.slovak_content:
            content = json.loads(listing.slovak_content)
        elif lang == 'ru' and listing.russian_content:
            content = json.loads(listing.russian_content)
        elif lang == 'gr' and listing.greek_content:
            content = json.loads(listing.greek_content)
        elif lang == 'sw' and listing.swedish_content:
            content = json.loads(listing.swedish_content)
        elif lang == 'no' and listing.norway_content:
            content = json.loads(listing.norway_content)
        else:
            content = listing.get_json()
        
        item = ET.SubElement(channel, 'item')
        
        title = content.get('property_title', listing.property_title)
        ET.SubElement(item, 'title').text = title
        ET.SubElement(item, 'link').text = f"{base_url}/{lang}/property-details/{listing.id}/"
        ET.SubElement(item, 'guid').text = f"{base_url}/{lang}/property-details/{listing.id}/"
        
        # Nur Teaser - kein voller Content (Schutz vor Kopieren)
        teaser_texts = {
            'ge': f"{listing.property_type} in {listing.location} - {listing.bedrooms} Schlafzimmer, {listing.bathrooms} Bäder, {listing.area} m² - Mehr Details auf 123-kroatien.eu",
            'en': f"{listing.property_type} in {listing.location} - {listing.bedrooms} bedrooms, {listing.bathrooms} baths, {listing.area} m² - More details at 123-kroatien.eu",
            'hr': f"{listing.property_type} u {listing.location} - {listing.bedrooms} spavaće sobe, {listing.bathrooms} kupaonice, {listing.area} m² - Više detalja na 123-kroatien.eu",
        }
        teaser = teaser_texts.get(lang, teaser_texts['ge'])
        ET.SubElement(item, 'description').text = teaser
        
        ET.SubElement(item, 'pubDate').text = listing.list_date.strftime('%a, %d %b %Y %H:%M:%S %z') if listing.list_date else ''
        ET.SubElement(item, 'dc:creator').text = '123-Kroatien.eu'
        
        # Kategorie
        ET.SubElement(item, 'category').text = listing.property_type
        ET.SubElement(item, 'category').text = listing.property_status
        ET.SubElement(item, 'category').text = listing.location
    
    # XML Response
    xml_str = ET.tostring(rss, encoding='unicode', method='xml')
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    
    return HttpResponse(xml_declaration + xml_str, content_type='application/rss+xml; charset=utf-8')


# =============================================================================
# XML SITEMAP - SEO + AI OPTIMIERT (12 Sprachen)
# =============================================================================

def xml_sitemap(request):
    """
    Dynamische XML Sitemap mit allen Seiten in 12 Sprachen
    Für Suchmaschinen und AI-Crawler optimiert
    """
    base_url = request.build_absolute_uri('/').rstrip('/')
    
    LANGUAGES = ['ge', 'en', 'hr', 'fr', 'nl', 'pl', 'cz', 'sk', 'ru', 'gr', 'sw', 'no']
    LANG_CODES = {
        'ge': 'de', 'en': 'en', 'hr': 'hr', 'fr': 'fr', 'nl': 'nl', 'pl': 'pl',
        'cz': 'cs', 'sk': 'sk', 'ru': 'ru', 'gr': 'el', 'sw': 'sv', 'no': 'no'
    }
    COUNTRY_NAMES = {
        'ge': 'kroatien', 'en': 'croatia', 'hr': 'hrvatska', 'fr': 'croatie',
        'nl': 'kroatie', 'pl': 'chorwacja', 'cz': 'chorvatsko', 'sk': 'chorvatsko',
        'ru': 'horvatiya', 'gr': 'kroatia', 'sw': 'kroatien', 'no': 'kroatia',
    }
    
    # XML erstellen
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
    xml_content += 'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
    
    # Statische Seiten
    static_pages = ['', 'about/', 'contact/', 'listings/', 'faq/', 'blog/']
    
    for page in static_pages:
        for lang in LANGUAGES:
            xml_content += '  <url>\n'
            xml_content += f'    <loc>{base_url}/{lang}/{page}</loc>\n'
            xml_content += '    <changefreq>weekly</changefreq>\n'
            xml_content += '    <priority>0.8</priority>\n'
            # Hreflang für alle Sprachen
            for alt_lang in LANGUAGES:
                xml_content += f'    <xhtml:link rel="alternate" hreflang="{LANG_CODES[alt_lang]}" href="{base_url}/{alt_lang}/{page}"/>\n'
            xml_content += '  </url>\n'
    
    # Immobilien-Listings
    listings = Listing.objects.filter(is_published=True)
    for listing in listings:
        for lang in LANGUAGES:
            xml_content += '  <url>\n'
            xml_content += f'    <loc>{base_url}/{lang}/property-details/{listing.id}/</loc>\n'
            xml_content += '    <changefreq>daily</changefreq>\n'
            xml_content += '    <priority>0.9</priority>\n'
            for alt_lang in LANGUAGES:
                xml_content += f'    <xhtml:link rel="alternate" hreflang="{LANG_CODES[alt_lang]}" href="{base_url}/{alt_lang}/property-details/{listing.id}/"/>\n'
            xml_content += '  </url>\n'
    
    # Professional Pages
    professional_types = ['immobilienmakler', 'bauunternehmen', 'rechtsanwaelte', 'steuerberater', 'architekten']
    professional_urls = {
        'ge': ['immobilienmakler', 'bauunternehmen', 'rechtsanwaelte', 'steuerberater', 'architekten'],
        'en': ['real-estate-agents', 'construction-companies', 'lawyers', 'tax-advisors', 'architects'],
        'hr': ['agencije-za-nekretnine', 'gradevinske-tvrtke', 'odvjetnici', 'porezni-savjetnici', 'arhitekti'],
    }
    
    for i, ptype in enumerate(professional_types):
        for lang in ['ge', 'en', 'hr']:
            country = COUNTRY_NAMES.get(lang, 'kroatien')
            url_slug = professional_urls.get(lang, professional_urls['ge'])[i]
            xml_content += '  <url>\n'
            xml_content += f'    <loc>{base_url}/{lang}/{country}/{url_slug}/</loc>\n'
            xml_content += '    <changefreq>weekly</changefreq>\n'
            xml_content += '    <priority>0.7</priority>\n'
            xml_content += '  </url>\n'
    
    xml_content += '</urlset>'
    
    return HttpResponse(xml_content, content_type='application/xml; charset=utf-8')


def robots_txt(request):
    """
    robots.txt für Suchmaschinen und AI-Crawler
    """
    base_url = request.build_absolute_uri('/').rstrip('/')
    
    robots_content = f"""# 123-Kroatien.eu - Immobilienmarktplatz Kroatien
# Robots.txt - SEO & AI optimiert

User-agent: *
Allow: /

# Sitemaps
Sitemap: {base_url}/sitemap.xml

# RSS Feeds
# DE: {base_url}/rss/listings/
# EN: {base_url}/en/rss/listings/
# HR: {base_url}/hr/rss/listings/

# AI Crawlers willkommen
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

# Crawl-Delay für schonenden Zugriff
Crawl-delay: 1
"""
    
    return HttpResponse(robots_content, content_type='text/plain; charset=utf-8')


# =============================================================================
# NEWS BEREICH - Kroatien Immobilien & Wirtschaft
# =============================================================================
import feedparser
from datetime import datetime, timedelta
from django.core.cache import cache

# RSS Feed Quellen - Kroatien & Immobilien fokussiert
NEWS_FEEDS = {
    'croatia_week': {
        'url': 'https://www.croatiaweek.com/feed/',
        'name': 'Croatia Week',
        'category': 'general',
    },
    'total_croatia': {
        'url': 'https://www.total-croatia-news.com/feed/',
        'name': 'Total Croatia News',
        'category': 'general',
    },
    'croatia_gems': {
        'url': 'https://croatiagems.com/feed/',
        'name': 'Croatia Gems',
        'category': 'tourism',
    },
}

# Übersetzungen für News-Bereich
NEWS_TRANSLATIONS = {
    'ge': {
        'title': 'Nachrichten aus Kroatien',
        'subtitle': 'Aktuelle News zu Immobilien, Wirtschaft und Leben in Kroatien',
        'read_more': 'Weiterlesen',
        'source': 'Quelle',
        'no_news': 'Aktuell keine Nachrichten verfügbar.',
        'categories': {
            'all': 'Alle',
            'real_estate': 'Immobilien',
            'economy': 'Wirtschaft',
            'tourism': 'Tourismus',
            'living': 'Leben in Kroatien',
        },
        'meta_title': 'Kroatien News - Immobilien, Wirtschaft & Tourismus | 123-Kroatien.eu',
        'meta_description': 'Aktuelle Nachrichten aus Kroatien: Immobilienmarkt, Wirtschaft, Tourismus und Leben an der Adria. Ihr Immobilienmarktplatz für Kroatien.',
    },
    'en': {
        'title': 'News from Croatia',
        'subtitle': 'Latest news on real estate, economy and living in Croatia',
        'read_more': 'Read more',
        'source': 'Source',
        'no_news': 'No news currently available.',
        'categories': {
            'all': 'All',
            'real_estate': 'Real Estate',
            'economy': 'Economy',
            'tourism': 'Tourism',
            'living': 'Living in Croatia',
        },
        'meta_title': 'Croatia News - Real Estate, Economy & Tourism | 123-Kroatien.eu',
        'meta_description': 'Latest news from Croatia: real estate market, economy, tourism and life on the Adriatic. Your real estate marketplace for Croatia.',
    },
    'hr': {
        'title': 'Vijesti iz Hrvatske',
        'subtitle': 'Najnovije vijesti o nekretninama, gospodarstvu i životu u Hrvatskoj',
        'read_more': 'Pročitaj više',
        'source': 'Izvor',
        'no_news': 'Trenutno nema dostupnih vijesti.',
        'categories': {
            'all': 'Sve',
            'real_estate': 'Nekretnine',
            'economy': 'Gospodarstvo',
            'tourism': 'Turizam',
            'living': 'Život u Hrvatskoj',
        },
        'meta_title': 'Vijesti iz Hrvatske - Nekretnine, Gospodarstvo & Turizam | 123-Kroatien.eu',
        'meta_description': 'Najnovije vijesti iz Hrvatske: tržište nekretnina, gospodarstvo, turizam i život na Jadranu. Vaše tržište nekretnina za Hrvatsku.',
    },
    'fr': {
        'title': 'Actualités de Croatie',
        'subtitle': 'Dernières nouvelles sur immobilier, économie et vie en Croatie',
        'read_more': 'Lire la suite',
        'source': 'Source',
        'no_news': 'Aucune actualité disponible.',
        'categories': {
            'all': 'Tout',
            'real_estate': 'Immobilier',
            'economy': 'Économie',
            'tourism': 'Tourisme',
            'living': 'Vivre en Croatie',
        },
        'meta_title': 'Actualités Croatie - Immobilier, Économie & Tourisme | 123-Kroatien.eu',
        'meta_description': 'Dernières nouvelles de Croatie: marché immobilier, économie, tourisme et vie sur Adriatique.',
    },
    'nl': {
        'title': 'Nieuws uit Kroatië',
        'subtitle': 'Laatste nieuws over vastgoed, economie en leven in Kroatië',
        'read_more': 'Lees meer',
        'source': 'Bron',
        'no_news': 'Momenteel geen nieuws beschikbaar.',
        'categories': {
            'all': 'Alles',
            'real_estate': 'Vastgoed',
            'economy': 'Economie',
            'tourism': 'Toerisme',
            'living': 'Wonen in Kroatië',
        },
        'meta_title': 'Kroatië Nieuws - Vastgoed, Economie & Toerisme | 123-Kroatien.eu',
        'meta_description': 'Laatste nieuws uit Kroatië: vastgoedmarkt, economie, toerisme en leven aan de Adriatische kust.',
    },
    'pl': {
        'title': 'Wiadomości z Chorwacji',
        'subtitle': 'Najnowsze wiadomości o nieruchomościach, gospodarce i życiu w Chorwacji',
        'read_more': 'Czytaj więcej',
        'source': 'Źródło',
        'no_news': 'Brak dostępnych wiadomości.',
        'categories': {
            'all': 'Wszystko',
            'real_estate': 'Nieruchomości',
            'economy': 'Gospodarka',
            'tourism': 'Turystyka',
            'living': 'Życie w Chorwacji',
        },
        'meta_title': 'Wiadomości Chorwacja - Nieruchomości, Gospodarka & Turystyka | 123-Kroatien.eu',
        'meta_description': 'Najnowsze wiadomości z Chorwacji: rynek nieruchomości, gospodarka, turystyka i życie nad Adriatykiem.',
    },
    'cz': {
        'title': 'Zprávy z Chorvatska',
        'subtitle': 'Nejnovější zprávy o nemovitostech, ekonomice a životě v Chorvatsku',
        'read_more': 'Číst dále',
        'source': 'Zdroj',
        'no_news': 'Žádné zprávy nejsou k dispozici.',
        'categories': {
            'all': 'Vše',
            'real_estate': 'Nemovitosti',
            'economy': 'Ekonomika',
            'tourism': 'Turismus',
            'living': 'Život v Chorvatsku',
        },
        'meta_title': 'Zprávy Chorvatsko - Nemovitosti, Ekonomika & Turismus | 123-Kroatien.eu',
        'meta_description': 'Nejnovější zprávy z Chorvatska: trh nemovitostí, ekonomika, turismus a život na Jadranu.',
    },
    'sk': {
        'title': 'Správy z Chorvátska',
        'subtitle': 'Najnovšie správy o nehnuteľnostiach, ekonomike a živote v Chorvátsku',
        'read_more': 'Čítať ďalej',
        'source': 'Zdroj',
        'no_news': 'Žiadne správy nie sú k dispozícii.',
        'categories': {
            'all': 'Všetko',
            'real_estate': 'Nehnuteľnosti',
            'economy': 'Ekonomika',
            'tourism': 'Turizmus',
            'living': 'Život v Chorvátsku',
        },
        'meta_title': 'Správy Chorvátsko - Nehnuteľnosti, Ekonomika & Turizmus | 123-Kroatien.eu',
        'meta_description': 'Najnovšie správy z Chorvátska: trh nehnuteľností, ekonomika, turizmus a život na Jadrane.',
    },
    'ru': {
        'title': 'Новости Хорватии',
        'subtitle': 'Последние новости о недвижимости, экономике и жизни в Хорватии',
        'read_more': 'Читать далее',
        'source': 'Источник',
        'no_news': 'Новости недоступны.',
        'categories': {
            'all': 'Все',
            'real_estate': 'Недвижимость',
            'economy': 'Экономика',
            'tourism': 'Туризм',
            'living': 'Жизнь в Хорватии',
        },
        'meta_title': 'Новости Хорватии - Недвижимость, Экономика & Туризм | 123-Kroatien.eu',
        'meta_description': 'Последние новости из Хорватии: рынок недвижимости, экономика, туризм и жизнь на Адриатике.',
    },
    'gr': {
        'title': 'Νέα από την Κροατία',
        'subtitle': 'Τελευταία νέα για ακίνητα, οικονομία και ζωή στην Κροατία',
        'read_more': 'Διαβάστε περισσότερα',
        'source': 'Πηγή',
        'no_news': 'Δεν υπάρχουν διαθέσιμα νέα.',
        'categories': {
            'all': 'Όλα',
            'real_estate': 'Ακίνητα',
            'economy': 'Οικονομία',
            'tourism': 'Τουρισμός',
            'living': 'Ζωή στην Κροατία',
        },
        'meta_title': 'Νέα Κροατίας - Ακίνητα, Οικονομία & Τουρισμός | 123-Kroatien.eu',
        'meta_description': 'Τελευταία νέα από την Κροατία: αγορά ακινήτων, οικονομία, τουρισμός και ζωή στην Αδριατική.',
    },
    'sw': {
        'title': 'Nyheter från Kroatien',
        'subtitle': 'Senaste nytt om fastigheter, ekonomi och livet i Kroatien',
        'read_more': 'Läs mer',
        'source': 'Källa',
        'no_news': 'Inga nyheter tillgängliga.',
        'categories': {
            'all': 'Alla',
            'real_estate': 'Fastigheter',
            'economy': 'Ekonomi',
            'tourism': 'Turism',
            'living': 'Livet i Kroatien',
        },
        'meta_title': 'Kroatien Nyheter - Fastigheter, Ekonomi & Turism | 123-Kroatien.eu',
        'meta_description': 'Senaste nytt från Kroatien: fastighetsmarknad, ekonomi, turism och livet vid Adriatiska havet.',
    },
    'no': {
        'title': 'Nyheter fra Kroatia',
        'subtitle': 'Siste nytt om eiendom, økonomi og livet i Kroatia',
        'read_more': 'Les mer',
        'source': 'Kilde',
        'no_news': 'Ingen nyheter tilgjengelig.',
        'categories': {
            'all': 'Alle',
            'real_estate': 'Eiendom',
            'economy': 'Økonomi',
            'tourism': 'Turisme',
            'living': 'Livet i Kroatia',
        },
        'meta_title': 'Kroatia Nyheter - Eiendom, Økonomi & Turisme | 123-Kroatien.eu',
        'meta_description': 'Siste nytt fra Kroatia: eiendomsmarked, økonomi, turisme og livet ved Adriaterhavet.',
    },
}


def fetch_news_feeds():
    """
    Holt News von externen RSS-Feeds
    Mit Caching für Performance
    """
    cache_key = 'croatia_news_feeds'
    cached_news = cache.get(cache_key)
    
    if cached_news:
        return cached_news
    
    all_news = []
    
    for feed_id, feed_info in NEWS_FEEDS.items():
        try:
            feed = feedparser.parse(feed_info['url'])
            
            for entry in feed.entries[:10]:  # Max 10 pro Quelle
                # Datum parsen
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])
                else:
                    published = datetime.now()
                
                # Bild extrahieren (wenn vorhanden)
                image = None
                if hasattr(entry, 'media_content') and entry.media_content:
                    image = entry.media_content[0].get('url')
                elif hasattr(entry, 'enclosures') and entry.enclosures:
                    for enc in entry.enclosures:
                        if 'image' in enc.get('type', ''):
                            image = enc.get('href')
                            break
                
                news_item = {
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'description': entry.get('summary', '')[:300] if entry.get('summary') else '',
                    'published': published,
                    'source': feed_info['name'],
                    'category': feed_info['category'],
                    'image': image,
                }
                all_news.append(news_item)
                
        except Exception as e:
            print(f"Feed Error ({feed_id}): {e}")
            continue
    
    # Nach Datum sortieren (neueste zuerst)
    all_news.sort(key=lambda x: x['published'] if x['published'] else datetime.min, reverse=True)
    
    # Cache für 30 Minuten
    cache.set(cache_key, all_news, 1800)
    
    return all_news


def news_page(request, country=None, lang=None):
    # Lang aus country ermitteln falls nicht direkt übergeben
    if lang is None and country:
        country_to_lang = {
            'kroatien': 'ge', 'croatia': 'en', 'hrvatska': 'hr', 'croatie': 'fr',
            'kroatie': 'nl', 'chorwacja': 'pl', 'chorvatsko': 'cz',
            'horvatiya': 'ru', 'kroatia': 'gr',
        }
        lang = country_to_lang.get(country, 'ge')
    if lang is None:
        lang = request.session.get('site_language', 'ge')
    """
    News-Seite mit Kroatien-Nachrichten
    SEO & AI optimiert
    """
    trans = NEWS_TRANSLATIONS.get(lang, NEWS_TRANSLATIONS['ge'])
    news_items = fetch_news_feeds()
    
    # Filter by category if provided
    category = request.GET.get('category', 'all')
    if category != 'all':
        news_items = [n for n in news_items if n['category'] == category]
    
    lang = request.session.get('site_language', 'ge')
    context = {
        'news_items': news_items[:30],  # Max 30 Artikel
        'trans': trans,
        'lang': lang,
        'current_category': category,
        'meta_title': trans['meta_title'],
        'meta_description': trans['meta_description'],
    }
    
    return render(request, 'main/news.html', context)


# === ANFRAGE AN MAKLER (E-Mail Benachrichtigung) ===
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
import json

@csrf_exempt
def send_listing_inquiry(request):
    """Sendet eine Anfrage zu einer Immobilie an den Makler (mit Spam-Schutz)"""
    if request.method == 'POST':
        try:
            # === RATE LIMITING (max 3 Anfragen pro Minute pro IP) ===
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            if ',' in client_ip:
                client_ip = client_ip.split(',')[0].strip()
            
            current_time = time.time()
            if client_ip in _inquiry_cache:
                last_request, count = _inquiry_cache[client_ip]
                if current_time - last_request < 60:
                    if count >= 3:
                        return JsonResponse({'status': 'error', 'message': 'Zu viele Anfragen. Bitte warten Sie eine Minute.'})
                    _inquiry_cache[client_ip] = (last_request, count + 1)
                else:
                    _inquiry_cache[client_ip] = (current_time, 1)
            else:
                _inquiry_cache[client_ip] = (current_time, 1)
            
            data = json.loads(request.body)
            
            # === INPUT VALIDIERUNG ===
            name = data.get('name', '').strip()[:100]
            phone = data.get('phone', '').strip()[:30]
            email = data.get('email', '').strip()[:100]
            message = data.get('message', '').strip()[:2000]
            listing_id = str(data.get('listing_id', '')).strip()[:20]
            listing_title = data.get('listing_title', '').strip()[:200]
            realtor_email = data.get('realtor_email', '').strip()
            
            # Pflichtfelder pruefen
            if not name or not email or not message:
                return JsonResponse({'status': 'error', 'message': 'Bitte fuellen Sie alle Pflichtfelder aus.'})
            
            # E-Mail Format pruefen
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                return JsonResponse({'status': 'error', 'message': 'Bitte geben Sie eine gueltige E-Mail-Adresse ein.'})
            
            if not realtor_email:
                return JsonResponse({'status': 'error', 'message': 'Makler E-Mail nicht gefunden'})
            
            # E-Mail an den Makler senden
            subject = f'Neue Anfrage zu Ihrer Immobilie: {listing_title}'
            email_body = f"""
Guten Tag,

Sie haben eine neue Anfrage zu Ihrer Immobilie erhalten:

=== IMMOBILIE ===
Titel: {listing_title}
ID: {listing_id}

=== INTERESSENT ===
Name: {name}
Telefon: {phone}
E-Mail: {email}

=== NACHRICHT ===
{message}

---
Diese E-Mail wurde automatisch von 123-Kroatien.eu gesendet.
            """
            
            send_mail(
                subject=subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[realtor_email],
                fail_silently=False,
            )
            
            return JsonResponse({'status': 'success', 'message': 'Anfrage erfolgreich gesendet!'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Nur POST erlaubt'})


# === ANFRAGE AN PROFESSIONAL (E-Mail Benachrichtigung) ===
@csrf_exempt
def send_professional_inquiry(request):
    """Sendet eine Anfrage an einen Professional"""
    if request.method == 'POST':
        try:
            # Rate Limiting
            client_ip = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
            if ',' in client_ip:
                client_ip = client_ip.split(',')[0].strip()
            
            current_time = time.time()
            cache_key = f"prof_{client_ip}"
            if cache_key in _inquiry_cache:
                last_request, count = _inquiry_cache[cache_key]
                if current_time - last_request < 60:
                    if count >= 3:
                        return JsonResponse({'status': 'error', 'message': 'Zu viele Anfragen. Bitte warten Sie eine Minute.'})
                    _inquiry_cache[cache_key] = (last_request, count + 1)
                else:
                    _inquiry_cache[cache_key] = (current_time, 1)
            else:
                _inquiry_cache[cache_key] = (current_time, 1)
            
            data = json.loads(request.body)
            
            name = data.get('name', '').strip()[:100]
            email = data.get('email', '').strip()[:100]
            phone = data.get('phone', '').strip()[:30]
            message = data.get('message', '').strip()[:2000]
            professional_email = data.get('professional_email', '').strip()
            
            if not name or not email or not message:
                return JsonResponse({'status': 'error', 'message': 'Bitte fuellen Sie alle Pflichtfelder aus.'})
            
            if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                return JsonResponse({'status': 'error', 'message': 'Bitte geben Sie eine gueltige E-Mail-Adresse ein.'})
            
            if not professional_email:
                return JsonResponse({'status': 'error', 'message': 'E-Mail-Adresse nicht gefunden'})
            
            subject = 'Neue Anfrage ueber 123-Kroatien.eu'
            email_body = f"""
Guten Tag,

Sie haben eine neue Anfrage erhalten:

=== INTERESSENT ===
Name: {name}
E-Mail: {email}
Telefon: {phone}

=== NACHRICHT ===
{message}

---
Diese E-Mail wurde automatisch von 123-Kroatien.eu gesendet.
            """
            
            send_mail(
                subject=subject,
                message=email_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[professional_email],
                fail_silently=False,
            )
            
            return JsonResponse({'status': 'success', 'message': 'Anfrage erfolgreich gesendet!'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Nur POST erlaubt'})


@login_required(login_url='account:login')
def makler_dashboard(request):
    """Redirect to the user's professional profile"""
    try:
        professional = Professional.objects.get(user=request.user)
        return redirect('main:agent', id=professional.id)
    except Professional.DoesNotExist:
        messages.error(request, "Kein Makler-Profil gefunden.")
        return redirect('main:home')
