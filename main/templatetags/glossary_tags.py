from django import template

register = template.Library()

CATEGORY_TRANSLATIONS = {
    "Investoren": {
        "en": "Investors", "hr": "Investitori", "fr": "Investisseurs",
        "nl": "Investeerders", "pl": "Inwestorzy", "cz": "Investoři",
        "sk": "Investori", "ru": "Инвесторы", "gr": "Επενδυτές",
        "sw": "Investerare", "no": "Investorer"
    },
    "Ferienkäufer & Vermietung": {
        "en": "Holiday Buyers & Rental", "hr": "Kupci za odmor i najam", "fr": "Acheteurs vacances & Location",
        "nl": "Vakantiekopers & Verhuur", "pl": "Kupujący wakacje i wynajem", "cz": "Kupci dovolených a pronájem",
        "sk": "Kupci dovolenky a prenájom", "ru": "Покупатели на отдых и аренда", "gr": "Αγοραστές διακοπών & Ενοικίαση",
        "sw": "Semesterköpare & Uthyrning", "no": "Feriekjøpere & Utleie"
    },
    "Luxus & Premium": {
        "en": "Luxury & Premium", "hr": "Luksuz i Premium", "fr": "Luxe & Premium",
        "nl": "Luxe & Premium", "pl": "Luksus i Premium", "cz": "Luxus a Premium",
        "sk": "Luxus a Premium", "ru": "Люкс и Премиум", "gr": "Πολυτέλεια & Premium",
        "sw": "Lyx & Premium", "no": "Luksus & Premium"
    },
    "Recht & Grundbuch": {
        "en": "Legal & Land Registry", "hr": "Pravo i zemljišne knjige", "fr": "Droit & Cadastre",
        "nl": "Juridisch & Kadaster", "pl": "Prawo i księgi wieczyste", "cz": "Právo a katastr",
        "sk": "Právo a kataster", "ru": "Право и кадастр", "gr": "Νομικά & Κτηματολόγιο",
        "sw": "Juridik & Fastighetsregister", "no": "Jus & Grunnbok"
    },
    "Steuern": {
        "en": "Taxes", "hr": "Porezi", "fr": "Impôts",
        "nl": "Belastingen", "pl": "Podatki", "cz": "Daně",
        "sk": "Dane", "ru": "Налоги", "gr": "Φόροι",
        "sw": "Skatter", "no": "Skatter"
    },
    "Kaufprozess & Closing": {
        "en": "Purchase Process & Closing", "hr": "Proces kupnje i zatvaranje", "fr": "Processus d'achat & Clôture",
        "nl": "Aankoopproces & Closing", "pl": "Proces zakupu i zamknięcie", "cz": "Proces nákupu a uzavření",
        "sk": "Proces nákupu a uzavretie", "ru": "Процесс покупки и закрытие", "gr": "Διαδικασία αγοράς & Κλείσιμο",
        "sw": "Köpprocess & Avslut", "no": "Kjøpsprosess & Avslutning"
    },
    "Vermietung & Betrieb": {
        "en": "Rental & Operations", "hr": "Najam i poslovanje", "fr": "Location & Exploitation",
        "nl": "Verhuur & Beheer", "pl": "Wynajem i zarządzanie", "cz": "Pronájem a provoz",
        "sk": "Prenájom a prevádzka", "ru": "Аренда и эксплуатация", "gr": "Ενοικίαση & Λειτουργία",
        "sw": "Uthyrning & Drift", "no": "Utleie & Drift"
    },
    "Bewertung": {
        "en": "Valuation", "hr": "Procjena", "fr": "Évaluation",
        "nl": "Taxatie", "pl": "Wycena", "cz": "Ocenění",
        "sk": "Ocenenie", "ru": "Оценка", "gr": "Αποτίμηση",
        "sw": "Värdering", "no": "Verdivurdering"
    },
    "Finanzierung": {
        "en": "Financing", "hr": "Financiranje", "fr": "Financement",
        "nl": "Financiering", "pl": "Finansowanie", "cz": "Financování",
        "sk": "Financovanie", "ru": "Финансирование", "gr": "Χρηματοδότηση",
        "sw": "Finansiering", "no": "Finansiering"
    },
    "Bau & Genehmigungen": {
        "en": "Building & Permits", "hr": "Gradnja i dozvole", "fr": "Construction & Permis",
        "nl": "Bouw & Vergunningen", "pl": "Budowa i pozwolenia", "cz": "Stavba a povolení",
        "sk": "Stavba a povolenia", "ru": "Строительство и разрешения", "gr": "Κατασκευή & Άδειες",
        "sw": "Bygg & Tillstånd", "no": "Bygg & Tillatelser"
    },
    "Apartment/Wohnung": {
        "en": "Apartment", "hr": "Stan", "fr": "Appartement",
        "nl": "Appartement", "pl": "Mieszkanie", "cz": "Byt",
        "sk": "Byt", "ru": "Квартира", "gr": "Διαμέρισμα",
        "sw": "Lägenhet", "no": "Leilighet"
    },
    "Villa": {
        "en": "Villa", "hr": "Vila", "fr": "Villa",
        "nl": "Villa", "pl": "Willa", "cz": "Vila",
        "sk": "Vila", "ru": "Вилла", "gr": "Βίλα",
        "sw": "Villa", "no": "Villa"
    },
    "Haus": {
        "en": "House", "hr": "Kuća", "fr": "Maison",
        "nl": "Huis", "pl": "Dom", "cz": "Dům",
        "sk": "Dom", "ru": "Дом", "gr": "Σπίτι",
        "sw": "Hus", "no": "Hus"
    },
    "Grundstück": {
        "en": "Land", "hr": "Zemljište", "fr": "Terrain",
        "nl": "Grond", "pl": "Działka", "cz": "Pozemek",
        "sk": "Pozemok", "ru": "Участок", "gr": "Οικόπεδο",
        "sw": "Tomt", "no": "Tomt"
    },
    "Hotel/Resort": {
        "en": "Hotel/Resort", "hr": "Hotel/Resort", "fr": "Hôtel/Resort",
        "nl": "Hotel/Resort", "pl": "Hotel/Resort", "cz": "Hotel/Resort",
        "sk": "Hotel/Resort", "ru": "Отель/Курорт", "gr": "Ξενοδοχείο/Resort",
        "sw": "Hotell/Resort", "no": "Hotell/Resort"
    },
    "Marina": {
        "en": "Marina", "hr": "Marina", "fr": "Marina",
        "nl": "Marina", "pl": "Marina", "cz": "Marina",
        "sk": "Marina", "ru": "Марина", "gr": "Μαρίνα",
        "sw": "Marina", "no": "Marina"
    },
}

@register.filter
def translate_category(label, lang):
    """Translate category label to target language."""
    if lang == 'ge':
        return label
    translations = CATEGORY_TRANSLATIONS.get(label, {})
    return translations.get(lang, label)
