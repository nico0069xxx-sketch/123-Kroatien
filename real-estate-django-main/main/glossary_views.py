# main/glossary_views.py
"""
Glossar Views für Django SSR
- Index mit Suche, Filter, Pagination
- Detail mit Canonical/hreflang
- Alias 301 Redirects
- Segment-Landingpages (Investoren, Ferien, Luxus)
"""

from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404

from .glossary_models import (
    GlossaryTerm,
    GlossaryTermTranslation,
    GlossaryTermAlias,
    TermCategory,
    GLOSSARY_URLS,
    COUNTRY_NAMES,
    LANG_CHOICES,
)


# Status-Filter für veröffentlichte Inhalte
APPROVED_STATUSES = ["approved", "published"]

# UI-Übersetzungen für Glossar-Seiten
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
        "disclaimer_short": "Nur zur Information. Keine Rechts-, Steuer- oder Anlageberatung. Konsultieren Sie qualifizierte Fachleute in Kroatien.",
        # Landing Pages
        "investors_title": "Glossar für Investoren",
        "investors_subtitle": "Fachbegriffe für Immobilieninvestoren in Kroatien",
        "holiday_title": "Glossar für Ferienkäufer",
        "holiday_subtitle": "Fachbegriffe für Ferienimmobilien und touristische Vermietung",
        "luxury_title": "Glossar für Luxusimmobilien",
        "luxury_subtitle": "Fachbegriffe für Premium- und Luxusimmobilien in Kroatien",
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
        "disclaimer_short": "Information only. No legal, tax, or investment advice. Consult qualified professionals in Croatia.",
        # Landing Pages
        "investors_title": "Investor Glossary",
        "investors_subtitle": "Key terms for real estate investors in Croatia",
        "holiday_title": "Holiday Buyer Glossary",
        "holiday_subtitle": "Key terms for holiday properties and tourist rentals",
        "luxury_title": "Luxury Real Estate Glossary",
        "luxury_subtitle": "Key terms for premium and luxury properties in Croatia",
        "featured_terms": "Featured Terms",
        "browse_by_topic": "Browse by Topic",
    },
    "hr": {
        "glossary_title": "Pojmovnik nekretnina Hrvatske",
        "glossary_subtitle": "Ključni pojmovi za kupnju nekretnina u Hrvatskoj",
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
        "disclaimer_short": "Samo informativno. Bez pravnih, poreznih ili investicijskih savjeta. Konzultirajte kvalificirane stručnjake u Hrvatskoj.",
        # Landing Pages
        "investors_title": "Pojmovnik za investitore",
        "investors_subtitle": "Ključni pojmovi za investitore u nekretnine u Hrvatskoj",
        "holiday_title": "Pojmovnik za kupce odmor nekretnina",
        "holiday_subtitle": "Ključni pojmovi za odmor nekretnine i turistički najam",
        "luxury_title": "Pojmovnik luksuznih nekretnina",
        "luxury_subtitle": "Ključni pojmovi za premium i luksuzne nekretnine u Hrvatskoj",
        "featured_terms": "Istaknuti pojmovi",
        "browse_by_topic": "Pregledaj po temi",
    },
    "fr": {
        "glossary_title": "Glossaire immobilier Croatie",
        "glossary_subtitle": "Termes clés pour l'achat immobilier en Croatie",
        "search_placeholder": "Rechercher...",
        "filter_audience": "Public cible",
        "filter_topic": "Sujet",
        "filter_asset_type": "Type de bien",
        "all": "Tous",
        "learn_more": "En savoir plus",
        "back_to_glossary": "Retour au glossaire",
        "related_terms": "Termes connexes",
        "synonyms": "Aussi connu comme",
        "faq_title": "Questions fréquentes",
        "no_results": "Aucun terme trouvé.",
        "results_count": "termes trouvés",
        "page": "Page",
        "of": "sur",
        "disclaimer_short": "Information uniquement. Pas de conseil juridique, fiscal ou d'investissement.",
        "investors_title": "Glossaire investisseurs",
        "investors_subtitle": "Termes clés pour les investisseurs immobiliers en Croatie",
        "holiday_title": "Glossaire vacances",
        "holiday_subtitle": "Termes clés pour les propriétés de vacances",
        "luxury_title": "Glossaire luxe",
        "luxury_subtitle": "Termes clés pour l'immobilier de prestige en Croatie",
        "featured_terms": "Termes importants",
        "browse_by_topic": "Parcourir par sujet",
    },
}

# Fallback für nicht definierte Sprachen
def get_translations(lang: str) -> dict:
    """Gibt Übersetzungen für die Sprache zurück, mit Fallback zu Deutsch."""
    return GLOSSARY_TRANSLATIONS.get(lang, GLOSSARY_TRANSLATIONS.get("ge", {}))


def get_glossary_base_url(lang: str) -> str:
    """Gibt die Basis-URL für das Glossar in der angegebenen Sprache zurück."""
    country = COUNTRY_NAMES.get(lang, "kroatien")
    glossary_segment = GLOSSARY_URLS.get(lang, "glossar")
    return f"/{lang}/{country}/{glossary_segment}/"


# ============================================
# GLOSSAR INDEX VIEW
# ============================================

def glossary_index(request, lang, country):
    """
    Glossar-Übersichtsseite mit Suche, Filter und Pagination.
    
    Query-Parameter:
    - q: Volltext-Suche
    - audience: Filter nach Zielgruppe
    - topic: Filter nach Thema
    - asset_type: Filter nach Objekttyp
    - page: Pagination
    - ordering: Sortierung (default: title)
    """
    # Session-Sprache setzen
    request.session['site_language'] = lang
    
    # Query-Parameter
    q = (request.GET.get("q") or "").strip()
    audience = request.GET.get("audience")
    topic = request.GET.get("topic")
    asset_type = request.GET.get("asset_type")
    ordering = request.GET.get("ordering") or "title"
    page = request.GET.get("page", 1)
    
    try:
        page = int(page)
    except ValueError:
        page = 1
    
    # Basis-Query
    qs = (GlossaryTermTranslation.objects
          .select_related("term")
          .prefetch_related("term__categories")
          .filter(
              language=lang,
              term__is_published=True,
              status__in=APPROVED_STATUSES
          )
          .distinct())
    
    # Volltextsuche
    if q:
        qs = qs.filter(
            Q(title__icontains=q) |
            Q(short_def__icontains=q) |
            Q(long_def__icontains=q) |
            Q(keywords__icontains=q) |
            Q(synonyms__icontains=q)
        )
    
    # Taxonomie-Filter
    if audience:
        qs = qs.filter(
            term__categories__group="audience",
            term__categories__key=audience
        )
    if topic:
        qs = qs.filter(
            term__categories__group="topic",
            term__categories__key=topic
        )
    if asset_type:
        qs = qs.filter(
            term__categories__group="asset_type",
            term__categories__key=asset_type
        )
    
    # Sortierung
    valid_orderings = ["title", "-title", "updated_at", "-updated_at"]
    if ordering not in valid_orderings:
        ordering = "title"
    qs = qs.order_by(ordering)
    
    # Pagination
    paginator = Paginator(qs, 30)
    page_obj = paginator.get_page(page)
    
    # Taxonomien für Filter
    categories = TermCategory.objects.all().order_by("group", "order")
    audience_cats = categories.filter(group="audience")
    topic_cats = categories.filter(group="topic")
    asset_type_cats = categories.filter(group="asset_type")
    
    # Übersetzungen
    t = get_translations(lang)
    
    context = {
        "lang": lang,
        "country": country,
        "language": lang,  # für Template-Kompatibilität
        "q": q,
        "audience": audience,
        "topic": topic,
        "asset_type": asset_type,
        "ordering": ordering,
        "page_obj": page_obj,
        "total_count": paginator.count,
        "audience_cats": audience_cats,
        "topic_cats": topic_cats,
        "asset_type_cats": asset_type_cats,
        "glossary_base_url": get_glossary_base_url(lang),
        "t": t,
        # Canonical URL
        "canonical_url": f"/{lang}/{country}/{GLOSSARY_URLS.get(lang, 'glossar')}/",
    }
    
    return render(request, "glossary/index.html", context)


# ============================================
# GLOSSAR DETAIL VIEW
# ============================================

def glossary_detail(request, slug, lang, country):
    """
    Glossar-Detailseite für einen Begriff.
    
    - Zeigt den Begriff mit allen Details
    - Canonical URL & hreflang Tags
    - 301 Redirect für Aliase
    """
    # Session-Sprache setzen
    request.session['site_language'] = lang
    
    # Suche Translation
    translation = (GlossaryTermTranslation.objects
                   .select_related("term")
                   .prefetch_related("term__categories", "term__translations")
                   .filter(
                       language=lang,
                       slug=slug,
                       term__is_published=True,
                       status__in=APPROVED_STATUSES
                   )
                   .first())
    
    if translation:
        # Alle Übersetzungen für hreflang
        all_translations = translation.term.translations.filter(
            status__in=APPROVED_STATUSES
        ).select_related("term")
        
        # hreflang Links erstellen
        hreflang_links = []
        for tr in all_translations:
            tr_country = COUNTRY_NAMES.get(tr.language, "kroatien")
            tr_glossary = GLOSSARY_URLS.get(tr.language, "glossar")
            hreflang_links.append({
                "lang": tr.language,
                "url": f"/{tr.language}/{tr_country}/{tr_glossary}/{tr.slug}/",
            })
        
        # Verwandte Begriffe (gleiche Kategorien)
        category_ids = translation.term.categories.values_list("id", flat=True)
        related_terms = (GlossaryTermTranslation.objects
                        .filter(
                            language=lang,
                            term__is_published=True,
                            status__in=APPROVED_STATUSES,
                            term__categories__id__in=category_ids
                        )
                        .exclude(id=translation.id)
                        .distinct()
                        .order_by("title")[:6])
        
        # Übersetzungen
        t = get_translations(lang)
        
        context = {
            "lang": lang,
            "country": country,
            "language": lang,
            "term": translation,
            "all_translations": all_translations,
            "hreflang_links": hreflang_links,
            "related_terms": related_terms,
            "glossary_base_url": get_glossary_base_url(lang),
            "t": t,
            # SEO
            "canonical_url": translation.get_canonical_url(),
            "meta_title": translation.meta_title or f"{translation.title} | {t.get('glossary_title', 'Glossar')}",
            "meta_description": translation.meta_description or translation.short_def,
        }
        
        return render(request, "glossary/detail.html", context)
    
    # Alias-Suche für 301 Redirect
    alias = GlossaryTermAlias.objects.filter(
        language=lang,
        slug=slug
    ).select_related("translation").first()
    
    if alias:
        # 301 Permanent Redirect zur canonical URL
        canonical_url = alias.translation.get_absolute_url()
        return redirect(canonical_url, permanent=True)
    
    # Nicht gefunden
    raise Http404("Begriff nicht gefunden")


# ============================================
# SEGMENT LANDING PAGES
# ============================================

def _landing_page(request, lang, country, audience_key, template_name):
    """
    Basis-Funktion für Segment-Landingpages.
    
    Zeigt Begriffe gefiltert nach Zielgruppe mit Themen-Clustern.
    """
    # Session-Sprache setzen
    request.session['site_language'] = lang
    
    # Featured Terms für diese Zielgruppe
    featured_terms = (GlossaryTermTranslation.objects
                      .select_related("term")
                      .filter(
                          language=lang,
                          term__is_published=True,
                          status__in=APPROVED_STATUSES,
                          term__categories__group="audience",
                          term__categories__key=audience_key
                      )
                      .distinct()
                      .order_by("title")[:24])
    
    # Topic-Kategorien für Navigation
    topic_categories = TermCategory.objects.filter(
        group="topic"
    ).order_by("order")
    
    # Übersetzungen
    t = get_translations(lang)
    
    context = {
        "lang": lang,
        "country": country,
        "language": lang,
        "audience_key": audience_key,
        "featured_terms": featured_terms,
        "topic_categories": topic_categories,
        "glossary_base_url": get_glossary_base_url(lang),
        "t": t,
    }
    
    return render(request, template_name, context)


def landing_investors(request, lang, country):
    """Landing Page für Investoren."""
    return _landing_page(
        request, lang, country,
        "investor",
        "glossary/landing_investors.html"
    )


def landing_holiday(request, lang, country):
    """Landing Page für Ferienkäufer."""
    return _landing_page(
        request, lang, country,
        "holiday-buyer",
        "glossary/landing_holiday.html"
    )


def landing_luxury(request, lang, country):
    """Landing Page für Luxusimmobilien."""
    return _landing_page(
        request, lang, country,
        "luxury",
        "glossary/landing_luxury.html"
    )


# ============================================
# COMPLIANCE & TRUST PAGES
# ============================================

def disclaimer_page(request, lang, country):
    """Haftungsausschluss-Seite."""
    request.session['site_language'] = lang
    t = get_translations(lang)
    
    return render(request, "legal/disclaimer.html", {
        "lang": lang,
        "country": country,
        "language": lang,
        "glossary_base_url": get_glossary_base_url(lang),
        "t": t,
    })


def buyer_guide_page(request, lang, country):
    """Käufer-Leitfaden-Seite."""
    request.session['site_language'] = lang
    t = get_translations(lang)
    
    return render(request, "legal/buyer_guide.html", {
        "lang": lang,
        "country": country,
        "language": lang,
        "glossary_base_url": get_glossary_base_url(lang),
        "t": t,
    })
