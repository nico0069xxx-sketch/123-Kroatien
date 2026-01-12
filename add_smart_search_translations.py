#!/usr/bin/env python3
"""
Fügt Smart-Search Übersetzungen zur Datenbank hinzu
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
django.setup()

from pages.models import Translation

# Smart-Search Übersetzungen
TRANSLATIONS = [
    {
        'name': 'smart_search_title',
        'page': 'home',
        'german_content': 'KI-Immobiliensuche',
        'english_content': 'AI Property Search',
        'croatian_content': 'AI Pretraživanje Nekretnina',
        'french_content': 'Recherche Immobilière IA',
        'dutch_content': 'AI Vastgoed Zoeken',
        'polish_content': 'Wyszukiwanie Nieruchomości AI',
        'czech_content': 'AI Vyhledávání Nemovitostí',
        'slovak_content': 'AI Vyhľadávanie Nehnuteľností',
        'russian_content': 'AI Поиск Недвижимости',
        'greek_content': 'AI Αναζήτηση Ακινήτων',
        'swedish_content': 'AI Fastighetssökning',
        'norway_content': 'AI Eiendomssøk',
    },
    {
        'name': 'smart_search_placeholder',
        'page': 'home',
        'german_content': 'Beschreibe deine Traumimmobilie... z.B. Haus am Meer mit Pool unter 500.000€',
        'english_content': 'Describe your dream property... e.g. House by the sea with pool under €500,000',
        'croatian_content': 'Opišite svoju nekretninu iz snova... npr. Kuća uz more s bazenom ispod 500.000€',
        'french_content': 'Décrivez votre propriété de rêve... ex. Maison en bord de mer avec piscine moins de 500.000€',
        'dutch_content': 'Beschrijf uw droomwoning... bijv. Huis aan zee met zwembad onder €500.000',
        'polish_content': 'Opisz wymarzoną nieruchomość... np. Dom nad morzem z basenem poniżej 500.000€',
        'czech_content': 'Popište svou vysněnou nemovitost... např. Dům u moře s bazénem pod 500.000€',
        'slovak_content': 'Opíšte svoju vysnívanú nehnuteľnosť... napr. Dom pri mori s bazénom pod 500.000€',
        'russian_content': 'Опишите недвижимость вашей мечты... напр. Дом у моря с бассейном до 500.000€',
        'greek_content': 'Περιγράψτε το ακίνητο των ονείρων σας... π.χ. Σπίτι δίπλα στη θάλασσα με πισίνα κάτω από 500.000€',
        'swedish_content': 'Beskriv din drömfastighet... t.ex. Hus vid havet med pool under 500.000€',
        'norway_content': 'Beskriv drømmeeiendommen din... f.eks. Hus ved sjøen med basseng under 500.000€',
    },
    {
        'name': 'smart_search_loading',
        'page': 'home',
        'german_content': 'Suche läuft...',
        'english_content': 'Searching...',
        'croatian_content': 'Pretraživanje...',
        'french_content': 'Recherche en cours...',
        'dutch_content': 'Zoeken...',
        'polish_content': 'Wyszukiwanie...',
        'czech_content': 'Vyhledávání...',
        'slovak_content': 'Vyhľadávanie...',
        'russian_content': 'Поиск...',
        'greek_content': 'Αναζήτηση...',
        'swedish_content': 'Söker...',
        'norway_content': 'Søker...',
    },
    {
        'name': 'smart_search_found',
        'page': 'home',
        'german_content': 'Ich habe {count} passende Immobilien für dich gefunden!',
        'english_content': 'I found {count} matching properties for you!',
        'croatian_content': 'Pronašao sam {count} odgovarajućih nekretnina za vas!',
        'french_content': "J'ai trouvé {count} propriétés correspondantes pour vous!",
        'dutch_content': 'Ik heb {count} passende woningen voor u gevonden!',
        'polish_content': 'Znalazłem {count} pasujących nieruchomości dla Ciebie!',
        'czech_content': 'Našel jsem pro vás {count} odpovídajících nemovitostí!',
        'slovak_content': 'Našiel som pre vás {count} zodpovedajúcich nehnuteľností!',
        'russian_content': 'Я нашел {count} подходящих объектов для вас!',
        'greek_content': 'Βρήκα {count} κατάλληλα ακίνητα για εσάς!',
        'swedish_content': 'Jag hittade {count} matchande fastigheter åt dig!',
        'norway_content': 'Jeg fant {count} matchende eiendommer for deg!',
    },
    {
        'name': 'smart_search_none',
        'page': 'home',
        'german_content': 'Leider keine passenden Immobilien gefunden. Versuche andere Kriterien.',
        'english_content': 'No matching properties found. Try different criteria.',
        'croatian_content': 'Nažalost, nisu pronađene odgovarajuće nekretnine. Pokušajte s drugim kriterijima.',
        'french_content': 'Aucune propriété correspondante trouvée. Essayez d\'autres critères.',
        'dutch_content': 'Geen passende woningen gevonden. Probeer andere criteria.',
        'polish_content': 'Nie znaleziono pasujących nieruchomości. Spróbuj innych kryteriów.',
        'czech_content': 'Nebyly nalezeny žádné odpovídající nemovitosti. Zkuste jiná kritéria.',
        'slovak_content': 'Nenašli sa žiadne zodpovedajúce nehnuteľnosti. Skúste iné kritériá.',
        'russian_content': 'Подходящих объектов не найдено. Попробуйте другие критерии.',
        'greek_content': 'Δεν βρέθηκαν αντίστοιχα ακίνητα. Δοκιμάστε διαφορετικά κριτήρια.',
        'swedish_content': 'Inga matchande fastigheter hittades. Prova andra kriterier.',
        'norway_content': 'Ingen matchende eiendommer funnet. Prøv andre kriterier.',
    },
]

count = 0
for t in TRANSLATIONS:
    obj, created = Translation.objects.update_or_create(
        name=t['name'],
        defaults=t
    )
    if created:
        print(f"✅ Erstellt: {t['name']}")
        count += 1
    else:
        print(f"🔄 Aktualisiert: {t['name']}")

print(f"\n🎉 Fertig! {count} neue Übersetzungen hinzugefügt.")
