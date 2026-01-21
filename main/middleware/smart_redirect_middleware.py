# core/middleware/smart_redirect_middleware.py
Smart redirect resolver to avoid dead ends while keeping correct HTTP status codes.

Purpose:
- If a request would otherwise return 404, attempt deterministic redirects:
  1) Glossary alias slugs -> canonical glossary term (301)
  2) (Optional extension) a generic RedirectRule table for legacy URLs

Notes:
- This middleware MUST NOT turn unknown URLs into 200 OK.
- It only redirects when an unambiguous target exists.

import re
from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

from glossary.models import GlossaryTermAlias

# IMPORTANT: Keep these mappings aligned with your existing context_processors.py
COUNTRY_NAMES = {
    "ge": "kroatien", "en": "croatia", "hr": "hrvatska", "fr": "croatie",
    "nl": "kroatie", "pl": "chorwacja", "cz": "chorvatsko", "sk": "chorvatsko",
    "ru": "horvatiya", "gr": "kroatia", "sw": "kroatien", "no": "kroatia",
}

GLOSSARY_URLS = {
    "ge": "glossar",
    "en": "glossary",
    "hr": "pojmovnik",
    "fr": "glossaire",
    "nl": "woordenlijst",
    "pl": "slownik",
    "cz": "glosar",
    "sk": "slovnik",
    "ru": "glossarij",
    "gr": "glossari",
    "sw": "ordlista",
    "no": "ordliste",
}

# Regex matches: /{lang}/{country}/{segment}/{slug}/
# Example: /ge/kroatien/glossar/alter-slug/
GLOSSARY_DETAIL_RE = re.compile(r"^/(?P<lang>[a-z]{2})/(?P<country>[a-z\-]+)/(?P<segment>[a-z\-]+)/(?P<slug>[a-z0-9\-]+)/$")


class SmartRedirectMiddleware(MiddlewareMixin):
    """Resolve deterministic redirects on 404 responses.

    Current implementation:
    - Glossary alias slugs per language -> canonical translation slug (301)
    """

    def process_response(self, request, response):
        # Only act on 404
        if getattr(response, "status_code", None) != 404:
            return response

        path = request.path
        m = GLOSSARY_DETAIL_RE.match(path)
        if not m:
            return response

        lang = m.group("lang")
        country = m.group("country")
        segment = m.group("segment")
        slug = m.group("slug")

        # Validate language + localized country + glossary segment
        if lang not in COUNTRY_NAMES:
            return response
        if country != COUNTRY_NAMES.get(lang):
            return response
        if segment != GLOSSARY_URLS.get(lang):
            return response

        # Resolve alias
        alias = (GlossaryTermAlias.objects
                 .select_related("translation")
                 .filter(language=lang, slug=slug)
                 .first())
        if not alias or not getattr(alias, "translation", None):
            return response

        target_slug = alias.translation.slug
        if not target_slug:
            return response

        target_path = f"/{lang}/{country}/{segment}/{target_slug}/"
        # Preserve querystring
        if request.META.get("QUERY_STRING"):
            target_path = f"{target_path}?{request.META['QUERY_STRING']}"

        return HttpResponsePermanentRedirect(target_path)
