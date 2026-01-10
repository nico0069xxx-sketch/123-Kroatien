import json
import os
from django.shortcuts import render
from django.http import Http404

COUNTRY_NAMES = {
    'ge': 'kroatien',
    'en': 'croatia',
    'hr': 'hrvatska',
    'fr': 'croatie',
    'nl': 'kroatie',
    'pl': 'chorwacja',
    'cz': 'chorvatsko',
    'sk': 'chorvatsko',
    'ru': 'horvatiya',
    'gr': 'kroatia',
    'sw': 'kroatien',
    'no': 'kroatia',
}

COUNTRY_TO_LANG = {
    'kroatien': 'ge',
    'croatia': 'en',
    'hrvatska': 'hr',
    'croatie': 'fr',
    'kroatie': 'nl',
    'chorwacja': 'pl',
    'chorvatsko': 'cz',
    'horvatiya': 'ru',
    'kroatia': 'gr',
}

URL_PATHS = {
    'ge': {'reports': 'marktberichte', 'report': 'marktbericht'},
    'en': {'reports': 'market-reports', 'report': 'market-report'},
    'hr': {'reports': 'trzisna-izvjesca', 'report': 'trzisno-izvjesce'},
    'fr': {'reports': 'rapports-immobiliers', 'report': 'rapport-immobilier'},
    'nl': {'reports': 'marktrapporten', 'report': 'marktrapport'},
    'pl': {'reports': 'raporty-rynkowe', 'report': 'raport-rynkowy'},
    'cz': {'reports': 'trzni-zpravy', 'report': 'trzni-zprava'},
    'sk': {'reports': 'trhove-spravy', 'report': 'trhova-sprava'},
    'ru': {'reports': 'rynochnye-otchety', 'report': 'rynochnyj-otchet'},
    'gr': {'reports': 'anafores-agoras', 'report': 'anafora-agoras'},
    'sw': {'reports': 'marknadsrapporter', 'report': 'marknadsrapport'},
    'no': {'reports': 'markedsrapporter', 'report': 'markedsrapport'},
}

TRANSLATIONS = {
    'ge': {
        'title': 'Immobilien-Marktberichte Kroatien 2025',
        'subtitle': 'Aktuelle Marktanalysen für alle Regionen Kroatiens von 123-Kroatien.eu',
        'report_label': 'Marktbericht',
        'read_more': 'Bericht lesen',
        'back': 'Alle Berichte',
    },
    'en': {
        'title': 'Real Estate Market Reports Croatia 2025',
        'subtitle': 'Current market analysis for all regions of Croatia from 123-Kroatien.eu',
        'report_label': 'Market Report',
        'read_more': 'Read Report',
        'back': 'All Reports',
    },
    'hr': {
        'title': 'Izvješća o tržištu nekretnina Hrvatska 2025',
        'subtitle': 'Aktualne analize tržišta za sve regije Hrvatske od 123-Kroatien.eu',
        'report_label': 'Tržišno izvješće',
        'read_more': 'Pročitaj izvješće',
        'back': 'Sva izvješća',
    },
    'fr': {
        'title': 'Rapports du marché immobilier Croatie 2025',
        'subtitle': 'Analyses de marché actuelles pour toutes les régions de Croatie de 123-Kroatien.eu',
        'report_label': 'Rapport de marché',
        'read_more': 'Lire le rapport',
        'back': 'Tous les rapports',
    },
    'nl': {
        'title': 'Vastgoedmarktrapporten Kroatië 2025',
        'subtitle': 'Actuele marktanalyses voor alle regio s van Kroatië van 123-Kroatien.eu',
        'report_label': 'Marktrapport',
        'read_more': 'Rapport lezen',
        'back': 'Alle rapporten',
    },
    'pl': {
        'title': 'Raporty rynku nieruchomości Chorwacja 2025',
        'subtitle': 'Aktualne analizy rynkowe dla wszystkich regionów Chorwacji od 123-Kroatien.eu',
        'report_label': 'Raport rynkowy',
        'read_more': 'Czytaj raport',
        'back': 'Wszystkie raporty',
    },
    'cz': {
        'title': 'Zprávy o trhu nemovitostí Chorvatsko 2025',
        'subtitle': 'Aktuální tržní analýzy pro všechny regiony Chorvatska od 123-Kroatien.eu',
        'report_label': 'Tržní zpráva',
        'read_more': 'Číst zprávu',
        'back': 'Všechny zprávy',
    },
    'sk': {
        'title': 'Správy o trhu nehnuteľností Chorvátsko 2025',
        'subtitle': 'Aktuálne trhové analýzy pre všetky regióny Chorvátska od 123-Kroatien.eu',
        'report_label': 'Trhová správa',
        'read_more': 'Čítať správu',
        'back': 'Všetky správy',
    },
    'ru': {
        'title': 'Отчёты о рынке недвижимости Хорватия 2025',
        'subtitle': 'Актуальные рыночные анализы для всех регионов Хорватии от 123-Kroatien.eu',
        'report_label': 'Рыночный отчёт',
        'read_more': 'Читать отчёт',
        'back': 'Все отчёты',
    },
    'gr': {
        'title': 'Αναφορές αγοράς ακινήτων Κροατία 2025',
        'subtitle': 'Τρέχουσες αναλύσεις αγοράς για όλες τις περιοχές της Κροατίας από 123-Kroatien.eu',
        'report_label': 'Αναφορά αγοράς',
        'read_more': 'Διαβάστε την αναφορά',
        'back': 'Όλες οι αναφορές',
    },
    'sw': {
        'title': 'Fastighetsmarknadsrapporter Kroatien 2025',
        'subtitle': 'Aktuella marknadsanalyser för alla regioner i Kroatien från 123-Kroatien.eu',
        'report_label': 'Marknadsrapport',
        'read_more': 'Läs rapport',
        'back': 'Alla rapporter',
    },
    'no': {
        'title': 'Eiendomsmarkedsrapporter Kroatia 2025',
        'subtitle': 'Aktuelle markedsanalyser for alle regioner i Kroatia fra 123-Kroatien.eu',
        'report_label': 'Markedsrapport',
        'read_more': 'Les rapport',
        'back': 'Alle rapporter',
    },
}

def get_lang_from_request(request, country):
    # Session-Sprache hat Priorität
    session_lang = request.session.get('site_language')
    if session_lang:
        return session_lang
    # Fallback auf URL-Land
    lang = COUNTRY_TO_LANG.get(country)
    if lang:
        return lang
    return 'ge' 

def get_market_reports(lang='ge'):
    base_path = os.path.dirname(os.path.abspath(__file__))
    reports_dir = os.path.join(base_path, 'market_reports_data')
    reports = []
    
    if not os.path.exists(reports_dir):
        return reports
    
    for filename in os.listdir(reports_dir):
        if filename.endswith(f'_{lang}.json'):
            filepath = os.path.join(reports_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                reports.append(data)
    
    return sorted(reports, key=lambda x: x.get('region_name', ''))

def market_report_list(request, country):
    lang = get_lang_from_request(request, country)
    reports = get_market_reports(lang)
    country_name = COUNTRY_NAMES.get(lang, 'kroatien')
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ge'])
    url_paths = URL_PATHS.get(lang, URL_PATHS['ge'])
    return render(request, 'main/market_report_list.html', {
        'reports': reports,
        'country_name': country_name,
        'lang': lang,
        'trans': trans,
        'url_paths': url_paths
    })

def market_report_detail(request, country, region_slug, year):
    lang = get_lang_from_request(request, country)
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    filename = f'{region_slug}_{year}_{lang}.json'
    filepath = os.path.join(base_path, 'market_reports_data', filename)
    
    if not os.path.exists(filepath):
        raise Http404('Marktbericht nicht gefunden')
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    import markdown
    data['content_html'] = markdown.markdown(data['content'])
    country_name = COUNTRY_NAMES.get(lang, 'kroatien')
    trans = TRANSLATIONS.get(lang, TRANSLATIONS['ge'])
    url_paths = URL_PATHS.get(lang, URL_PATHS['ge'])
    return render(request, 'main/market_report_detail.html', {
        'report': data,
        'country_name': country_name,
        'lang': lang,
        'trans': trans,
        'url_paths': url_paths
    })
