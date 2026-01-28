"""
Image Optimization Template Tags für 123-Kroatien.eu
Fügt Lazy Loading und Performance-Attribute zu Bildern hinzu.

Verwendung im Template:
{% load image_optimization %}
{{ image_url|lazy_img:"Alt Text" }}
"""

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def lazy_img(src, alt="", css_class="img-fluid", width="", height=""):
    """
    Generiert ein optimiertes img-Tag mit Lazy Loading.
    
    Verwendung:
    {% lazy_img "/static/images/photo.jpg" "Beschreibung" "img-fluid w-100" %}
    """
    attrs = [
        f'src="{src}"',
        f'alt="{alt}"',
        'loading="lazy"',
        'decoding="async"',
    ]
    
    if css_class:
        attrs.append(f'class="{css_class}"')
    if width:
        attrs.append(f'width="{width}"')
    if height:
        attrs.append(f'height="{height}"')
    
    img_tag = f'<img {" ".join(attrs)}>'
    return mark_safe(img_tag)


@register.filter(name='add_lazy')
def add_lazy_loading(html_content):
    """
    Fügt loading="lazy" zu allen img-Tags in einem HTML-String hinzu.
    
    Verwendung:
    {{ content|add_lazy }}
    """
    if not html_content:
        return html_content
    
    import re
    
    def add_lazy_attr(match):
        img_tag = match.group(0)
        if 'loading=' not in img_tag:
            # Füge lazy loading vor dem schließenden > ein
            return img_tag.replace('>', ' loading="lazy" decoding="async">', 1)
        return img_tag
    
    result = re.sub(r'<img[^>]+>', add_lazy_attr, str(html_content))
    return mark_safe(result)


@register.simple_tag
def responsive_img(src, alt="", sizes="100vw"):
    """
    Generiert ein responsives Bild mit srcset (falls verschiedene Größen verfügbar).
    
    Verwendung:
    {% responsive_img "/media/photos/villa.jpg" "Villa am Meer" "(max-width: 768px) 100vw, 50vw" %}
    """
    # Basis-Implementation ohne srcset (kann erweitert werden wenn verschiedene Bildgrößen verfügbar)
    img_tag = f'''<img 
        src="{src}" 
        alt="{alt}"
        loading="lazy"
        decoding="async"
        class="img-fluid"
        sizes="{sizes}"
    >'''
    return mark_safe(img_tag)


@register.inclusion_tag('include/optimized_image.html')
def optimized_image(src, alt="", css_class="img-fluid", placeholder=True):
    """
    Zeigt ein optimiertes Bild mit optionalem Placeholder.
    
    Verwendung:
    {% optimized_image listing.photo_main.url listing.property_title "img-fluid w-100" %}
    """
    return {
        'src': src,
        'alt': alt,
        'css_class': css_class,
        'placeholder': placeholder,
    }
