# main/glossary_views.py
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .glossary_models import (
    GlossaryTerm, GlossaryTermTranslation, GlossaryTermAlias,
    TermCategory, GLOSSARY_URLS, COUNTRY_NAMES,
)

APPROVED_STATUSES = ["approved", "published"]

GLOSSARY_TRANSLATIONS = {
    "ge": {
        "glossary_title": "Immobilien-Glossar Kroatien",
        "glossary_subtitle": "Fachbegriffe rund um den Immobilienkauf in Kroatien",
        "search_placeholder": "Begriff suchen...",
        "filter_audience": "Zielgruppe",
        "filter_topic": "Thema",
        "filter_asset_type": "Objekttyp",
        "all": "Alle",
        "learn_more": "Mehr erfahren",
        "back_to_glossary": "Zurück zum Glossar",
        "related_terms": "Verwandte Begriffe",
        "synonyms": "Auch bekannt als",
        "faq_title": "Häufige Fragen",
        "no_results": "Keine Begriffe gefunden.",
        "results_count": "Begriffe gefunden",
        "page": "Seite",
        "of": "von",
        "disclaimer_short": "Nur zur Information. Keine Rechts-, Steuer- oder Anlageberatung.",
        "investors_title": "Glossar für Investoren",
        "investors_subtitle": "Fachbegriffe für Immobilieninvestoren in Kroatien",
        "holiday_title": "Glossar für Ferienkäufer",
        "holiday_subtitle": "Fachbegriffe für Ferienimmobilien",
        "luxury_title": "Glossar für Luxusimmobilien",
        "luxury_subtitle": "Fachbegriffe für Premium-Immobilien",
        "featured_terms": "Wichtige Begriffe",
        "browse_by_topic": "Nach Thema durchsuchen",
        "categories_label": "Kategorien",
        "general_label": "Allgemein",
    },
    "en": {
        "glossary_title": "Croatia Real Estate Glossary",
        "glossary_subtitle": "Key terms for buying property in Croatia",
        "search_placeholder": "Search terms...",
        "filter_audience": "Audience",
        "filter_topic": "Topic",
        "filter_asset_type": "Property Type",
        "all": "All",
        "learn_more": "Learn more",
        "back_to_glossary": "Back to Glossary",
        "related_terms": "Related Terms",
        "synonyms": "Also known as",
        "faq_title": "Frequently Asked Questions",
        "no_results": "No terms found.",
        "results_count": "terms found",
        "page": "Page",
        "of": "of",
        "disclaimer_short": "Information only. No legal, tax, or investment advice.",
        "investors_title": "Investor Glossary",
        "investors_subtitle": "Key terms for real estate investors",
        "holiday_title": "Holiday Buyer Glossary",
        "holiday_subtitle": "Key terms for holiday properties",
        "luxury_title": "Luxury Real Estate Glossary",
        "luxury_subtitle": "Key terms for luxury properties",
        "featured_terms": "Featured Terms",
        "browse_by_topic": "Browse by Topic",
        "categories_label": "Categories",
        "general_label": "General",
    },
    "hr": {
        "glossary_title": "Pojmovnik nekretnina Hrvatske",
        "glossary_subtitle": "Ključni pojmovi za kupnju nekretnina",
        "search_placeholder": "Pretraži pojmove...",
        "filter_audience": "Ciljna skupina",
        "filter_topic": "Tema",
        "filter_asset_type": "Vrsta nekretnine",
        "all": "Sve",
        "learn_more": "Saznaj više",
        "back_to_glossary": "Natrag na pojmovnik",
        "related_terms": "Povezani pojmovi",
        "synonyms": "Poznato i kao",
        "faq_title": "Često postavljana pitanja",
        "no_results": "Pojmovi nisu pronađeni.",
        "results_count": "pojmova pronađeno",
        "page": "Stranica",
        "of": "od",
        "disclaimer_short": "Samo informativno. Bez pravnih, poreznih ili investicijskih savjeta.",
        "investors_title": "Pojmovnik za investitore",
        "investors_subtitle": "Ključni pojmovi za investitore",
        "holiday_title": "Pojmovnik za odmor",
        "holiday_subtitle": "Ključni pojmovi za odmor nekretnine",
        "luxury_title": "Pojmovnik luksuznih nekretnina",
        "luxury_subtitle": "Ključni pojmovi za luksuzne nekretnine",
        "featured_terms": "Istaknuti pojmovi",
        "browse_by_topic": "Pregledaj po temi",
        "categories_label": "Kategorije",
        "general_label": "Opće",
    },
    "fr": {
        "glossary_title": "Glossaire Immobilier Croatie",
        "glossary_subtitle": "Termes clés pour l'achat immobilier en Croatie",
        "search_placeholder": "Rechercher...",
        "filter_audience": "Public cible",
        "filter_topic": "Sujet",
        "filter_asset_type": "Type de bien",
        "all": "Tous",
        "learn_more": "En savoir plus",
        "back_to_glossary": "Retour au glossaire",
        "related_terms": "Termes associés",
        "synonyms": "Également connu sous",
        "faq_title": "Questions fréquentes",
        "no_results": "Aucun terme trouvé.",
        "results_count": "termes trouvés",
        "page": "Page",
        "of": "sur",
        "disclaimer_short": "Informations uniquement. Pas de conseils juridiques, fiscaux ou d'investissement.",
        "investors_title": "Glossaire Investisseurs",
        "investors_subtitle": "Termes clés pour les investisseurs immobiliers",
        "holiday_title": "Glossaire Vacances",
        "holiday_subtitle": "Termes clés pour les biens de vacances",
        "luxury_title": "Glossaire Luxe",
        "luxury_subtitle": "Termes clés pour l'immobilier de luxe",
        "featured_terms": "Termes en vedette",
        "browse_by_topic": "Parcourir par sujet",
        "categories_label": "Catégories",
        "general_label": "Général",
    },
    "nl": {
        "glossary_title": "Vastgoed Woordenlijst Kroatië",
        "glossary_subtitle": "Belangrijke termen voor vastgoedaankoop in Kroatië",
        "search_placeholder": "Zoeken...",
        "filter_audience": "Doelgroep",
        "filter_topic": "Onderwerp",
        "filter_asset_type": "Type vastgoed",
        "all": "Alle",
        "learn_more": "Meer informatie",
        "back_to_glossary": "Terug naar woordenlijst",
        "related_terms": "Gerelateerde termen",
        "synonyms": "Ook bekend als",
        "faq_title": "Veelgestelde vragen",
        "no_results": "Geen termen gevonden.",
        "results_count": "termen gevonden",
        "page": "Pagina",
        "of": "van",
        "disclaimer_short": "Alleen ter informatie. Geen juridisch, fiscaal of beleggingsadvies.",
        "investors_title": "Investeerders Woordenlijst",
        "investors_subtitle": "Belangrijke termen voor vastgoedinvesteerders",
        "holiday_title": "Vakantie Woordenlijst",
        "holiday_subtitle": "Belangrijke termen voor vakantiewoningen",
        "luxury_title": "Luxe Woordenlijst",
        "luxury_subtitle": "Belangrijke termen voor luxe vastgoed",
        "featured_terms": "Uitgelichte termen",
        "browse_by_topic": "Bladeren op onderwerp",
        "categories_label": "Categorieën",
        "general_label": "Algemeen",
    },
    "pl": {
        "glossary_title": "Słownik Nieruchomości Chorwacja",
        "glossary_subtitle": "Kluczowe terminy dotyczące zakupu nieruchomości w Chorwacji",
        "search_placeholder": "Szukaj...",
        "filter_audience": "Grupa docelowa",
        "filter_topic": "Temat",
        "filter_asset_type": "Typ nieruchomości",
        "all": "Wszystkie",
        "learn_more": "Dowiedz się więcej",
        "back_to_glossary": "Powrót do słownika",
        "related_terms": "Powiązane terminy",
        "synonyms": "Znany również jako",
        "faq_title": "Często zadawane pytania",
        "no_results": "Nie znaleziono terminów.",
        "results_count": "znalezionych terminów",
        "page": "Strona",
        "of": "z",
        "disclaimer_short": "Tylko informacje. Brak porad prawnych, podatkowych ani inwestycyjnych.",
        "investors_title": "Słownik dla Inwestorów",
        "investors_subtitle": "Kluczowe terminy dla inwestorów nieruchomości",
        "holiday_title": "Słownik Wakacyjny",
        "holiday_subtitle": "Kluczowe terminy dla nieruchomości wakacyjnych",
        "luxury_title": "Słownik Luksusowy",
        "luxury_subtitle": "Kluczowe terminy dla nieruchomości luksusowych",
        "featured_terms": "Wyróżnione terminy",
        "browse_by_topic": "Przeglądaj według tematu",
        "categories_label": "Kategorie",
        "general_label": "Ogólne",
    },
    "cz": {
        "glossary_title": "Glosář Nemovitostí Chorvatsko",
        "glossary_subtitle": "Klíčové pojmy pro nákup nemovitostí v Chorvatsku",
        "search_placeholder": "Hledat...",
        "filter_audience": "Cílová skupina",
        "filter_topic": "Téma",
        "filter_asset_type": "Typ nemovitosti",
        "all": "Vše",
        "learn_more": "Více informací",
        "back_to_glossary": "Zpět na glosář",
        "related_terms": "Související pojmy",
        "synonyms": "Také známý jako",
        "faq_title": "Často kladené otázky",
        "no_results": "Žádné pojmy nenalezeny.",
        "results_count": "nalezených pojmů",
        "page": "Strana",
        "of": "z",
        "disclaimer_short": "Pouze informace. Žádné právní, daňové ani investiční poradenství.",
        "investors_title": "Glosář pro Investory",
        "investors_subtitle": "Klíčové pojmy pro investory do nemovitostí",
        "holiday_title": "Glosář Dovolené",
        "holiday_subtitle": "Klíčové pojmy pro rekreační nemovitosti",
        "luxury_title": "Luxusní Glosář",
        "luxury_subtitle": "Klíčové pojmy pro luxusní nemovitosti",
        "featured_terms": "Vybrané pojmy",
        "browse_by_topic": "Procházet podle tématu",
        "categories_label": "Kategorie",
        "general_label": "Obecné",
    },
    "sk": {
        "glossary_title": "Slovník Nehnuteľností Chorvátsko",
        "glossary_subtitle": "Kľúčové pojmy pre nákup nehnuteľností v Chorvátsku",
        "search_placeholder": "Hľadať...",
        "filter_audience": "Cieľová skupina",
        "filter_topic": "Téma",
        "filter_asset_type": "Typ nehnuteľnosti",
        "all": "Všetko",
        "learn_more": "Viac informácií",
        "back_to_glossary": "Späť na slovník",
        "related_terms": "Súvisiace pojmy",
        "synonyms": "Tiež známy ako",
        "faq_title": "Často kladené otázky",
        "no_results": "Žiadne pojmy nenájdené.",
        "results_count": "nájdených pojmov",
        "page": "Strana",
        "of": "z",
        "disclaimer_short": "Len informácie. Žiadne právne, daňové ani investičné poradenstvo.",
        "investors_title": "Slovník pre Investorov",
        "investors_subtitle": "Kľúčové pojmy pre investorov do nehnuteľností",
        "holiday_title": "Slovník Dovolenky",
        "holiday_subtitle": "Kľúčové pojmy pre rekreačné nehnuteľnosti",
        "luxury_title": "Luxusný Slovník",
        "luxury_subtitle": "Kľúčové pojmy pre luxusné nehnuteľnosti",
        "featured_terms": "Vybrané pojmy",
        "browse_by_topic": "Prehľadávať podľa témy",
        "categories_label": "Kategórie",
        "general_label": "Všeobecné",
    },
    "ru": {
        "glossary_title": "Глоссарий Недвижимости Хорватия",
        "glossary_subtitle": "Ключевые термины для покупки недвижимости в Хорватии",
        "search_placeholder": "Поиск...",
        "filter_audience": "Аудитория",
        "filter_topic": "Тема",
        "filter_asset_type": "Тип недвижимости",
        "all": "Все",
        "learn_more": "Подробнее",
        "back_to_glossary": "Назад к глоссарию",
        "related_terms": "Связанные термины",
        "synonyms": "Также известен как",
        "faq_title": "Часто задаваемые вопросы",
        "no_results": "Термины не найдены.",
        "results_count": "найденных терминов",
        "page": "Страница",
        "of": "из",
        "disclaimer_short": "Только информация. Без юридических, налоговых или инвестиционных консультаций.",
        "investors_title": "Глоссарий для Инвесторов",
        "investors_subtitle": "Ключевые термины для инвесторов в недвижимость",
        "holiday_title": "Глоссарий Отдыха",
        "holiday_subtitle": "Ключевые термины для курортной недвижимости",
        "luxury_title": "Люксовый Глоссарий",
        "luxury_subtitle": "Ключевые термины для элитной недвижимости",
        "featured_terms": "Избранные термины",
        "browse_by_topic": "Просмотр по теме",
        "categories_label": "Категории",
        "general_label": "Общее",
    },
    "gr": {
        "glossary_title": "Γλωσσάριο Ακινήτων Κροατία",
        "glossary_subtitle": "Βασικοί όροι για αγορά ακινήτων στην Κροατία",
        "search_placeholder": "Αναζήτηση...",
        "filter_audience": "Κοινό",
        "filter_topic": "Θέμα",
        "filter_asset_type": "Τύπος ακινήτου",
        "all": "Όλα",
        "learn_more": "Μάθετε περισσότερα",
        "back_to_glossary": "Πίσω στο γλωσσάριο",
        "related_terms": "Σχετικοί όροι",
        "synonyms": "Επίσης γνωστό ως",
        "faq_title": "Συχνές ερωτήσεις",
        "no_results": "Δεν βρέθηκαν όροι.",
        "results_count": "όροι βρέθηκαν",
        "page": "Σελίδα",
        "of": "από",
        "disclaimer_short": "Μόνο πληροφορίες. Χωρίς νομικές, φορολογικές ή επενδυτικές συμβουλές.",
        "investors_title": "Γλωσσάριο Επενδυτών",
        "investors_subtitle": "Βασικοί όροι για επενδυτές ακινήτων",
        "holiday_title": "Γλωσσάριο Διακοπών",
        "holiday_subtitle": "Βασικοί όροι για ακίνητα διακοπών",
        "luxury_title": "Γλωσσάριο Πολυτελείας",
        "luxury_subtitle": "Βασικοί όροι για πολυτελή ακίνητα",
        "featured_terms": "Επιλεγμένοι όροι",
        "browse_by_topic": "Περιήγηση ανά θέμα",
        "categories_label": "Κατηγορίες",
        "general_label": "Γενικά",
    },
    "sw": {
        "glossary_title": "Fastighetsordlista Kroatien",
        "glossary_subtitle": "Viktiga termer för fastighetsköp i Kroatien",
        "search_placeholder": "Sök...",
        "filter_audience": "Målgrupp",
        "filter_topic": "Ämne",
        "filter_asset_type": "Fastighetstyp",
        "all": "Alla",
        "learn_more": "Läs mer",
        "back_to_glossary": "Tillbaka till ordlistan",
        "related_terms": "Relaterade termer",
        "synonyms": "Även känd som",
        "faq_title": "Vanliga frågor",
        "no_results": "Inga termer hittades.",
        "results_count": "termer hittades",
        "page": "Sida",
        "of": "av",
        "disclaimer_short": "Endast information. Ingen juridisk, skatte- eller investeringsrådgivning.",
        "investors_title": "Investerarordlista",
        "investors_subtitle": "Viktiga termer för fastighetsinvesterare",
        "holiday_title": "Semesterordlista",
        "holiday_subtitle": "Viktiga termer för semesterfastigheter",
        "luxury_title": "Lyxordlista",
        "luxury_subtitle": "Viktiga termer för lyxfastigheter",
        "featured_terms": "Utvalda termer",
        "browse_by_topic": "Bläddra efter ämne",
        "categories_label": "Kategorier",
        "general_label": "Allmänt",
    },
    "no": {
        "glossary_title": "Eiendomsordliste Kroatia",
        "glossary_subtitle": "Viktige begreper for eiendomskjøp i Kroatia",
        "search_placeholder": "Søk...",
        "filter_audience": "Målgruppe",
        "filter_topic": "Emne",
        "filter_asset_type": "Eiendomstype",
        "all": "Alle",
        "learn_more": "Les mer",
        "back_to_glossary": "Tilbake til ordlisten",
        "related_terms": "Relaterte begreper",
        "synonyms": "Også kjent som",
        "faq_title": "Ofte stilte spørsmål",
        "no_results": "Ingen begreper funnet.",
        "results_count": "begreper funnet",
        "page": "Side",
        "of": "av",
        "disclaimer_short": "Kun informasjon. Ingen juridisk, skatte- eller investeringsrådgivning.",
        "investors_title": "Investorordliste",
        "investors_subtitle": "Viktige begreper for eiendomsinvestorer",
        "holiday_title": "Ferieordliste",
        "holiday_subtitle": "Viktige begreper for ferieeiendommer",
        "luxury_title": "Luksusordliste",
        "luxury_subtitle": "Viktige begreper for luksuseiendommer",
        "featured_terms": "Utvalgte begreper",
        "browse_by_topic": "Bla etter emne",
        "categories_label": "Kategorier",
        "general_label": "Generelt",
    },

}


def get_translations(lang):
    return GLOSSARY_TRANSLATIONS.get(lang, GLOSSARY_TRANSLATIONS.get("ge", {}))


def get_glossary_base_url(lang):
    country = COUNTRY_NAMES.get(lang, "kroatien")
    glossary_segment = GLOSSARY_URLS.get(lang, "glossar")
    return f"/{lang}/{country}/{glossary_segment}/"


def glossary_index(request, lang, country):
    request.session['site_language'] = lang
    q = (request.GET.get("q") or "").strip()
    audience = request.GET.get("audience")
    topic = request.GET.get("topic")
    asset_type = request.GET.get("asset_type")
    ordering = request.GET.get("ordering") or "title"
    page = request.GET.get("page", 1)

    qs = GlossaryTermTranslation.objects.select_related("term").prefetch_related(
        "term__categories"
    ).filter(
        language=lang, term__is_published=True, status__in=APPROVED_STATUSES
    ).distinct()

    if q:
        qs = qs.filter(
            Q(title__icontains=q) | Q(short_def__icontains=q) |
            Q(long_def__icontains=q) | Q(keywords__icontains=q)
        )
    if audience:
        qs = qs.filter(term__categories__group="audience", term__categories__key=audience)
    if topic:
        qs = qs.filter(term__categories__group="topic", term__categories__key=topic)
    if asset_type:
        qs = qs.filter(term__categories__group="asset_type", term__categories__key=asset_type)

    qs = qs.order_by(ordering if ordering in ["title", "-title"] else "title")
    paginator = Paginator(qs, 30)
    page_obj = paginator.get_page(page)

    categories = TermCategory.objects.all().order_by("group", "order")
    t = get_translations(lang)

    return render(request, "glossary/index.html", {
        "lang": lang, "language": lang, "country": country, "language": lang,
        "q": q, "audience": audience, "topic": topic, "asset_type": asset_type,
        "page_obj": page_obj, "total_count": paginator.count,
        "audience_cats": categories.filter(group="audience"),
        "topic_cats": categories.filter(group="topic"),
        "asset_type_cats": categories.filter(group="asset_type"),
        "glossary_base_url": get_glossary_base_url(lang), "t": t,
    })


def glossary_detail(request, slug, lang, country):
    request.session['site_language'] = lang
    translation = GlossaryTermTranslation.objects.select_related("term").prefetch_related(
        "term__categories", "term__translations", "term__related_terms__translations"
    ).filter(
        language=lang, slug=slug, term__is_published=True, status__in=APPROVED_STATUSES
    ).first()

    if translation:
        all_translations = translation.term.translations.filter(status__in=APPROVED_STATUSES)
        hreflang_links = [{"lang": tr.language, "url": tr.get_absolute_url()} for tr in all_translations]
        category_ids = translation.term.categories.values_list("id", flat=True)
        related_terms = GlossaryTermTranslation.objects.filter(
            language=lang, term__is_published=True, status__in=APPROVED_STATUSES,
            term__categories__id__in=category_ids
        ).exclude(id=translation.id).distinct().order_by("title")[:6]
        t = get_translations(lang)
        
        # Build absolute URLs for JSON-LD
        canonical_url = request.build_absolute_uri(translation.get_absolute_url())
        glossary_index_url = request.build_absolute_uri(get_glossary_base_url(lang))
        
        # Related URLs for JSON-LD (same language, approved)
        related_urls = []
        for rel_term in translation.term.related_terms.filter(is_published=True):
            rel_trans = rel_term.translations.filter(language=lang, status__in=APPROVED_STATUSES).first()
            if not rel_trans:
                rel_trans = rel_term.translations.filter(language="ge", status__in=APPROVED_STATUSES).first()
            if rel_trans:
                related_urls.append(request.build_absolute_uri(rel_trans.get_absolute_url()))

        return render(request, "glossary/detail.html", {
            "lang": lang, "language": lang, "country": country, "language": lang,
            "term": translation, "translation": translation,
            "all_translations": all_translations,
            "hreflang_links": hreflang_links, "related_terms": related_terms,
            "glossary_base_url": get_glossary_base_url(lang), "t": t,
            "canonical_url": canonical_url,
            "glossary_index_url": glossary_index_url,
            "related_urls": related_urls,
        })

    alias = GlossaryTermAlias.objects.filter(language=lang, slug=slug).select_related("translation").first()
    if alias:
        return redirect(alias.translation.get_absolute_url(), permanent=True)

    raise Http404("Begriff nicht gefunden")


def _landing_page(request, lang, country, audience_key, template_name):
    request.session['site_language'] = lang
    featured_terms = GlossaryTermTranslation.objects.select_related("term").filter(
        language=lang, term__is_published=True, status__in=APPROVED_STATUSES,
        term__categories__group="audience", term__categories__key=audience_key
    ).distinct().order_by("title")[:24]
    topic_categories = TermCategory.objects.filter(group="topic").order_by("order")
    t = get_translations(lang)

    return render(request, template_name, {
        "lang": lang, "language": lang, "country": country, "language": lang,
        "audience_key": audience_key, "featured_terms": featured_terms,
        "topic_categories": topic_categories,
        "glossary_base_url": get_glossary_base_url(lang), "t": t,
    })


def landing_investors(request, lang, country):
    return _landing_page(request, lang, country, "investor", "glossary/landing_investors.html")


def landing_holiday(request, lang, country):
    return _landing_page(request, lang, country, "holiday-buyer", "glossary/landing_holiday.html")


def landing_luxury(request, lang, country):
    return _landing_page(request, lang, country, "luxury", "glossary/landing_luxury.html")


def disclaimer_page(request, lang, country):
    request.session['site_language'] = lang
    t = get_translations(lang)
    return render(request, "legal/disclaimer.html", {
        "lang": lang, "language": lang, "country": country, "glossary_base_url": get_glossary_base_url(lang), "t": t,
    })


def buyer_guide_page(request, lang, country):
    request.session['site_language'] = lang
    t = get_translations(lang)
    return render(request, "legal/buyer_guide.html", {
        "lang": lang, "language": lang, "country": country, "glossary_base_url": get_glossary_base_url(lang), "t": t,
    })