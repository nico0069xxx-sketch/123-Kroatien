"""
Bulk Translation Import - Fügt vordefinierte Übersetzungen in die Datenbank ein
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'realstate.settings')
sys.path.insert(0, '/app/real-estate-django-main')
django.setup()

from pages.models import Translation

# Vordefinierte Übersetzungen für alle 86 Texte in 12 Sprachen
TRANSLATIONS = [
    # Navigation
    {'name': 'nav_buy', 'page': 'navbar', 'ge': 'Kaufen', 'en': 'Buy', 'fr': 'Acheter', 'gr': 'Αγοράστε', 'hr': 'Kupiti', 'pl': 'Kup', 'cz': 'Koupit', 'ru': 'Купить', 'sw': 'Köpa', 'no': 'Kjøpe', 'sk': 'Kúpiť', 'nl': 'Kopen'},
    {'name': 'nav_sell', 'page': 'navbar', 'ge': 'Verkaufen', 'en': 'Sell', 'fr': 'Vendre', 'gr': 'Πουλήστε', 'hr': 'Prodati', 'pl': 'Sprzedaj', 'cz': 'Prodat', 'ru': 'Продать', 'sw': 'Sälja', 'no': 'Selge', 'sk': 'Predať', 'nl': 'Verkopen'},
    {'name': 'nav_contact', 'page': 'navbar', 'ge': 'Kontakt', 'en': 'Contact', 'fr': 'Contact', 'gr': 'Επικοινωνία', 'hr': 'Kontakt', 'pl': 'Kontakt', 'cz': 'Kontakt', 'ru': 'Контакт', 'sw': 'Kontakt', 'no': 'Kontakt', 'sk': 'Kontakt', 'nl': 'Contact'},
    {'name': 'nav_about', 'page': 'navbar', 'ge': 'Über uns', 'en': 'About us', 'fr': 'À propos', 'gr': 'Σχετικά με εμάς', 'hr': 'O nama', 'pl': 'O nas', 'cz': 'O nás', 'ru': 'О нас', 'sw': 'Om oss', 'no': 'Om oss', 'sk': 'O nás', 'nl': 'Over ons'},
    {'name': 'nav_faq', 'page': 'navbar', 'ge': 'F.A.Q', 'en': 'FAQ', 'fr': 'FAQ', 'gr': 'Συχνές ερωτήσεις', 'hr': 'Česta pitanja', 'pl': 'FAQ', 'cz': 'FAQ', 'ru': 'FAQ', 'sw': 'FAQ', 'no': 'FAQ', 'sk': 'FAQ', 'nl': 'FAQ'},
    {'name': 'nav_add_listing', 'page': 'navbar', 'ge': 'Immobilie hinzufügen', 'en': 'Add property', 'fr': 'Ajouter bien', 'gr': 'Προσθήκη ακινήτου', 'hr': 'Dodaj nekretninu', 'pl': 'Dodaj nieruchomość', 'cz': 'Přidat nemovitost', 'ru': 'Добавить недвижимость', 'sw': 'Lägg till fastighet', 'no': 'Legg til eiendom', 'sk': 'Pridať nehnuteľnosť', 'nl': 'Eigendom toevoegen'},
    {'name': 'nav_logout', 'page': 'navbar', 'ge': 'Abmelden', 'en': 'Logout', 'fr': 'Déconnexion', 'gr': 'Αποσύνδεση', 'hr': 'Odjava', 'pl': 'Wyloguj', 'cz': 'Odhlásit', 'ru': 'Выйти', 'sw': 'Logga ut', 'no': 'Logg ut', 'sk': 'Odhlásiť', 'nl': 'Uitloggen'},
    {'name': 'nav_login', 'page': 'navbar', 'ge': 'Anmelden', 'en': 'Login', 'fr': 'Connexion', 'gr': 'Σύνδεση', 'hr': 'Prijava', 'pl': 'Zaloguj', 'cz': 'Přihlásit', 'ru': 'Войти', 'sw': 'Logga in', 'no': 'Logg inn', 'sk': 'Prihlásiť', 'nl': 'Inloggen'},
    {'name': 'nav_register', 'page': 'navbar', 'ge': 'Registrieren', 'en': 'Register', 'fr': 'Inscription', 'gr': 'Εγγραφή', 'hr': 'Registracija', 'pl': 'Rejestracja', 'cz': 'Registrace', 'ru': 'Регистрация', 'sw': 'Registrera', 'no': 'Registrer', 'sk': 'Registrácia', 'nl': 'Registreren'},
    
    # Dropdown Kaufen
    {'name': 'dropdown_house', 'page': 'navbar', 'ge': 'Haus', 'en': 'House', 'fr': 'Maison', 'gr': 'Σπίτι', 'hr': 'Kuća', 'pl': 'Dom', 'cz': 'Dům', 'ru': 'Дом', 'sw': 'Hus', 'no': 'Hus', 'sk': 'Dom', 'nl': 'Huis'},
    {'name': 'dropdown_apartment', 'page': 'navbar', 'ge': 'Wohnung', 'en': 'Apartment', 'fr': 'Appartement', 'gr': 'Διαμέρισμα', 'hr': 'Stan', 'pl': 'Mieszkanie', 'cz': 'Byt', 'ru': 'Квартира', 'sw': 'Lägenhet', 'no': 'Leilighet', 'sk': 'Byt', 'nl': 'Appartement'},
    {'name': 'dropdown_new_building', 'page': 'navbar', 'ge': 'Neubau', 'en': 'New construction', 'fr': 'Neuf', 'gr': 'Νέα κατασκευή', 'hr': 'Novogradnja', 'pl': 'Nowe budownictwo', 'cz': 'Novostavba', 'ru': 'Новостройка', 'sw': 'Nybyggnation', 'no': 'Nybygg', 'sk': 'Novostavba', 'nl': 'Nieuwbouw'},
    {'name': 'dropdown_land', 'page': 'navbar', 'ge': 'Grundstück', 'en': 'Land', 'fr': 'Terrain', 'gr': 'Οικόπεδο', 'hr': 'Zemljište', 'pl': 'Działka', 'cz': 'Pozemek', 'ru': 'Участок', 'sw': 'Mark', 'no': 'Tomt', 'sk': 'Pozemok', 'nl': 'Grond'},
    
    # Dropdown Benutzer
    {'name': 'dropdown_realtor', 'page': 'navbar', 'ge': 'Immobilienmakler', 'en': 'Real estate agent', 'fr': 'Agent immobilier', 'gr': 'Μεσίτης', 'hr': 'Agent za nekretnine', 'pl': 'Agent nieruchomości', 'cz': 'Realitní makléř', 'ru': 'Риэлтор', 'sw': 'Fastighetsmäklare', 'no': 'Eiendomsmegler', 'sk': 'Realitný maklér', 'nl': 'Makelaar'},
    {'name': 'dropdown_contractor', 'page': 'navbar', 'ge': 'Bauunternehmer', 'en': 'Building contractor', 'fr': 'Entrepreneur', 'gr': 'Κατασκευαστής', 'hr': 'Građevinar', 'pl': 'Wykonawca', 'cz': 'Stavitel', 'ru': 'Подрядчик', 'sw': 'Byggentreprenör', 'no': 'Byggentreprenør', 'sk': 'Staviteľ', 'nl': 'Aannemer'},
    {'name': 'dropdown_owner', 'page': 'navbar', 'ge': 'Eigentümer', 'en': 'Owner', 'fr': 'Propriétaire', 'gr': 'Ιδιοκτήτης', 'hr': 'Vlasnik', 'pl': 'Właściciel', 'cz': 'Vlastník', 'ru': 'Владелец', 'sw': 'Ägare', 'no': 'Eier', 'sk': 'Vlastník', 'nl': 'Eigenaar'},
    
    # Labels
    {'name': 'label_for_sale', 'page': 'listings', 'ge': 'Zu verkaufen', 'en': 'For sale', 'fr': 'À vendre', 'gr': 'Προς πώληση', 'hr': 'Na prodaju', 'pl': 'Na sprzedaż', 'cz': 'Na prodej', 'ru': 'Продаётся', 'sw': 'Till salu', 'no': 'Til salgs', 'sk': 'Na predaj', 'nl': 'Te koop'},
    {'name': 'label_for_rent', 'page': 'listings', 'ge': 'Zu vermieten', 'en': 'For rent', 'fr': 'À louer', 'gr': 'Προς ενοικίαση', 'hr': 'Za najam', 'pl': 'Do wynajęcia', 'cz': 'K pronájmu', 'ru': 'Сдаётся', 'sw': 'Att hyra', 'no': 'Til leie', 'sk': 'Na prenájom', 'nl': 'Te huur'},
    {'name': 'label_bedrooms', 'page': 'listings', 'ge': 'Schlafzimmer', 'en': 'Bedrooms', 'fr': 'Chambres', 'gr': 'Υπνοδωμάτια', 'hr': 'Spavaće sobe', 'pl': 'Sypialnie', 'cz': 'Ložnice', 'ru': 'Спальни', 'sw': 'Sovrum', 'no': 'Soverom', 'sk': 'Spálne', 'nl': 'Slaapkamers'},
    {'name': 'label_bathrooms', 'page': 'listings', 'ge': 'Badezimmer', 'en': 'Bathrooms', 'fr': 'Salles de bain', 'gr': 'Μπάνια', 'hr': 'Kupaonice', 'pl': 'Łazienki', 'cz': 'Koupelny', 'ru': 'Ванные', 'sw': 'Badrum', 'no': 'Bad', 'sk': 'Kúpeľne', 'nl': 'Badkamers'},
    {'name': 'label_area', 'page': 'listings', 'ge': 'Fläche', 'en': 'Area', 'fr': 'Surface', 'gr': 'Έκταση', 'hr': 'Površina', 'pl': 'Powierzchnia', 'cz': 'Plocha', 'ru': 'Площадь', 'sw': 'Yta', 'no': 'Areal', 'sk': 'Plocha', 'nl': 'Oppervlakte'},
    {'name': 'label_sqm', 'page': 'listings', 'ge': 'qm', 'en': 'sqm', 'fr': 'm²', 'gr': 'τ.μ.', 'hr': 'm²', 'pl': 'm²', 'cz': 'm²', 'ru': 'м²', 'sw': 'kvm', 'no': 'kvm', 'sk': 'm²', 'nl': 'm²'},
    {'name': 'label_price', 'page': 'listings', 'ge': 'Preis', 'en': 'Price', 'fr': 'Prix', 'gr': 'Τιμή', 'hr': 'Cijena', 'pl': 'Cena', 'cz': 'Cena', 'ru': 'Цена', 'sw': 'Pris', 'no': 'Pris', 'sk': 'Cena', 'nl': 'Prijs'},
    {'name': 'label_description', 'page': 'property details', 'ge': 'Beschreibung', 'en': 'Description', 'fr': 'Description', 'gr': 'Περιγραφή', 'hr': 'Opis', 'pl': 'Opis', 'cz': 'Popis', 'ru': 'Описание', 'sw': 'Beskrivning', 'no': 'Beskrivelse', 'sk': 'Popis', 'nl': 'Beschrijving'},
    {'name': 'label_features', 'page': 'property details', 'ge': 'Ausstattung', 'en': 'Features', 'fr': 'Équipements', 'gr': 'Χαρακτηριστικά', 'hr': 'Oprema', 'pl': 'Wyposażenie', 'cz': 'Vybavení', 'ru': 'Удобства', 'sw': 'Funktioner', 'no': 'Funksjoner', 'sk': 'Vybavenie', 'nl': 'Kenmerken'},
    {'name': 'label_location', 'page': 'property details', 'ge': 'Standort', 'en': 'Location', 'fr': 'Emplacement', 'gr': 'Τοποθεσία', 'hr': 'Lokacija', 'pl': 'Lokalizacja', 'cz': 'Lokalita', 'ru': 'Расположение', 'sw': 'Plats', 'no': 'Beliggenhet', 'sk': 'Poloha', 'nl': 'Locatie'},
    {'name': 'label_details', 'page': 'property details', 'ge': 'Details', 'en': 'Details', 'fr': 'Détails', 'gr': 'Λεπτομέρειες', 'hr': 'Detalji', 'pl': 'Szczegóły', 'cz': 'Detaily', 'ru': 'Детали', 'sw': 'Detaljer', 'no': 'Detaljer', 'sk': 'Detaily', 'nl': 'Details'},
    {'name': 'label_garage', 'page': 'property details', 'ge': 'Garage', 'en': 'Garage', 'fr': 'Garage', 'gr': 'Γκαράζ', 'hr': 'Garaža', 'pl': 'Garaż', 'cz': 'Garáž', 'ru': 'Гараж', 'sw': 'Garage', 'no': 'Garasje', 'sk': 'Garáž', 'nl': 'Garage'},
    {'name': 'label_floors', 'page': 'property details', 'ge': 'Etagen', 'en': 'Floors', 'fr': 'Étages', 'gr': 'Όροφοι', 'hr': 'Katovi', 'pl': 'Piętra', 'cz': 'Podlaží', 'ru': 'Этажи', 'sw': 'Våningar', 'no': 'Etasjer', 'sk': 'Poschodia', 'nl': 'Verdiepingen'},
    {'name': 'label_deposit', 'page': 'property details', 'ge': 'Anzahlung', 'en': 'Deposit', 'fr': 'Acompte', 'gr': 'Προκαταβολή', 'hr': 'Polog', 'pl': 'Zaliczka', 'cz': 'Záloha', 'ru': 'Депозит', 'sw': 'Deposition', 'no': 'Depositum', 'sk': 'Záloha', 'nl': 'Aanbetaling'},
    {'name': 'label_property_id', 'page': 'property details', 'ge': 'Immobilien-ID', 'en': 'Property ID', 'fr': 'ID du bien', 'gr': 'ID Ακινήτου', 'hr': 'ID Nekretnine', 'pl': 'ID Nieruchomości', 'cz': 'ID Nemovitosti', 'ru': 'ID Недвижимости', 'sw': 'Fastighets-ID', 'no': 'Eiendoms-ID', 'sk': 'ID Nehnuteľnosti', 'nl': 'Eigendom-ID'},
    {'name': 'label_property_type', 'page': 'property details', 'ge': 'Immobilientyp', 'en': 'Property type', 'fr': 'Type de bien', 'gr': 'Τύπος ακινήτου', 'hr': 'Tip nekretnine', 'pl': 'Typ nieruchomości', 'cz': 'Typ nemovitosti', 'ru': 'Тип недвижимости', 'sw': 'Fastighetstyp', 'no': 'Eiendomstype', 'sk': 'Typ nehnuteľnosti', 'nl': 'Type eigendom'},
    {'name': 'label_property_status', 'page': 'property details', 'ge': 'Status', 'en': 'Status', 'fr': 'Statut', 'gr': 'Κατάσταση', 'hr': 'Status', 'pl': 'Status', 'cz': 'Stav', 'ru': 'Статус', 'sw': 'Status', 'no': 'Status', 'sk': 'Stav', 'nl': 'Status'},
    
    # Buttons
    {'name': 'btn_view_details', 'page': 'listings', 'ge': 'Details anzeigen', 'en': 'View details', 'fr': 'Voir détails', 'gr': 'Λεπτομέρειες', 'hr': 'Pogledaj detalje', 'pl': 'Zobacz szczegóły', 'cz': 'Zobrazit detaily', 'ru': 'Подробнее', 'sw': 'Visa detaljer', 'no': 'Se detaljer', 'sk': 'Zobraziť detaily', 'nl': 'Details bekijken'},
    {'name': 'btn_contact_agent', 'page': 'property details', 'ge': 'Makler kontaktieren', 'en': 'Contact agent', 'fr': 'Contacter agent', 'gr': 'Επικοινωνία με μεσίτη', 'hr': 'Kontaktiraj agenta', 'pl': 'Kontakt z agentem', 'cz': 'Kontaktovat makléře', 'ru': 'Связаться с агентом', 'sw': 'Kontakta mäklare', 'no': 'Kontakt megler', 'sk': 'Kontaktovať agenta', 'nl': 'Contact makelaar'},
    {'name': 'btn_send_message', 'page': 'contact', 'ge': 'Nachricht senden', 'en': 'Send message', 'fr': 'Envoyer message', 'gr': 'Αποστολή μηνύματος', 'hr': 'Pošalji poruku', 'pl': 'Wyślij wiadomość', 'cz': 'Odeslat zprávu', 'ru': 'Отправить сообщение', 'sw': 'Skicka meddelande', 'no': 'Send melding', 'sk': 'Odoslať správu', 'nl': 'Bericht versturen'},
    {'name': 'btn_submit', 'page': 'contact', 'ge': 'Absenden', 'en': 'Submit', 'fr': 'Soumettre', 'gr': 'Υποβολή', 'hr': 'Pošalji', 'pl': 'Wyślij', 'cz': 'Odeslat', 'ru': 'Отправить', 'sw': 'Skicka', 'no': 'Send', 'sk': 'Odoslať', 'nl': 'Verzenden'},
    {'name': 'btn_search', 'page': 'home', 'ge': 'Suchen', 'en': 'Search', 'fr': 'Rechercher', 'gr': 'Αναζήτηση', 'hr': 'Traži', 'pl': 'Szukaj', 'cz': 'Hledat', 'ru': 'Поиск', 'sw': 'Sök', 'no': 'Søk', 'sk': 'Hľadať', 'nl': 'Zoeken'},
    {'name': 'btn_load_more', 'page': 'listings', 'ge': 'Mehr laden', 'en': 'Load more', 'fr': 'Charger plus', 'gr': 'Φόρτωση περισσοτέρων', 'hr': 'Učitaj više', 'pl': 'Załaduj więcej', 'cz': 'Načíst více', 'ru': 'Загрузить ещё', 'sw': 'Ladda mer', 'no': 'Last mer', 'sk': 'Načítať viac', 'nl': 'Meer laden'},
    
    # Homepage
    {'name': 'home_title', 'page': 'home', 'ge': 'Finden Sie Ihre Traumimmobilie in Kroatien', 'en': 'Find your dream property in Croatia', 'fr': 'Trouvez votre bien de rêve en Croatie', 'gr': 'Βρείτε το ακίνητο των ονείρων σας στην Κροατία', 'hr': 'Pronađite svoju nekretninu iz snova u Hrvatskoj', 'pl': 'Znajdź wymarzoną nieruchomość w Chorwacji', 'cz': 'Najděte svůj vysněný majetek v Chorvatsku', 'ru': 'Найдите недвижимость своей мечты в Хорватии', 'sw': 'Hitta din drömfastighet i Kroatien', 'no': 'Finn drømmeeiendommen din i Kroatia', 'sk': 'Nájdite svoju vysnívanú nehnuteľnosť v Chorvátsku', 'nl': 'Vind uw droomwoning in Kroatië'},
    {'name': 'home_subtitle', 'page': 'home', 'ge': 'Entdecken Sie die besten Immobilien an der kroatischen Küste', 'en': 'Discover the best properties on the Croatian coast', 'fr': 'Découvrez les meilleurs biens sur la côte croate', 'gr': 'Ανακαλύψτε τα καλύτερα ακίνητα στην κροατική ακτή', 'hr': 'Otkrijte najbolje nekretnine na hrvatskoj obali', 'pl': 'Odkryj najlepsze nieruchomości na chorwackim wybrzeżu', 'cz': 'Objevte nejlepší nemovitosti na chorvatském pobřeží', 'ru': 'Откройте лучшую недвижимость на побережье Хорватии', 'sw': 'Upptäck de bästa fastigheterna på den kroatiska kusten', 'no': 'Oppdag de beste eiendommene på den kroatiske kysten', 'sk': 'Objavte najlepšie nehnuteľnosti na chorvátskom pobreží', 'nl': 'Ontdek de beste woningen aan de Kroatische kust'},
    {'name': 'home_latest_listings', 'page': 'home', 'ge': 'Neueste Immobilien', 'en': 'Latest properties', 'fr': 'Derniers biens', 'gr': 'Τελευταία ακίνητα', 'hr': 'Najnovije nekretnine', 'pl': 'Najnowsze nieruchomości', 'cz': 'Nejnovější nemovitosti', 'ru': 'Последние объекты', 'sw': 'Senaste fastigheter', 'no': 'Nyeste eiendommer', 'sk': 'Najnovšie nehnuteľnosti', 'nl': 'Nieuwste woningen'},
    {'name': 'home_featured', 'page': 'home', 'ge': 'Empfohlene Immobilien', 'en': 'Featured properties', 'fr': 'Biens en vedette', 'gr': 'Προτεινόμενα ακίνητα', 'hr': 'Istaknute nekretnine', 'pl': 'Wyróżnione nieruchomości', 'cz': 'Doporučené nemovitosti', 'ru': 'Рекомендуемые объекты', 'sw': 'Utvalda fastigheter', 'no': 'Utvalgte eiendommer', 'sk': 'Odporúčané nehnuteľnosti', 'nl': 'Uitgelichte woningen'},
    
    # Property Types
    {'name': 'type_house', 'page': 'listings', 'ge': 'Haus', 'en': 'House', 'fr': 'Maison', 'gr': 'Σπίτι', 'hr': 'Kuća', 'pl': 'Dom', 'cz': 'Dům', 'ru': 'Дом', 'sw': 'Hus', 'no': 'Hus', 'sk': 'Dom', 'nl': 'Huis'},
    {'name': 'type_apartment', 'page': 'listings', 'ge': 'Wohnung', 'en': 'Apartment', 'fr': 'Appartement', 'gr': 'Διαμέρισμα', 'hr': 'Stan', 'pl': 'Mieszkanie', 'cz': 'Byt', 'ru': 'Квартира', 'sw': 'Lägenhet', 'no': 'Leilighet', 'sk': 'Byt', 'nl': 'Appartement'},
    {'name': 'type_villa', 'page': 'listings', 'ge': 'Villa', 'en': 'Villa', 'fr': 'Villa', 'gr': 'Βίλα', 'hr': 'Vila', 'pl': 'Willa', 'cz': 'Vila', 'ru': 'Вилла', 'sw': 'Villa', 'no': 'Villa', 'sk': 'Vila', 'nl': 'Villa'},
    {'name': 'type_office', 'page': 'listings', 'ge': 'Büro', 'en': 'Office', 'fr': 'Bureau', 'gr': 'Γραφείο', 'hr': 'Ured', 'pl': 'Biuro', 'cz': 'Kancelář', 'ru': 'Офис', 'sw': 'Kontor', 'no': 'Kontor', 'sk': 'Kancelária', 'nl': 'Kantoor'},
    {'name': 'type_land', 'page': 'listings', 'ge': 'Grundstück', 'en': 'Land', 'fr': 'Terrain', 'gr': 'Οικόπεδο', 'hr': 'Zemljište', 'pl': 'Działka', 'cz': 'Pozemek', 'ru': 'Участок', 'sw': 'Mark', 'no': 'Tomt', 'sk': 'Pozemok', 'nl': 'Grond'},
    {'name': 'type_family_house', 'page': 'listings', 'ge': 'Familienhaus', 'en': 'Family house', 'fr': 'Maison familiale', 'gr': 'Οικογενειακή κατοικία', 'hr': 'Obiteljska kuća', 'pl': 'Dom rodzinny', 'cz': 'Rodinný dům', 'ru': 'Семейный дом', 'sw': 'Familjehus', 'no': 'Familiehus', 'sk': 'Rodinný dom', 'nl': 'Gezinswoning'},
    {'name': 'type_modern_villa', 'page': 'listings', 'ge': 'Moderne Villa', 'en': 'Modern villa', 'fr': 'Villa moderne', 'gr': 'Μοντέρνα βίλα', 'hr': 'Moderna vila', 'pl': 'Nowoczesna willa', 'cz': 'Moderní vila', 'ru': 'Современная вилла', 'sw': 'Modern villa', 'no': 'Moderne villa', 'sk': 'Moderná vila', 'nl': 'Moderne villa'},
    {'name': 'type_town_house', 'page': 'listings', 'ge': 'Stadthaus', 'en': 'Town house', 'fr': 'Maison de ville', 'gr': 'Αστική κατοικία', 'hr': 'Gradska kuća', 'pl': 'Kamienica', 'cz': 'Městský dům', 'ru': 'Таунхаус', 'sw': 'Radhus', 'no': 'Rekkehus', 'sk': 'Mestský dom', 'nl': 'Stadswoning'},
    
    # Footer
    {'name': 'footer_about', 'page': 'footer', 'ge': 'Über uns', 'en': 'About us', 'fr': 'À propos', 'gr': 'Σχετικά με εμάς', 'hr': 'O nama', 'pl': 'O nas', 'cz': 'O nás', 'ru': 'О нас', 'sw': 'Om oss', 'no': 'Om oss', 'sk': 'O nás', 'nl': 'Over ons'},
    {'name': 'footer_contact', 'page': 'footer', 'ge': 'Kontakt', 'en': 'Contact', 'fr': 'Contact', 'gr': 'Επικοινωνία', 'hr': 'Kontakt', 'pl': 'Kontakt', 'cz': 'Kontakt', 'ru': 'Контакт', 'sw': 'Kontakt', 'no': 'Kontakt', 'sk': 'Kontakt', 'nl': 'Contact'},
    {'name': 'footer_privacy', 'page': 'footer', 'ge': 'Datenschutz', 'en': 'Privacy', 'fr': 'Confidentialité', 'gr': 'Απόρρητο', 'hr': 'Privatnost', 'pl': 'Prywatność', 'cz': 'Ochrana osobních údajů', 'ru': 'Конфиденциальность', 'sw': 'Integritet', 'no': 'Personvern', 'sk': 'Súkromie', 'nl': 'Privacy'},
    {'name': 'footer_imprint', 'page': 'footer', 'ge': 'Impressum', 'en': 'Imprint', 'fr': 'Mentions légales', 'gr': 'Αποτύπωμα', 'hr': 'Impressum', 'pl': 'Impressum', 'cz': 'Impressum', 'ru': 'Выходные данные', 'sw': 'Impressum', 'no': 'Impressum', 'sk': 'Impressum', 'nl': 'Impressum'},
    {'name': 'footer_terms', 'page': 'footer', 'ge': 'AGB', 'en': 'Terms', 'fr': 'CGV', 'gr': 'Όροι', 'hr': 'Uvjeti', 'pl': 'Warunki', 'cz': 'Podmínky', 'ru': 'Условия', 'sw': 'Villkor', 'no': 'Vilkår', 'sk': 'Podmienky', 'nl': 'Voorwaarden'},
    {'name': 'footer_sitemap', 'page': 'footer', 'ge': 'Sitemap', 'en': 'Sitemap', 'fr': 'Plan du site', 'gr': 'Χάρτης', 'hr': 'Mapa stranica', 'pl': 'Mapa strony', 'cz': 'Mapa stránek', 'ru': 'Карта сайта', 'sw': 'Webbkarta', 'no': 'Nettstedskart', 'sk': 'Mapa stránok', 'nl': 'Sitemap'},
    {'name': 'footer_copyright', 'page': 'footer', 'ge': 'Alle Rechte vorbehalten', 'en': 'All rights reserved', 'fr': 'Tous droits réservés', 'gr': 'Με επιφύλαξη παντός δικαιώματος', 'hr': 'Sva prava pridržana', 'pl': 'Wszelkie prawa zastrzeżone', 'cz': 'Všechna práva vyhrazena', 'ru': 'Все права защищены', 'sw': 'Alla rättigheter reserverade', 'no': 'Alle rettigheter forbeholdes', 'sk': 'Všetky práva vyhradené', 'nl': 'Alle rechten voorbehouden'},
    
    # Contact
    {'name': 'contact_title', 'page': 'contact', 'ge': 'Kontaktieren Sie uns', 'en': 'Contact us', 'fr': 'Contactez-nous', 'gr': 'Επικοινωνήστε μαζί μας', 'hr': 'Kontaktirajte nas', 'pl': 'Skontaktuj się z nami', 'cz': 'Kontaktujte nás', 'ru': 'Свяжитесь с нами', 'sw': 'Kontakta oss', 'no': 'Kontakt oss', 'sk': 'Kontaktujte nás', 'nl': 'Neem contact op'},
    {'name': 'contact_name', 'page': 'contact', 'ge': 'Name', 'en': 'Name', 'fr': 'Nom', 'gr': 'Όνομα', 'hr': 'Ime', 'pl': 'Imię', 'cz': 'Jméno', 'ru': 'Имя', 'sw': 'Namn', 'no': 'Navn', 'sk': 'Meno', 'nl': 'Naam'},
    {'name': 'contact_email', 'page': 'contact', 'ge': 'E-Mail', 'en': 'Email', 'fr': 'Email', 'gr': 'Email', 'hr': 'Email', 'pl': 'Email', 'cz': 'Email', 'ru': 'Email', 'sw': 'Email', 'no': 'E-post', 'sk': 'Email', 'nl': 'Email'},
    {'name': 'contact_phone', 'page': 'contact', 'ge': 'Telefon', 'en': 'Phone', 'fr': 'Téléphone', 'gr': 'Τηλέφωνο', 'hr': 'Telefon', 'pl': 'Telefon', 'cz': 'Telefon', 'ru': 'Телефон', 'sw': 'Telefon', 'no': 'Telefon', 'sk': 'Telefón', 'nl': 'Telefoon'},
    {'name': 'contact_message', 'page': 'contact', 'ge': 'Nachricht', 'en': 'Message', 'fr': 'Message', 'gr': 'Μήνυμα', 'hr': 'Poruka', 'pl': 'Wiadomość', 'cz': 'Zpráva', 'ru': 'Сообщение', 'sw': 'Meddelande', 'no': 'Melding', 'sk': 'Správa', 'nl': 'Bericht'},
    
    # About
    {'name': 'about_title', 'page': 'about', 'ge': 'Über 123-Kroatien', 'en': 'About 123-Croatia', 'fr': 'À propos de 123-Croatie', 'gr': 'Σχετικά με 123-Κροατία', 'hr': 'O 123-Hrvatska', 'pl': 'O 123-Chorwacja', 'cz': 'O 123-Chorvatsko', 'ru': 'О 123-Хорватия', 'sw': 'Om 123-Kroatien', 'no': 'Om 123-Kroatia', 'sk': 'O 123-Chorvátsko', 'nl': 'Over 123-Kroatië'},
    {'name': 'about_mission', 'page': 'about', 'ge': 'Unsere Mission', 'en': 'Our mission', 'fr': 'Notre mission', 'gr': 'Η αποστολή μας', 'hr': 'Naša misija', 'pl': 'Nasza misja', 'cz': 'Naše poslání', 'ru': 'Наша миссия', 'sw': 'Vårt uppdrag', 'no': 'Vårt oppdrag', 'sk': 'Naša misia', 'nl': 'Onze missie'},
    
    # Login/Register
    {'name': 'login_title', 'page': 'login', 'ge': 'Anmelden', 'en': 'Login', 'fr': 'Connexion', 'gr': 'Σύνδεση', 'hr': 'Prijava', 'pl': 'Logowanie', 'cz': 'Přihlášení', 'ru': 'Вход', 'sw': 'Logga in', 'no': 'Logg inn', 'sk': 'Prihlásenie', 'nl': 'Inloggen'},
    {'name': 'login_email', 'page': 'login', 'ge': 'E-Mail Adresse', 'en': 'Email address', 'fr': 'Adresse email', 'gr': 'Διεύθυνση email', 'hr': 'Email adresa', 'pl': 'Adres email', 'cz': 'Emailová adresa', 'ru': 'Email адрес', 'sw': 'E-postadress', 'no': 'E-postadresse', 'sk': 'Emailová adresa', 'nl': 'E-mailadres'},
    {'name': 'login_password', 'page': 'login', 'ge': 'Passwort', 'en': 'Password', 'fr': 'Mot de passe', 'gr': 'Κωδικός', 'hr': 'Lozinka', 'pl': 'Hasło', 'cz': 'Heslo', 'ru': 'Пароль', 'sw': 'Lösenord', 'no': 'Passord', 'sk': 'Heslo', 'nl': 'Wachtwoord'},
    {'name': 'login_remember', 'page': 'login', 'ge': 'Angemeldet bleiben', 'en': 'Remember me', 'fr': 'Se souvenir', 'gr': 'Θυμήσου με', 'hr': 'Zapamti me', 'pl': 'Zapamiętaj mnie', 'cz': 'Zapamatovat', 'ru': 'Запомнить', 'sw': 'Kom ihåg mig', 'no': 'Husk meg', 'sk': 'Zapamätať si', 'nl': 'Onthoud mij'},
    {'name': 'login_forgot', 'page': 'login', 'ge': 'Passwort vergessen?', 'en': 'Forgot password?', 'fr': 'Mot de passe oublié?', 'gr': 'Ξεχάσατε κωδικό;', 'hr': 'Zaboravili lozinku?', 'pl': 'Zapomniałeś hasła?', 'cz': 'Zapomněli heslo?', 'ru': 'Забыли пароль?', 'sw': 'Glömt lösenord?', 'no': 'Glemt passord?', 'sk': 'Zabudnuté heslo?', 'nl': 'Wachtwoord vergeten?'},
    {'name': 'register_title', 'page': 'signup', 'ge': 'Registrieren', 'en': 'Register', 'fr': 'Inscription', 'gr': 'Εγγραφή', 'hr': 'Registracija', 'pl': 'Rejestracja', 'cz': 'Registrace', 'ru': 'Регистрация', 'sw': 'Registrera', 'no': 'Registrer', 'sk': 'Registrácia', 'nl': 'Registreren'},
    {'name': 'register_firstname', 'page': 'signup', 'ge': 'Vorname', 'en': 'First name', 'fr': 'Prénom', 'gr': 'Όνομα', 'hr': 'Ime', 'pl': 'Imię', 'cz': 'Jméno', 'ru': 'Имя', 'sw': 'Förnamn', 'no': 'Fornavn', 'sk': 'Meno', 'nl': 'Voornaam'},
    {'name': 'register_lastname', 'page': 'signup', 'ge': 'Nachname', 'en': 'Last name', 'fr': 'Nom', 'gr': 'Επώνυμο', 'hr': 'Prezime', 'pl': 'Nazwisko', 'cz': 'Příjmení', 'ru': 'Фамилия', 'sw': 'Efternamn', 'no': 'Etternavn', 'sk': 'Priezvisko', 'nl': 'Achternaam'},
    {'name': 'register_confirm_password', 'page': 'signup', 'ge': 'Passwort bestätigen', 'en': 'Confirm password', 'fr': 'Confirmer mot de passe', 'gr': 'Επιβεβαίωση κωδικού', 'hr': 'Potvrdite lozinku', 'pl': 'Potwierdź hasło', 'cz': 'Potvrdit heslo', 'ru': 'Подтвердите пароль', 'sw': 'Bekräfta lösenord', 'no': 'Bekreft passord', 'sk': 'Potvrdiť heslo', 'nl': 'Bevestig wachtwoord'},
    
    # Filter/Search
    {'name': 'filter_property_type', 'page': 'listings', 'ge': 'Immobilientyp', 'en': 'Property type', 'fr': 'Type de bien', 'gr': 'Τύπος', 'hr': 'Tip', 'pl': 'Typ', 'cz': 'Typ', 'ru': 'Тип', 'sw': 'Typ', 'no': 'Type', 'sk': 'Typ', 'nl': 'Type'},
    {'name': 'filter_location', 'page': 'listings', 'ge': 'Standort', 'en': 'Location', 'fr': 'Emplacement', 'gr': 'Τοποθεσία', 'hr': 'Lokacija', 'pl': 'Lokalizacja', 'cz': 'Lokalita', 'ru': 'Расположение', 'sw': 'Plats', 'no': 'Beliggenhet', 'sk': 'Poloha', 'nl': 'Locatie'},
    {'name': 'filter_price_range', 'page': 'listings', 'ge': 'Preisbereich', 'en': 'Price range', 'fr': 'Fourchette de prix', 'gr': 'Εύρος τιμής', 'hr': 'Raspon cijene', 'pl': 'Zakres cen', 'cz': 'Cenové rozpětí', 'ru': 'Диапазон цен', 'sw': 'Prisintervall', 'no': 'Prisområde', 'sk': 'Cenový rozsah', 'nl': 'Prijsbereik'},
    {'name': 'filter_bedrooms', 'page': 'listings', 'ge': 'Schlafzimmer', 'en': 'Bedrooms', 'fr': 'Chambres', 'gr': 'Υπνοδωμάτια', 'hr': 'Spavaće sobe', 'pl': 'Sypialnie', 'cz': 'Ložnice', 'ru': 'Спальни', 'sw': 'Sovrum', 'no': 'Soverom', 'sk': 'Spálne', 'nl': 'Slaapkamers'},
    {'name': 'filter_bathrooms', 'page': 'listings', 'ge': 'Badezimmer', 'en': 'Bathrooms', 'fr': 'Salles de bain', 'gr': 'Μπάνια', 'hr': 'Kupaonice', 'pl': 'Łazienki', 'cz': 'Koupelny', 'ru': 'Ванные', 'sw': 'Badrum', 'no': 'Bad', 'sk': 'Kúpeľne', 'nl': 'Badkamers'},
    {'name': 'filter_min_area', 'page': 'listings', 'ge': 'Min. Fläche', 'en': 'Min. area', 'fr': 'Surface min.', 'gr': 'Ελάχ. έκταση', 'hr': 'Min. površina', 'pl': 'Min. powierzchnia', 'cz': 'Min. plocha', 'ru': 'Мин. площадь', 'sw': 'Min. yta', 'no': 'Min. areal', 'sk': 'Min. plocha', 'nl': 'Min. oppervlakte'},
    {'name': 'filter_max_area', 'page': 'listings', 'ge': 'Max. Fläche', 'en': 'Max. area', 'fr': 'Surface max.', 'gr': 'Μέγ. έκταση', 'hr': 'Maks. površina', 'pl': 'Maks. powierzchnia', 'cz': 'Max. plocha', 'ru': 'Макс. площадь', 'sw': 'Max. yta', 'no': 'Maks. areal', 'sk': 'Max. plocha', 'nl': 'Max. oppervlakte'},
    {'name': 'filter_all', 'page': 'listings', 'ge': 'Alle', 'en': 'All', 'fr': 'Tous', 'gr': 'Όλα', 'hr': 'Sve', 'pl': 'Wszystkie', 'cz': 'Vše', 'ru': 'Все', 'sw': 'Alla', 'no': 'Alle', 'sk': 'Všetko', 'nl': 'Alle'},
    
    # Messages
    {'name': 'msg_no_listings', 'page': 'listings', 'ge': 'Keine Immobilien gefunden', 'en': 'No properties found', 'fr': 'Aucun bien trouvé', 'gr': 'Δεν βρέθηκαν ακίνητα', 'hr': 'Nema nekretnina', 'pl': 'Brak nieruchomości', 'cz': 'Žádné nemovitosti', 'ru': 'Недвижимость не найдена', 'sw': 'Inga fastigheter', 'no': 'Ingen eiendommer', 'sk': 'Žiadne nehnuteľnosti', 'nl': 'Geen woningen gevonden'},
    {'name': 'msg_loading', 'page': 'home', 'ge': 'Laden...', 'en': 'Loading...', 'fr': 'Chargement...', 'gr': 'Φόρτωση...', 'hr': 'Učitavanje...', 'pl': 'Ładowanie...', 'cz': 'Načítání...', 'ru': 'Загрузка...', 'sw': 'Laddar...', 'no': 'Laster...', 'sk': 'Načítava sa...', 'nl': 'Laden...'},
    {'name': 'msg_success', 'page': 'contact', 'ge': 'Erfolgreich gesendet!', 'en': 'Successfully sent!', 'fr': 'Envoyé avec succès!', 'gr': 'Εστάλη επιτυχώς!', 'hr': 'Uspješno poslano!', 'pl': 'Wysłano pomyślnie!', 'cz': 'Úspěšně odesláno!', 'ru': 'Успешно отправлено!', 'sw': 'Skickat!', 'no': 'Sendt!', 'sk': 'Úspešne odoslané!', 'nl': 'Succesvol verzonden!'},
    {'name': 'msg_error', 'page': 'contact', 'ge': 'Ein Fehler ist aufgetreten', 'en': 'An error occurred', 'fr': 'Une erreur est survenue', 'gr': 'Παρουσιάστηκε σφάλμα', 'hr': 'Dogodila se greška', 'pl': 'Wystąpił błąd', 'cz': 'Došlo k chybě', 'ru': 'Произошла ошибка', 'sw': 'Ett fel uppstod', 'no': 'En feil oppstod', 'sk': 'Vyskytla sa chyba', 'nl': 'Er is een fout opgetreden'},
]

def import_translations():
    """Importiert alle Übersetzungen in die Datenbank"""
    # Lösche alle bestehenden
    Translation.objects.all().delete()
    print(f"Bestehende Übersetzungen gelöscht.")
    
    count = 0
    for t in TRANSLATIONS:
        translation = Translation(
            name=t['name'],
            page=t['page'],
            german_content=t['ge'],
            english_content=t['en'],
            french_content=t['fr'],
            greek_content=t['gr'],
            croatian_content=t['hr'],
            polish_content=t['pl'],
            czech_content=t['cz'],
            russian_content=t['ru'],
            swedish_content=t['sw'],
            norway_content=t['no'],
            slovak_content=t['sk'],
            dutch_content=t['nl']
        )
        translation.save()
        count += 1
    
    print(f"✓ {count} Übersetzungen erfolgreich importiert!")
    
    # Zeige einige Beispiele
    print("\nBeispiele:")
    for t in Translation.objects.all()[:5]:
        print(f"  {t.name}: DE={t.german_content}, EN={t.english_content}, HR={t.croatian_content}")

if __name__ == '__main__':
    import_translations()
