# main/views_404.py
"""
Smart 404 Handler - Hilfreiche 404-Seite mit Suchfunktion und Vorschlägen.
"""
from django.shortcuts import render
from main.glossary_models import GlossaryTermTranslation


def smart_404_handler(request, exception=None):
    """
    Custom 404 Handler.
    - Zeigt hilfreiche Fehlermeldung
    - Bietet Suchfunktion
    - Schlägt ähnliche Begriffe vor
    - Setzt noindex,follow Meta-Tag
    """
    # Sprache aus Session oder URL ermitteln
    lang = request.session.get('site_language', 'ge')
    
    # Versuche ähnliche Glossar-Begriffe zu finden
    path_parts = request.path.strip('/').split('/')
    search_term = path_parts[-1] if path_parts else ''
    
    suggestions = []
    if search_term and len(search_term) > 2:
        suggestions = (GlossaryTermTranslation.objects
            .filter(
                language=lang,
                term__is_published=True,
                title__icontains=search_term
            )
            .select_related('term')[:5])
    
    context = {
        'path': request.path,
        'search_term': search_term,
        'suggestions': suggestions,
        'language': lang,
    }
    
    response = render(request, 'errors/404.html', context)
    response.status_code = 404
    return response