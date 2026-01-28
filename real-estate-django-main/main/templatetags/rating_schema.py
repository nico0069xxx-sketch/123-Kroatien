"""
Review/Rating Template Tags für 123-Kroatien.eu
Ermöglicht AggregateRating Schema wenn Bewertungen vorhanden sind.

Verwendung im Template:
{% load rating_schema %}
{% rating_schema professional %}
{% aggregate_rating_json professional %}
"""

from django import template
from django.utils.safestring import mark_safe
import json

register = template.Library()


@register.simple_tag
def rating_schema_json(obj, obj_type="RealEstateAgent"):
    """
    Generiert JSON-LD für AggregateRating wenn Bewertungen vorhanden sind.
    
    Verwendung:
    {% rating_schema_json professional "RealEstateAgent" %}
    {% rating_schema_json listing "RealEstateListing" %}
    """
    # Prüfen ob das Objekt Bewertungen hat
    rating_value = getattr(obj, 'average_rating', None)
    review_count = getattr(obj, 'review_count', None)
    
    # Falls keine Bewertungen, leeres String zurückgeben
    if not rating_value or not review_count:
        return ''
    
    schema = {
        "@context": "https://schema.org",
        "@type": obj_type,
        "name": getattr(obj, 'name', getattr(obj, 'title', str(obj))),
        "aggregateRating": {
            "@type": "AggregateRating",
            "ratingValue": str(rating_value),
            "bestRating": "5",
            "worstRating": "1",
            "ratingCount": str(review_count)
        }
    }
    
    script_tag = f'<script type="application/ld+json">{json.dumps(schema, ensure_ascii=False)}</script>'
    return mark_safe(script_tag)


@register.inclusion_tag('include/star_rating.html')
def star_rating(rating, max_rating=5):
    """
    Zeigt Sterne-Bewertung an.
    
    Verwendung:
    {% star_rating professional.average_rating %}
    {% star_rating 4.5 %}
    """
    if rating is None:
        rating = 0
    
    full_stars = int(rating)
    half_star = 1 if rating - full_stars >= 0.5 else 0
    empty_stars = max_rating - full_stars - half_star
    
    return {
        'full_stars': range(full_stars),
        'half_star': half_star,
        'empty_stars': range(empty_stars),
        'rating': rating,
        'max_rating': max_rating,
    }


# Hilfsfunktion für zukünftige Review-Implementierung
def generate_review_schema(reviews):
    """
    Generiert Schema für individuelle Reviews.
    Kann später verwendet werden wenn Review-System implementiert wird.
    """
    review_list = []
    for review in reviews:
        review_list.append({
            "@type": "Review",
            "author": {
                "@type": "Person",
                "name": review.get('author_name', 'Anonymous')
            },
            "datePublished": review.get('date', ''),
            "reviewBody": review.get('text', ''),
            "reviewRating": {
                "@type": "Rating",
                "ratingValue": str(review.get('rating', 5)),
                "bestRating": "5",
                "worstRating": "1"
            }
        })
    return review_list
