import re
from urllib.parse import urlparse

from django.http import (
    HttpResponsePermanentRedirect,
    HttpResponseRedirect,
)
from django.utils.deprecation import MiddlewareMixin

from main.redirect_rule_model import RedirectRule

ABSOLUTE_URL_RE = re.compile(r"^https?://", re.IGNORECASE)

def _safe_target(target_url: str) -> str:
    if not target_url:
        return None
    target_url = target_url.strip()
    if target_url.startswith("/"):
        return target_url
    if ABSOLUTE_URL_RE.match(target_url):
        return target_url
    return None

class RedirectRegistryMiddleware(MiddlewareMixin):
    def process_request(self, request):
        try:
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

            if request.META.get("QUERY_STRING"):
                sep = "&" if "?" in target else "?"
                target = f"{target}{sep}{request.META['QUERY_STRING']}"

            if rule.status_code in (301, 308):
                return HttpResponsePermanentRedirect(target)
            return HttpResponseRedirect(target)
        except Exception:
            return None
