from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from listings.models import Listing
from django.contrib import messages
from django.utils import translation
from django.http import HttpResponseRedirect
from accounts.models import Agent
from main.professional_models import Professional
from pages.models import Translation
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.core.mail import EmailMessage
import json
import os


def get_professional_or_agent(user):
    """
    Get Professional for user, fallback to Agent for backwards compatibility.
    Returns (professional, agent) tuple - one will be None.
    """
    try:
        professional = Professional.objects.get(user=user)
        return professional, None
    except Professional.DoesNotExist:
        pass
    
    try:
        agent = Agent.objects.get(user=user)
        return None, agent
    except Agent.DoesNotExist:
        pass
    
    return None, None

# Create your views here.

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
    # Get professional or agent for current user
    professional, agent = get_professional_or_agent(request.user)
    
    # Check if user can post properties
    if professional and not professional.can_post_properties():
        messages.error(request, "Sie haben keine Berechtigung, Objekte zu veröffentlichen.")
        return redirect('main:home')
    
    if not professional and not agent:
        messages.error(request, "Bitte vervollständigen Sie zuerst Ihr Profil.")
        return redirect('main:home')
    
    if request.method == 'POST':
        listing = Listing()
        
        # Use Professional data if available, otherwise fallback to Agent
        if professional:
            listing.company_name = professional.company_name
            listing.company_logo = professional.company_logo
            listing.portrait_photo = professional.portrait_photo
            listing.oib_number = professional.oib_number
            listing.email = professional.email
            listing.domain = professional.website
            listing.professional = professional
        else:
            listing.company_name = agent.company_name
            listing.company_logo = agent.company_logo
            listing.portrait_photo = agent.portrait_photo
            listing.oib_number = agent.oib_number
            listing.email = agent.user.email
            listing.domain = agent.domain
            listing.realtor = agent
        
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
    professional, agent = get_professional_or_agent(request.user)
    
    # Get listings for professional or agent
    if professional:
        listings = Listing.objects.filter(professional=professional)
    elif agent:
        listings = Listing.objects.filter(realtor=agent)
    else:
        listings = Listing.objects.none()
    
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
    
    context = {
        'listings': listings,
        'agent': agent,
        'professional': professional,
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

    # Support for old slider format (my_range) and new dropdown format (price_from/price_to)
    my_range = request.GET.get('my_range', None)
    if my_range:
        min_price, max_price = my_range.split(';')
        if min_price and max_price:
            listings = listings.filter(property_price__gte=int(min_price), property_price__lte=int(max_price))
    
    # New price dropdown filters
    price_from = request.GET.get('price_from', None)
    if price_from:
        listings = listings.filter(property_price__gte=int(price_from))
    
    price_to = request.GET.get('price_to', None)
    if price_to:
        listings = listings.filter(property_price__lte=int(price_to))


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
    user_language = request.session.get('site_language', 'en')
    listing = Listing.objects.get(id=id)
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
    # Prüfe ob ein 'next' Parameter übergeben wurde, sonst HTTP_REFERER, sonst Homepage
    next_url = request.GET.get('next')
    if next_url:
        return HttpResponseRedirect(next_url)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return HttpResponseRedirect(referer)
    return HttpResponseRedirect('/')


def agent(request, id):
    # Try to find Professional first, fallback to Agent
    professional = None
    agent = None
    
    try:
        professional = Professional.objects.get(id=id)
        listings = Listing.objects.filter(professional=professional)
    except (Professional.DoesNotExist, ValueError):
        try:
            agent = Agent.objects.get(id=id)
            listings = Listing.objects.filter(realtor=agent)
        except Agent.DoesNotExist:
            listings = Listing.objects.none()
    
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
    context = {
        'listings': listings,
        'agent': agent,
        'professional': professional,
    }
    return render(request, 'main/agent.html', context)


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
            # Handle multi-select languages
            languages_list = request.POST.getlist('languages')
            professional.languages = ', '.join(languages_list) if languages_list else professional.languages
            
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

    # Build public profile URL for Professional
    public_profile_url = None
    if professional:
        from main.professional_views import CATEGORY_URLS
        category_slug = CATEGORY_URLS.get(professional.professional_type, {}).get('ge', 'makler')
        public_profile_url = f"/ge/kroatien/{category_slug}/{professional.slug}/"
    
    context = {
        'agent': agent,
        'professional': professional,
        'regions': Professional.REGIONS,
        'public_profile_url': public_profile_url,
    }
    
    # Use extended template for Professional, legacy template for Agent
    if professional:
        return render(request, 'main/edit-agent-professional.html', context)
    return render(request, 'main/edit-agent.html', context)


# Reference Projects Management Views
from main.professional_models import ReferenceProject

@login_required(login_url='account:login')
def reference_projects_list(request, id):
    """List all reference projects for a professional"""
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        messages.error(request, "Profil nicht gefunden.")
        return redirect('main:home')
    
    # Security check: Only owner can manage
    if professional.user != request.user:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    projects = ReferenceProject.objects.filter(professional=professional)
    
    context = {
        'professional': professional,
        'projects': projects,
    }
    return render(request, 'main/reference_projects_list.html', context)


@login_required(login_url='account:login')
def reference_project_create(request, id):
    """Create a new reference project"""
    try:
        professional = Professional.objects.get(id=id)
    except Professional.DoesNotExist:
        messages.error(request, "Profil nicht gefunden.")
        return redirect('main:home')
    
    # Security check
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
        
        # Handle image uploads
        for i in range(1, 7):
            img_field = f'image_{i}'
            if request.FILES.get(img_field):
                setattr(project, img_field, request.FILES.get(img_field))
        
        project.save()
        messages.success(request, "Referenzprojekt erfolgreich erstellt!")
        return redirect('main:reference_projects_list', id=id)
    
    context = {
        'professional': professional,
        'is_edit': False,
    }
    return render(request, 'main/reference_project_form.html', context)


@login_required(login_url='account:login')
def reference_project_edit(request, id, project_id):
    """Edit an existing reference project"""
    try:
        professional = Professional.objects.get(id=id)
        project = ReferenceProject.objects.get(id=project_id, professional=professional)
    except (Professional.DoesNotExist, ReferenceProject.DoesNotExist):
        messages.error(request, "Projekt nicht gefunden.")
        return redirect('main:home')
    
    # Security check
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
        
        # Handle image uploads
        for i in range(1, 7):
            img_field = f'image_{i}'
            if request.FILES.get(img_field):
                setattr(project, img_field, request.FILES.get(img_field))
            # Handle image deletion
            if request.POST.get(f'delete_image_{i}'):
                setattr(project, img_field, None)
        
        project.save()
        messages.success(request, "Referenzprojekt erfolgreich aktualisiert!")
        return redirect('main:reference_projects_list', id=id)
    
    context = {
        'professional': professional,
        'project': project,
        'is_edit': True,
    }
    return render(request, 'main/reference_project_form.html', context)


@login_required(login_url='account:login')
def reference_project_delete(request, id, project_id):
    """Delete a reference project"""
    try:
        professional = Professional.objects.get(id=id)
        project = ReferenceProject.objects.get(id=project_id, professional=professional)
    except (Professional.DoesNotExist, ReferenceProject.DoesNotExist):
        messages.error(request, "Projekt nicht gefunden.")
        return redirect('main:home')
    
    # Security check
    if professional.user != request.user:
        messages.error(request, "Keine Berechtigung.")
        return redirect('main:home')
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, "Referenzprojekt erfolgreich gelöscht!")
    
    return redirect('main:reference_projects_list', id=id)


# Professional Registration View (Bilingual: German & Croatian)
def professional_registration(request, lang='ge'):
    """
    View for the bilingual professional registration form.
    Supports German (ge) and Croatian (hr).
    """
    from main.professional_forms import ProfessionalRegistrationForm, FORM_LABELS
    from django.core.mail import send_mail
    
    # Only DE and HR allowed
    if lang not in ["ge", "hr"]:
        lang = "ge"
    
    labels = FORM_LABELS.get(lang, FORM_LABELS["ge"])
    success = False
    
    if request.method == "POST":
        form = ProfessionalRegistrationForm(request.POST, request.FILES, lang=lang)
        if form.is_valid():
            professional = form.save()
            # Send email notification
            try:
                email_body = f"Neue Professional-Registrierung:\n\nName: {professional.name}\nTyp: {professional.get_professional_type_display()}\nE-Mail: {professional.email}\nTelefon: {professional.phone}\nStadt: {professional.city}\nRegion: {professional.get_region_display() if professional.region else '-'}"
                send_mail(
                    "Neue Professional-Registrierung",
                    email_body,
                    "service.mahamudh472@gmail.com",
                    ["ja@brandoz.de"],
                    fail_silently=True
                )
            except Exception as e:
                print(f"E-Mail Fehler: {e}")
            success = True
    else:
        form = ProfessionalRegistrationForm(lang=lang)
    
    context = {
        'form': form,
        'labels': labels,
        'lang': lang,
        'success': success,
    }
    return render(request, 'main/professional_registration.html', context)

@login_required(login_url='account:login')
def makler_dashboard(request):
    """Redirect to the user's professional profile"""
    try:
        professional = Professional.objects.get(user=request.user)
        return redirect('main:agent', id=professional.id)
    except Professional.DoesNotExist:
        messages.error(request, "Kein Makler-Profil gefunden.")
        return redirect('main:home')
