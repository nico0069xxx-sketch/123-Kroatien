# core/middleware/redirect_registry_middleware.py
import re
from urllib.parse import urlparse

from django.http import (
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.utils.deprecation import MiddlewareMixin

from core.models import RedirectRule  # adjust import location

ABSOLUTE_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

def _safe_target(target_url: str) -> str | None:
    """Prevent open redirects.
    Allow:
      - relative paths starting with '/'
      - absolute http/https URLs to same host is ideal, but if you must allow
        external, restrict by allowlist (not implemented here).
    """
    if not target_url:
        return None
    target_url = target_url.strip()
    if target_url.startswith("/"):
        return target_url
    if ABSOLUTE_URL_RE.match(target_url):
        # If you want to restrict to same-domain only, uncomment host check:
        # parsed = urlparse(target_url)
        # if parsed.netloc not in {"your-domain.tld", "www.your-domain.tld"}:
        #     return None
        return target_url
    return None

class RedirectRegistryMiddleware(MiddlewareMixin):
    """Resolve exact-match redirects early and safely.

    Recommended placement:
    - very early in MIDDLEWARE (after SecurityMiddleware), so we avoid
      expensive view work for known legacy URLs.
    """

    def process_request(self, request):
        path = request.path
        rule = (RedirectRule.objects
                .filter(is_active=True, source_path=path)
                .only("target_url", "status_code")
                .first())
        if not rule:
            return None

        target = _safe_target(rule.target_url)
        if not target:
            return None

        # Preserve querystring
        if request.META.get("QUERY_STRING"):
            sep = "&" if "?" in target else "?"
            target = f"{target}{sep}{request.META['QUERY_STRING']}"

        if rule.status_code in (301, 308):
            return HttpResponsePermanentRedirect(target)
        return HttpResponseRedirect(target)
