import json
from django.shortcuts import render, get_object_or_404
from django.http import Http404
from django.core.mail import send_mail
from main.professional_models import Professional, ProfessionalContent

# Übersetzungen für Regionen
REGION_TRANSLATIONS = {
    "ge": {"istrien": "Istrien", "kvarner": "Kvarner", "dalmatien-nord": "Nord-Dalmatien", "dalmatien-mitte": "Mittel-Dalmatien", "dalmatien-sued": "Süd-Dalmatien", "zagreb": "Zagreb", "slavonien": "Slawonien", "lika-gorski-kotar": "Lika & Gorski Kotar"},
    "en": {"istrien": "Istria", "kvarner": "Kvarner", "dalmatien-nord": "North Dalmatia", "dalmatien-mitte": "Central Dalmatia", "dalmatien-sued": "South Dalmatia", "zagreb": "Zagreb", "slavonien": "Slavonia", "lika-gorski-kotar": "Lika & Gorski Kotar"},
    "hr": {"istrien": "Istra", "kvarner": "Kvarner", "dalmatien-nord": "Sjeverna Dalmacija", "dalmatien-mitte": "Srednja Dalmacija", "dalmatien-sued": "Južna Dalmacija", "zagreb": "Zagreb", "slavonien": "Slavonija", "lika-gorski-kotar": "Lika i Gorski Kotar"},
    "fr": {"istrien": "Istrie", "kvarner": "Kvarner", "dalmatien-nord": "Dalmatie du Nord", "dalmatien-mitte": "Dalmatie centrale", "dalmatien-sued": "Dalmatie du Sud", "zagreb": "Zagreb", "slavonien": "Slavonie", "lika-gorski-kotar": "Lika et Gorski Kotar"},
    "nl": {"istrien": "Istrië", "kvarner": "Kvarner", "dalmatien-nord": "Noord-Dalmatië", "dalmatien-mitte": "Midden-Dalmatië", "dalmatien-sued": "Zuid-Dalmatië", "zagreb": "Zagreb", "slavonien": "Slavonië", "lika-gorski-kotar": "Lika & Gorski Kotar"},
    "pl": {"istrien": "Istria", "kvarner": "Kvarner", "dalmatien-nord": "Północna Dalmacja", "dalmatien-mitte": "Środkowa Dalmacja", "dalmatien-sued": "Południowa Dalmacja", "zagreb": "Zagrzeb", "slavonien": "Slawonia", "lika-gorski-kotar": "Lika i Gorski Kotar"},
    "cz": {"istrien": "Istrie", "kvarner": "Kvarner", "dalmatien-nord": "Severní Dalmácie", "dalmatien-mitte": "Střední Dalmácie", "dalmatien-sued": "Jižní Dalmácie", "zagreb": "Záhřeb", "slavonien": "Slavonie", "lika-gorski-kotar": "Lika a Gorski Kotar"},
    "sk": {"istrien": "Istria", "kvarner": "Kvarner", "dalmatien-nord": "Severná Dalmácia", "dalmatien-mitte": "Stredná Dalmácia", "dalmatien-sued": "Južná Dalmácia", "zagreb": "Záhreb", "slavonien": "Slavónia", "lika-gorski-kotar": "Lika a Gorski Kotar"},
    "ru": {"istrien": "Истрия", "kvarner": "Кварнер", "dalmatien-nord": "Северная Далмация", "dalmatien-mitte": "Центральная Далмация", "dalmatien-sued": "Южная Далмация", "zagreb": "Загреб", "slavonien": "Славония", "lika-gorski-kotar": "Лика и Горски Котар"},
    "gr": {"istrien": "Ίστρια", "kvarner": "Κβάρνερ", "dalmatien-nord": "Βόρεια Δαλματία", "dalmatien-mitte": "Κεντρική Δαλματία", "dalmatien-sued": "Νότια Δαλματία", "zagreb": "Ζάγκρεμπ", "slavonien": "Σλαβονία", "lika-gorski-kotar": "Λίκα & Γκόρσκι Κοτάρ"},
    "sw": {"istrien": "Istrien", "kvarner": "Kvarner", "dalmatien-nord": "Norra Dalmatien", "dalmatien-mitte": "Mellersta Dalmatien", "dalmatien-sued": "Södra Dalmatien", "zagreb": "Zagreb", "slavonien": "Slavonien", "lika-gorski-kotar": "Lika & Gorski Kotar"},
    "no": {"istrien": "Istria", "kvarner": "Kvarner", "dalmatien-nord": "Nord-Dalmatia", "dalmatien-mitte": "Midt-Dalmatia", "dalmatien-sued": "Sør-Dalmatia", "zagreb": "Zagreb", "slavonien": "Slavonia", "lika-gorski-kotar": "Lika & Gorski Kotar"},
}

# Übersetzungen für Sprachen
LANGUAGE_TRANSLATIONS = {
    "ge": {"de": "Deutsch", "en": "Englisch", "hr": "Kroatisch", "it": "Italienisch", "fr": "Französisch", "sl": "Slowenisch", "hu": "Ungarisch"},
    "en": {"de": "German", "en": "English", "hr": "Croatian", "it": "Italian", "fr": "French", "sl": "Slovenian", "hu": "Hungarian"},
    "hr": {"de": "Njemački", "en": "Engleski", "hr": "Hrvatski", "it": "Talijanski", "fr": "Francuski", "sl": "Slovenski", "hu": "Mađarski"},
    "fr": {"de": "Allemand", "en": "Anglais", "hr": "Croate", "it": "Italien", "fr": "Français", "sl": "Slovène", "hu": "Hongrois"},
    "nl": {"de": "Duits", "en": "Engels", "hr": "Kroatisch", "it": "Italiaans", "fr": "Frans", "sl": "Sloveens", "hu": "Hongaars"},
    "pl": {"de": "Niemiecki", "en": "Angielski", "hr": "Chorwacki", "it": "Włoski", "fr": "Francuski", "sl": "Słoweński", "hu": "Węgierski"},
    "cz": {"de": "Němčina", "en": "Angličtina", "hr": "Chorvatština", "it": "Italština", "fr": "Francouzština", "sl": "Slovinština", "hu": "Maďarština"},
    "sk": {"de": "Nemčina", "en": "Angličtina", "hr": "Chorvátčina", "it": "Taliančina", "fr": "Francúzština", "sl": "Slovinčina", "hu": "Maďarčina"},
    "ru": {"de": "Немецкий", "en": "Английский", "hr": "Хорватский", "it": "Итальянский", "fr": "Французский", "sl": "Словенский", "hu": "Венгерский"},
    "gr": {"de": "Γερμανικά", "en": "Αγγλικά", "hr": "Κροατικά", "it": "Ιταλικά", "fr": "Γαλλικά", "sl": "Σλοβενικά", "hu": "Ουγγρικά"},
    "sw": {"de": "Tyska", "en": "Engelska", "hr": "Kroatiska", "it": "Italienska", "fr": "Franska", "sl": "Slovenska", "hu": "Ungerska"},
    "no": {"de": "Tysk", "en": "Engelsk", "hr": "Kroatisk", "it": "Italiensk", "fr": "Fransk", "sl": "Slovensk", "hu": "Ungarsk"},
}

# Hilfsfunktionen

# Monatsübersetzungen
MONTH_TRANSLATIONS = {
    "ge": "Januar", "en": "January", "hr": "Siječanj", "fr": "Janvier",
    "nl": "Januari", "pl": "Styczeń", "cz": "Leden", "sk": "Január",
    "ru": "Январь", "gr": "Ιανουάριος", "sw": "Januari", "no": "Januar",
}

def translate_region(region_key, lang):
    """Übersetzt einen Region-Schlüssel oder deutschen Namen in die gewählte Sprache"""
    # Mapping von deutschen Namen zu Schlüsseln
    de_to_key = {
        "Istrien": "istrien", "Kvarner": "kvarner", 
        "Nord-Dalmatien": "dalmatien-nord", "Mittel-Dalmatien": "dalmatien-mitte",
        "Sued-Dalmatien": "dalmatien-sued", "Süd-Dalmatien": "dalmatien-sued",
        "Zagreb": "zagreb", "Slavonien": "slavonien", "Slawonien": "slavonien",
        "Lika & Gorski Kotar": "lika-gorski-kotar",
        "ganz Kroatien": "ganz-kroatien",
    }
    
    # Konvertiere deutschen Namen zu Schlüssel falls nötig
    key = de_to_key.get(region_key, region_key.lower() if region_key else region_key)
    
    # Spezialfall: "ganz Kroatien"
    ganz_kroatien = {
        "ge": "ganz Kroatien", "en": "all of Croatia", "hr": "cijela Hrvatska",
        "fr": "toute la Croatie", "nl": "heel Kroatië", "pl": "cała Chorwacja",
        "cz": "celé Chorvatsko", "sk": "celé Chorvátsko", "ru": "вся Хорватия",
        "gr": "όλη η Κροατία", "sw": "hela Kroatien", "no": "hele Kroatia",
    }
    if key == "ganz-kroatien" or region_key == "ganz Kroatien":
        return ganz_kroatien.get(lang, "ganz Kroatien")
    
    regions = REGION_TRANSLATIONS.get(lang, REGION_TRANSLATIONS["ge"])
    return regions.get(key, region_key)

def translate_languages(languages_str, lang):
    """Übersetzt eine kommagetrennte Sprachliste"""
    if not languages_str:
        return ""
    lang_trans = LANGUAGE_TRANSLATIONS.get(lang, LANGUAGE_TRANSLATIONS["ge"])
    # Versuche die gespeicherten Sprachen zu übersetzen
    parts = [p.strip() for p in languages_str.split(",")]
    translated = []
    # Mapping von deutschen Namen zu Codes
    de_to_code = {"Deutsch": "de", "Englisch": "en", "Kroatisch": "hr", "Italienisch": "it", "Französisch": "fr", "Slowenisch": "sl", "Ungarisch": "hu"}
    for p in parts:
        code = de_to_code.get(p, p.lower()[:2])
        translated.append(lang_trans.get(code, p))
    return ", ".join(translated)


# Länder-Namen in allen Sprachen
COUNTRY_NAMES = {
    "ge": "kroatien", "en": "croatia", "hr": "hrvatska", "fr": "croatie",
    "nl": "kroatie", "pl": "chorwacja", "cz": "chorvatsko", "sk": "chorvatsko",
    "ru": "horvatiya", "gr": "kroatia", "sw": "kroatien", "no": "kroatia",
}

COUNTRY_TO_LANG = {
    "kroatien": "ge", "croatia": "en", "hrvatska": "hr", "croatie": "fr",
    "kroatie": "nl", "chorwacja": "pl", "chorvatsko": "cz", "horvatiya": "ru",
    "kroatia": "gr",
}

# URL-Pfade für alle Kategorien in 12 Sprachen
CATEGORY_URLS = {
    "real_estate_agent": {
        "ge": "immobilienmakler", "en": "real-estate-agents", "hr": "agencije-za-nekretnine",
        "fr": "agents-immobiliers", "nl": "makelaars", "pl": "agenci-nieruchomosci",
        "cz": "realitni-makleri", "sk": "realitni-makleri", "ru": "agenty-nedvizhimosti",
        "gr": "mesites-akiniton", "sw": "fastighetsmaklare", "no": "eiendomsmeglere",
    },
    "construction_company": {
        "ge": "bauunternehmen", "en": "construction-companies", "hr": "gradevinske-tvrtke",
        "fr": "entreprises-construction", "nl": "bouwbedrijven", "pl": "firmy-budowlane",
        "cz": "stavebni-firmy", "sk": "stavebne-firmy", "ru": "stroitelnye-kompanii",
        "gr": "kataskevestikes-etaireies", "sw": "byggforetag", "no": "byggefirmaer",
    },
    "lawyer": {
        "ge": "rechtsanwaelte", "en": "lawyers", "hr": "odvjetnici",
        "fr": "avocats", "nl": "advocaten", "pl": "prawnicy",
        "cz": "pravnici", "sk": "pravnici", "ru": "advokaty",
        "gr": "dikigoroi", "sw": "advokater", "no": "advokater",
    },
    "tax_advisor": {
        "ge": "steuerberater", "en": "tax-advisors", "hr": "porezni-savjetnici",
        "fr": "conseillers-fiscaux", "nl": "belastingadviseurs", "pl": "doradcy-podatkowi",
        "cz": "danovi-poradci", "sk": "danovi-poradcovia", "ru": "nalogovye-konsultanty",
        "gr": "forologikoi-symvouloi", "sw": "skatteradgivare", "no": "skatteradgivere",
    },
    "architect": {
        "ge": "architekten", "en": "architects", "hr": "arhitekti",
        "fr": "architectes", "nl": "architecten", "pl": "architekci",
        "cz": "architekti", "sk": "architekti", "ru": "arhitektory",
        "gr": "architektons", "sw": "arkitekter", "no": "arkitekter",
    },
}

# Übersetzungen für UI-Texte
TRANSLATIONS = {
    "ge": {
        "real_estate_agent": {"title": "Immobilienmakler in Kroatien", "singular": "Immobilienmakler", "subtitle": "Finden Sie qualifizierte Immobilienmakler für Ihren Immobilienkauf in Kroatien"},
        "construction_company": {"title": "Bauunternehmen in Kroatien", "singular": "Bauunternehmen", "subtitle": "Finden Sie qualifizierte Bauunternehmen für Ihr Bauprojekt in Kroatien"},
        "lawyer": {"title": "Rechtsanwälte in Kroatien", "singular": "Rechtsanwalt", "subtitle": "Finden Sie qualifizierte Rechtsanwälte für Immobilienrecht in Kroatien"},
        "tax_advisor": {"title": "Steuerberater in Kroatien", "singular": "Steuerberater", "subtitle": "Finden Sie qualifizierte Steuerberater für Immobiliensteuern in Kroatien"},
        "architect": {"title": "Architekten in Kroatien", "singular": "Architekt", "subtitle": "Finden Sie qualifizierte Architekten für Ihr Bauprojekt in Kroatien"},
        "view_profile": "Profil ansehen",
        "back_to_list": "Zurück zur Liste",
        "contact": "Kontakt",
        "languages": "Sprachen",
        "regions": "Regionen",
        "verified": "Verifiziert",
        "no_entries": "Keine Einträge gefunden.",
        "disclaimer": "Dieser Inhalt dient nur der allgemeinen Information und stellt keine professionelle Beratung dar.",
        "last_updated": "Zuletzt aktualisiert",
        "profile": "Profil",
        "company": "Unternehmen",
        "areas_of_activity": "Tätigkeitsbereiche",
        "working_approach": "Arbeitsweise",
        "faq": "Häufige Fragen",
        "registration": "Registrierung",
    },
    "en": {
        "real_estate_agent": {"title": "Real Estate Agents in Croatia", "singular": "Real Estate Agent", "subtitle": "Find qualified real estate agents for your property purchase in Croatia"},
        "construction_company": {"title": "Construction Companies in Croatia", "singular": "Construction Company", "subtitle": "Find qualified construction companies for your building project in Croatia"},
        "lawyer": {"title": "Lawyers in Croatia", "singular": "Lawyer", "subtitle": "Find qualified lawyers for real estate law in Croatia"},
        "tax_advisor": {"title": "Tax Advisors in Croatia", "singular": "Tax Advisor", "subtitle": "Find qualified tax advisors for property taxes in Croatia"},
        "architect": {"title": "Architects in Croatia", "singular": "Architect", "subtitle": "Find qualified architects for your building project in Croatia"},
        "view_profile": "View Profile",
        "back_to_list": "Back to List",
        "contact": "Contact",
        "languages": "Languages",
        "regions": "Regions",
        "verified": "Verified",
        "no_entries": "No entries found.",
        "disclaimer": "This content is for general information only and does not constitute professional advice.",
        "last_updated": "Last updated",
        "profile": "Profile",
        "company": "Company",
        "areas_of_activity": "Areas of Activity",
        "working_approach": "Working Approach",
        "faq": "Frequently Asked Questions",
        "registration": "Registration",
    },
    "hr": {
        "real_estate_agent": {"title": "Agencije za nekretnine u Hrvatskoj", "singular": "Agencija za nekretnine", "subtitle": "Pronađite kvalificirane agencije za nekretnine za kupnju nekretnina u Hrvatskoj"},
        "construction_company": {"title": "Građevinske tvrtke u Hrvatskoj", "singular": "Građevinska tvrtka", "subtitle": "Pronađite kvalificirane građevinske tvrtke za vaš projekt u Hrvatskoj"},
        "lawyer": {"title": "Odvjetnici u Hrvatskoj", "singular": "Odvjetnik", "subtitle": "Pronađite kvalificirane odvjetnike za pravo nekretnina u Hrvatskoj"},
        "tax_advisor": {"title": "Porezni savjetnici u Hrvatskoj", "singular": "Porezni savjetnik", "subtitle": "Pronađite kvalificirane porezne savjetnike za porez na nekretnine u Hrvatskoj"},
        "architect": {"title": "Arhitekti u Hrvatskoj", "singular": "Arhitekt", "subtitle": "Pronađite kvalificirane arhitekte za vaš projekt u Hrvatskoj"},
        "view_profile": "Pogledaj profil",
        "back_to_list": "Natrag na popis",
        "contact": "Kontakt",
        "languages": "Jezici",
        "regions": "Regije",
        "verified": "Verificirano",
        "no_entries": "Nema unosa.",
        "disclaimer": "Ovaj sadržaj služi samo za opće informacije i ne predstavlja profesionalni savjet.",
        "last_updated": "Zadnje ažurirano",
        "profile": "Profil",
        "company": "Tvrtka",
        "areas_of_activity": "Područja djelovanja",
        "working_approach": "Način rada",
        "faq": "Česta pitanja",
        "registration": "Registracija",
    },
    "fr": {
        "real_estate_agent": {"title": "Agents immobiliers en Croatie", "singular": "Agent immobilier", "subtitle": "Trouvez des agents immobiliers qualifiés pour votre achat immobilier en Croatie"},
        "construction_company": {"title": "Entreprises de construction en Croatie", "singular": "Entreprise de construction", "subtitle": "Trouvez des entreprises de construction qualifiées pour votre projet en Croatie"},
        "lawyer": {"title": "Avocats en Croatie", "singular": "Avocat", "subtitle": "Trouvez des avocats qualifiés en droit immobilier en Croatie"},
        "tax_advisor": {"title": "Conseillers fiscaux en Croatie", "singular": "Conseiller fiscal", "subtitle": "Trouvez des conseillers fiscaux qualifiés pour les impôts immobiliers en Croatie"},
        "architect": {"title": "Architectes en Croatie", "singular": "Architecte", "subtitle": "Trouvez des architectes qualifiés pour votre projet en Croatie"},
        "view_profile": "Voir le profil",
        "back_to_list": "Retour à la liste",
        "contact": "Contact",
        "languages": "Langues",
        "regions": "Régions",
        "verified": "Vérifié",
        "no_entries": "Aucune entrée trouvée.",
        "disclaimer": "Ce contenu est fourni à titre informatif uniquement et ne constitue pas un conseil professionnel.",
        "last_updated": "Dernière mise à jour",
        "profile": "Profil",
        "company": "Entreprise",
        "areas_of_activity": "Domaines d'activité",
        "working_approach": "Méthode de travail",
        "faq": "Questions fréquentes",
        "registration": "Enregistrement",
    },
    "nl": {
        "real_estate_agent": {"title": "Makelaars in Kroatië", "singular": "Makelaar", "subtitle": "Vind gekwalificeerde makelaars voor uw vastgoedaankoop in Kroatië"},
        "construction_company": {"title": "Bouwbedrijven in Kroatië", "singular": "Bouwbedrijf", "subtitle": "Vind gekwalificeerde bouwbedrijven voor uw project in Kroatië"},
        "lawyer": {"title": "Advocaten in Kroatië", "singular": "Advocaat", "subtitle": "Vind gekwalificeerde advocaten voor vastgoedrecht in Kroatië"},
        "tax_advisor": {"title": "Belastingadviseurs in Kroatië", "singular": "Belastingadviseur", "subtitle": "Vind gekwalificeerde belastingadviseurs voor vastgoedbelasting in Kroatië"},
        "architect": {"title": "Architecten in Kroatië", "singular": "Architect", "subtitle": "Vind gekwalificeerde architecten voor uw project in Kroatië"},
        "view_profile": "Bekijk profiel",
        "back_to_list": "Terug naar lijst",
        "contact": "Contact",
        "languages": "Talen",
        "regions": "Regio's",
        "verified": "Geverifieerd",
        "no_entries": "Geen resultaten gevonden.",
        "disclaimer": "Deze inhoud is alleen voor algemene informatie en vormt geen professioneel advies.",
        "last_updated": "Laatst bijgewerkt",
        "profile": "Profiel",
        "company": "Bedrijf",
        "areas_of_activity": "Werkgebieden",
        "working_approach": "Werkwijze",
        "faq": "Veelgestelde vragen",
        "registration": "Registratie",
    },
    "pl": {
        "real_estate_agent": {"title": "Agenci nieruchomości w Chorwacji", "singular": "Agent nieruchomości", "subtitle": "Znajdź wykwalifikowanych agentów nieruchomości w Chorwacji"},
        "construction_company": {"title": "Firmy budowlane w Chorwacji", "singular": "Firma budowlana", "subtitle": "Znajdź wykwalifikowane firmy budowlane w Chorwacji"},
        "lawyer": {"title": "Prawnicy w Chorwacji", "singular": "Prawnik", "subtitle": "Znajdź wykwalifikowanych prawników w Chorwacji"},
        "tax_advisor": {"title": "Doradcy podatkowi w Chorwacji", "singular": "Doradca podatkowy", "subtitle": "Znajdź wykwalifikowanych doradców podatkowych w Chorwacji"},
        "architect": {"title": "Architekci w Chorwacji", "singular": "Architekt", "subtitle": "Znajdź wykwalifikowanych architektów w Chorwacji"},
        "view_profile": "Zobacz profil",
        "back_to_list": "Powrót do listy",
        "contact": "Kontakt",
        "languages": "Języki",
        "regions": "Regiony",
        "verified": "Zweryfikowany",
        "no_entries": "Nie znaleziono wpisów.",
        "disclaimer": "Ta treść służy wyłącznie celom informacyjnym i nie stanowi profesjonalnej porady.",
        "last_updated": "Ostatnia aktualizacja",
        "profile": "Profil",
        "company": "Firma",
        "areas_of_activity": "Obszary działalności",
        "working_approach": "Sposób pracy",
        "faq": "Często zadawane pytania",
        "registration": "Rejestracja",
    },
    "cz": {
        "real_estate_agent": {"title": "Realitní makléři v Chorvatsku", "singular": "Realitní makléř", "subtitle": "Najděte kvalifikované realitní makléře v Chorvatsku"},
        "construction_company": {"title": "Stavební firmy v Chorvatsku", "singular": "Stavební firma", "subtitle": "Najděte kvalifikované stavební firmy v Chorvatsku"},
        "lawyer": {"title": "Právníci v Chorvatsku", "singular": "Právník", "subtitle": "Najděte kvalifikované právníky v Chorvatsku"},
        "tax_advisor": {"title": "Daňoví poradci v Chorvatsku", "singular": "Daňový poradce", "subtitle": "Najděte kvalifikované daňové poradce v Chorvatsku"},
        "architect": {"title": "Architekti v Chorvatsku", "singular": "Architekt", "subtitle": "Najděte kvalifikované architekty v Chorvatsku"},
        "view_profile": "Zobrazit profil",
        "back_to_list": "Zpět na seznam",
        "contact": "Kontakt",
        "languages": "Jazyky",
        "regions": "Regiony",
        "verified": "Ověřeno",
        "no_entries": "Žádné záznamy nenalezeny.",
        "disclaimer": "Tento obsah slouží pouze pro obecné informace a nepředstavuje odbornou radu.",
        "last_updated": "Poslední aktualizace",
        "profile": "Profil",
        "company": "Společnost",
        "areas_of_activity": "Oblasti činnosti",
        "working_approach": "Způsob práce",
        "faq": "Často kladené otázky",
        "registration": "Registrace",
    },
    "ru": {
        "real_estate_agent": {"title": "Агенты по недвижимости в Хорватии", "singular": "Агент по недвижимости", "subtitle": "Найдите квалифицированных агентов по недвижимости в Хорватии"},
        "construction_company": {"title": "Строительные компании в Хорватии", "singular": "Строительная компания", "subtitle": "Найдите квалифицированные строительные компании в Хорватии"},
        "lawyer": {"title": "Адвокаты в Хорватии", "singular": "Адвокат", "subtitle": "Найдите квалифицированных адвокатов в Хорватии"},
        "tax_advisor": {"title": "Налоговые консультанты в Хорватии", "singular": "Налоговый консультант", "subtitle": "Найдите квалифицированных налоговых консультантов в Хорватии"},
        "architect": {"title": "Архитекторы в Хорватии", "singular": "Архитектор", "subtitle": "Найдите квалифицированных архитекторов в Хорватии"},
        "view_profile": "Просмотр профиля",
        "back_to_list": "Назад к списку",
        "contact": "Контакт",
        "languages": "Языки",
        "regions": "Регионы",
        "verified": "Проверено",
        "no_entries": "Записи не найдены.",
        "disclaimer": "Этот контент предназначен только для общей информации и не является профессиональной консультацией.",
        "last_updated": "Последнее обновление",
        "profile": "Профиль",
        "company": "Компания",
        "areas_of_activity": "Области деятельности",
        "working_approach": "Подход к работе",
        "faq": "Часто задаваемые вопросы",
        "registration": "Регистрация",
    },
    "gr": {
        "real_estate_agent": {"title": "Μεσίτες ακινήτων στην Κροατία", "singular": "Μεσίτης ακινήτων", "subtitle": "Βρείτε καταρτισμένους μεσίτες ακινήτων στην Κροατία"},
        "construction_company": {"title": "Κατασκευαστικές εταιρείες στην Κροατία", "singular": "Κατασκευαστική εταιρεία", "subtitle": "Βρείτε καταρτισμένες κατασκευαστικές εταιρείες στην Κροατία"},
        "lawyer": {"title": "Δικηγόροι στην Κροατία", "singular": "Δικηγόρος", "subtitle": "Βρείτε καταρτισμένους δικηγόρους στην Κροατία"},
        "tax_advisor": {"title": "Φορολογικοί σύμβουλοι στην Κροατία", "singular": "Φορολογικός σύμβουλος", "subtitle": "Βρείτε καταρτισμένους φορολογικούς συμβούλους στην Κροατία"},
        "architect": {"title": "Αρχιτέκτονες στην Κροατία", "singular": "Αρχιτέκτονας", "subtitle": "Βρείτε καταρτισμένους αρχιτέκτονες στην Κροατία"},
        "view_profile": "Προβολή προφίλ",
        "back_to_list": "Επιστροφή στη λίστα",
        "contact": "Επικοινωνία",
        "languages": "Γλώσσες",
        "regions": "Περιοχές",
        "verified": "Επαληθευμένο",
        "no_entries": "Δεν βρέθηκαν καταχωρήσεις.",
        "disclaimer": "Αυτό το περιεχόμενο είναι μόνο για γενική ενημέρωση και δεν αποτελεί επαγγελματική συμβουλή.",
        "last_updated": "Τελευταία ενημέρωση",
        "profile": "Προφίλ",
        "company": "Εταιρεία",
        "areas_of_activity": "Τομείς δραστηριότητας",
        "working_approach": "Τρόπος εργασίας",
        "faq": "Συχνές ερωτήσεις",
        "registration": "Εγγραφή",
    },
    "sw": {
        "real_estate_agent": {"title": "Fastighetsmäklare i Kroatien", "singular": "Fastighetsmäklare", "subtitle": "Hitta kvalificerade fastighetsmäklare i Kroatien"},
        "construction_company": {"title": "Byggföretag i Kroatien", "singular": "Byggföretag", "subtitle": "Hitta kvalificerade byggföretag i Kroatien"},
        "lawyer": {"title": "Advokater i Kroatien", "singular": "Advokat", "subtitle": "Hitta kvalificerade advokater i Kroatien"},
        "tax_advisor": {"title": "Skatterådgivare i Kroatien", "singular": "Skatterådgivare", "subtitle": "Hitta kvalificerade skatterådgivare i Kroatien"},
        "architect": {"title": "Arkitekter i Kroatien", "singular": "Arkitekt", "subtitle": "Hitta kvalificerade arkitekter i Kroatien"},
        "view_profile": "Visa profil",
        "back_to_list": "Tillbaka till listan",
        "contact": "Kontakt",
        "languages": "Språk",
        "regions": "Regioner",
        "verified": "Verifierad",
        "no_entries": "Inga poster hittades.",
        "disclaimer": "Detta innehåll är endast för allmän information och utgör inte professionell rådgivning.",
        "last_updated": "Senast uppdaterad",
        "profile": "Profil",
        "company": "Företag",
        "areas_of_activity": "Verksamhetsområden",
        "working_approach": "Arbetssätt",
        "faq": "Vanliga frågor",
        "registration": "Registrering",
    },
    "no": {
        "real_estate_agent": {"title": "Eiendomsmeglere i Kroatia", "singular": "Eiendomsmegler", "subtitle": "Finn kvalifiserte eiendomsmeglere i Kroatia"},
        "construction_company": {"title": "Byggefirmaer i Kroatia", "singular": "Byggefirma", "subtitle": "Finn kvalifiserte byggefirmaer i Kroatia"},
        "lawyer": {"title": "Advokater i Kroatia", "singular": "Advokat", "subtitle": "Finn kvalifiserte advokater i Kroatia"},
        "tax_advisor": {"title": "Skatterådgivere i Kroatia", "singular": "Skatterådgiver", "subtitle": "Finn kvalifiserte skatterådgivere i Kroatia"},
        "architect": {"title": "Arkitekter i Kroatia", "singular": "Arkitekt", "subtitle": "Finn kvalifiserte arkitekter i Kroatia"},
        "view_profile": "Vis profil",
        "back_to_list": "Tilbake til listen",
        "contact": "Kontakt",
        "languages": "Språk",
        "regions": "Regioner",
        "verified": "Verifisert",
        "no_entries": "Ingen oppføringer funnet.",
        "disclaimer": "Dette innholdet er kun for generell informasjon og utgjør ikke profesjonell rådgivning.",
        "last_updated": "Sist oppdatert",
        "profile": "Profil",
        "company": "Selskap",
        "areas_of_activity": "Virksomhetsområder",
        "working_approach": "Arbeidsmetode",
        "faq": "Ofte stilte spørsmål",
        "registration": "Registrering",
    },
    "sk": {
        "real_estate_agent": {"title": "Realitní makléri v Chorvátsku", "singular": "Realitný maklér", "subtitle": "Nájdite kvalifikovaných realitných maklérov v Chorvátsku"},
        "construction_company": {"title": "Stavebné firmy v Chorvátsku", "singular": "Stavebná firma", "subtitle": "Nájdite kvalifikované stavebné firmy v Chorvátsku"},
        "lawyer": {"title": "Právnici v Chorvátsku", "singular": "Právnik", "subtitle": "Nájdite kvalifikovaných právnikov v Chorvátsku"},
        "tax_advisor": {"title": "Daňoví poradcovia v Chorvátsku", "singular": "Daňový poradca", "subtitle": "Nájdite kvalifikovaných daňových poradcov v Chorvátsku"},
        "architect": {"title": "Architekti v Chorvátsku", "singular": "Architekt", "subtitle": "Nájdite kvalifikovaných architektov v Chorvátsku"},
        "view_profile": "Zobraziť profil",
        "back_to_list": "Späť na zoznam",
        "contact": "Kontakt",
        "languages": "Jazyky",
        "regions": "Regióny",
        "verified": "Overené",
        "no_entries": "Žiadne záznamy nenájdené.",
        "disclaimer": "Tento obsah slúži len na všeobecné informácie a nepredstavuje odbornú radu.",
        "last_updated": "Posledná aktualizácia",
        "profile": "Profil",
        "company": "Spoločnosť",
        "areas_of_activity": "Oblasti činnosti",
        "working_approach": "Spôsob práce",
        "faq": "Často kladené otázky",
        "registration": "Registrácia",
    },
}


def get_lang_from_request(request, country):
    # Session-Sprache hat Vorrang (damit Sprachwechsel funktioniert)
    session_lang = request.session.get("site_language")
    if session_lang:
        return session_lang
    # Fallback: URL-Land
    lang = COUNTRY_TO_LANG.get(country)
    if lang:
        return lang
    return "ge"


def professional_list(request, country, category):
    lang = get_lang_from_request(request, country)
    
    # Finde den professional_type aus der URL-Kategorie
    professional_type = None
    for ptype, urls in CATEGORY_URLS.items():
        if category in urls.values():
            professional_type = ptype
            break
    
    if not professional_type:
        raise Http404("Kategorie nicht gefunden")
    
    professionals = Professional.objects.filter(
        professional_type=professional_type,
        is_active=True
    ).order_by("name")
    
    trans = TRANSLATIONS.get(lang, TRANSLATIONS["ge"])
    cat_trans = trans.get(professional_type, {})
    url_paths = CATEGORY_URLS.get(professional_type, {})
    country_name = COUNTRY_NAMES.get(lang, "kroatien")
    
    # Übersetze Regionen und Sprachen für jedes Profil
    professionals_with_translations = []
    for prof in professionals:
        prof.translated_region = translate_region(prof.region, lang)
        prof.translated_languages = translate_languages(prof.languages_spoken, lang)
        professionals_with_translations.append(prof)
    
    return render(request, "main/professional_list.html", {
        "professionals": professionals_with_translations,
        "professional_type": professional_type,
        "title": cat_trans.get("title", ""),
        "subtitle": cat_trans.get("subtitle", ""),
        "trans": trans,
        "lang": lang,
        "country_name": country_name,
        "url_path": url_paths.get(lang, category),
    })


def professional_detail(request, country, category, slug):
    lang = get_lang_from_request(request, country)
    
    professional = get_object_or_404(Professional, slug=slug, is_active=True)
    
    # Hole sprachspezifischen Content
    try:
        content = ProfessionalContent.objects.get(professional=professional, language=lang)
    except ProfessionalContent.DoesNotExist:
        content = None
    
    trans = TRANSLATIONS.get(lang, TRANSLATIONS["ge"])
    cat_trans = trans.get(professional.professional_type, {})
    url_paths = CATEGORY_URLS.get(professional.professional_type, {})
    country_name = COUNTRY_NAMES.get(lang, "kroatien")
    
    # Übersetzte Felder
    translated_region = translate_region(professional.region, lang)
    translated_languages = translate_languages(professional.languages_spoken, lang)
    
    # Service-Regionen übersetzen (kommagetrennt)
    translated_service_regions = ""
    if professional.service_regions:
        regions = [r.strip() for r in professional.service_regions.split(",")]
        translated_service_regions = ", ".join([translate_region(r, lang) for r in regions])
    
    # Monat übersetzen
    current_month = MONTH_TRANSLATIONS.get(lang, "Januar")
    
    return render(request, "main/professional_detail.html", {
        "professional": professional,
        "content": content,
        "singular": cat_trans.get("singular", ""),
        "trans": trans,
        "lang": lang,
        "country_name": country_name,
        "url_path": url_paths.get(lang, category),
        "translated_region": translated_region,
        "translated_languages": translated_languages,
        "translated_service_regions": translated_service_regions,
        "current_month": current_month,
    })


from main.professional_forms import ProfessionalRegistrationForm, FORM_LABELS

def professional_registration(request, country):
    lang = get_lang_from_request(request, country)
    
    # Nur DE und HR erlaubt
    if lang not in ["ge", "hr"]:
        lang = "ge"
    
    labels = FORM_LABELS.get(lang, FORM_LABELS["ge"])
    success = False
    
    if request.method == "POST":
        form = ProfessionalRegistrationForm(request.POST, request.FILES, lang=lang)
        print("FORM ERRORS:", form.errors); print("IS VALID:", form.is_valid()); 
        if form.is_valid():
            professional = form.save()
            # E-Mail Benachrichtigung senden
            try:
                email_body = f"Neue Professional-Registrierung:\n\nName: {professional.name}\nTyp: {professional.professional_type}\nE-Mail: {professional.email}\nTelefon: {professional.phone}\nStadt: {professional.city}\nRegion: {professional.region}"
                send_mail("Neue Professional-Registrierung", email_body, "service.mahamudh472@gmail.com", ["ja@brandoz.de"], fail_silently=False)
            except Exception as e:
                print(f"E-Mail Fehler: {e}")
            success = True
    else:
        form = ProfessionalRegistrationForm(lang=lang)
    
    country_name = COUNTRY_NAMES.get(lang, "kroatien")
    
    return render(request, "main/professional_registration.html", {
        "form": form,
        "labels": labels,
        "lang": lang,
        "country_name": country_name,
        "success": success,
    })
