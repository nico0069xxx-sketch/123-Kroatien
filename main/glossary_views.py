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
        "lang": lang, "country": country, "language": lang,
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
        "term__categories", "term__translations"
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

        return render(request, "glossary/detail.html", {
            "lang": lang, "country": country, "language": lang,
            "term": translation, "all_translations": all_translations,
            "hreflang_links": hreflang_links, "related_terms": related_terms,
            "glossary_base_url": get_glossary_base_url(lang), "t": t,
            "canonical_url": translation.get_absolute_url(),
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
        "lang": lang, "country": country, "language": lang,
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
        "lang": lang, "country": country, "glossary_base_url": get_glossary_base_url(lang), "t": t,
    })


def buyer_guide_page(request, lang, country):
    request.session['site_language'] = lang
    t = get_translations(lang)
    return render(request, "legal/buyer_guide.html", {
        "lang": lang, "country": country, "glossary_base_url": get_glossary_base_url(lang), "t": t,
    })