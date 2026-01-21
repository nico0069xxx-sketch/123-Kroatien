# core/url_builders.py – localized URL builders for glossary (lang + country + segment)
from dataclasses import dataclass

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

def glossary_detail_path(lang: str, slug: str) -> str:
    country = COUNTRY_NAMES[lang]
    seg = GLOSSARY_URLS[lang]
    return f"/{lang}/{country}/{seg}/{slug}/"

def glossary_index_path(lang: str) -> str:
    country = COUNTRY_NAMES[lang]
    seg = GLOSSARY_URLS[lang]
    return f"/{lang}/{country}/{seg}/"
