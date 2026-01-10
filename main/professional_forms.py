from django import forms
from django.utils.text import slugify
from main.professional_models import Professional, REGIONS, PROFESSIONAL_TYPES
import uuid

FORM_LABELS = {
    "ge": {
        "professional_type": "Art des Professionals",
        "name": "Name",
        "email": "E-Mail",
        "phone": "Telefon",
        "city": "Stadt",
        "region": "Region",
        "service_regions": "Serviceregionen",
        "languages_spoken": "Gesprochene Sprachen",
        "company_name": "Firmenname",
        "website": "Webseite",
        "registration_number": "Registrierungsnummer",
        "oib_number": "OIB Nummer",
        "submit": "Registrieren",
        "success": "Vielen Dank! Ihre Registrierung wurde erfolgreich gesendet."
    },
    "hr": {
        "professional_type": "Vrsta profesionalca",
        "name": "Ime",
        "email": "E-mail",
        "phone": "Telefon",
        "city": "Grad",
        "region": "Regija",
        "service_regions": "Podrucja usluga",
        "languages_spoken": "Jezici",
        "company_name": "Naziv tvrtke",
        "website": "Web stranica",
        "registration_number": "Registracijski broj",
        "oib_number": "OIB broj",
        "submit": "Registriraj",
        "success": "Hvala! Vasa registracija je uspjesno poslana."
    },
    "en": {
        "professional_type": "Professional Type",
        "name": "Name",
        "email": "Email",
        "phone": "Phone",
        "city": "City",
        "region": "Region",
        "service_regions": "Service Regions",
        "languages_spoken": "Languages Spoken",
        "company_name": "Company Name",
        "website": "Website",
        "registration_number": "Registration Number",
        "oib_number": "OIB Number",
        "submit": "Register",
        "success": "Thank you! Your registration has been sent successfully."
    }
}

PROFESSIONAL_TYPES_TRANSLATED = {
    "ge": [("real_estate_agent", "Immobilienmakler"), ("construction_company", "Bauunternehmen"), ("lawyer", "Rechtsanwalt"), ("tax_advisor", "Steuerberater"), ("architect", "Architekt")],
    "hr": [("real_estate_agent", "Agencija za nekretnine"), ("construction_company", "Gradevinska tvrtka"), ("lawyer", "Odvjetnik"), ("tax_advisor", "Porezni savjetnik"), ("architect", "Arhitekt")],
    "en": [("real_estate_agent", "Real Estate Agent"), ("construction_company", "Construction Company"), ("lawyer", "Lawyer"), ("tax_advisor", "Tax Advisor"), ("architect", "Architect")]
}

REGIONS_TRANSLATED = {
    "ge": REGIONS,
    "hr": [("istrien", "Istra"), ("kvarner", "Kvarner"), ("dalmatien-nord", "Sjeverna Dalmacija"), ("dalmatien-mitte", "Srednja Dalmacija"), ("dalmatien-sued", "Juzna Dalmacija"), ("zagreb", "Zagreb"), ("slavonien", "Slavonija"), ("lika-gorski-kotar", "Lika i Gorski Kotar")],
    "en": REGIONS
}

class ProfessionalRegistrationForm(forms.Form):
    professional_type = forms.ChoiceField(choices=PROFESSIONAL_TYPES)
    name = forms.CharField(max_length=200)
    email = forms.EmailField()
    phone = forms.CharField(max_length=50, required=False)
    city = forms.CharField(max_length=100)
    region = forms.ChoiceField(choices=REGIONS)
    service_regions = forms.CharField(max_length=500, required=False)
    languages_spoken = forms.CharField(max_length=200)
    company_name = forms.CharField(max_length=200, required=False)
    website = forms.URLField(required=False)
    registration_number = forms.CharField(max_length=100, required=False)
    oib_number = forms.CharField(max_length=20, required=False)
    
    def __init__(self, *args, lang="ge", **kwargs):
        super().__init__(*args, **kwargs)
        self.lang = lang
        labels = FORM_LABELS.get(lang, FORM_LABELS["ge"])
        self.fields["professional_type"].choices = PROFESSIONAL_TYPES_TRANSLATED.get(lang, PROFESSIONAL_TYPES_TRANSLATED["ge"])
        self.fields["region"].choices = REGIONS_TRANSLATED.get(lang, REGIONS_TRANSLATED["ge"])
        for field_name, field in self.fields.items():
            if field_name in labels:
                field.label = labels[field_name]
    
    def save(self):
        d = self.cleaned_data
        slug = slugify(d["name"] + "-" + d["city"] + "-" + str(uuid.uuid4())[:8])
        return Professional.objects.create(
            professional_type=d["professional_type"], name=d["name"], slug=slug,
            email=d["email"], phone=d.get("phone",""), city=d["city"],
            region=d["region"], languages_spoken=d["languages_spoken"],
            company_name=d.get("company_name",""), website=d.get("website",""),
            is_active=False, is_verified=False
        )
