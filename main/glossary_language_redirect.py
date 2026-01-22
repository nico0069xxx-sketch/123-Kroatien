"""
Glossary language redirect helper.
Redirects to equivalent glossary page in target language.
"""
from django.shortcuts import redirect
from django.http import Http404
from .glossary_models import (
    GlossaryTermTranslation, 
    COUNTRY_NAMES, 
    GLOSSARY_URLS
)

def glossary_switch_language(request, target_lang):
    """
    Smart language switch for glossary pages.
    Detects current page type and redirects to equivalent in target language.
    """
    current_path = request.GET.get('next', '/')
    
    # Parse current path to detect glossary page
    parts = current_path.strip('/').split('/')
    
    if len(parts) >= 3:
        source_lang = parts[0]
        source_country = parts[1]
        source_segment = parts[2]
        slug = parts[3] if len(parts) > 3 else None
        
        # Check if this is a glossary page
        if source_segment in GLOSSARY_URLS.values():
            target_country = COUNTRY_NAMES.get(target_lang, 'croatia')
            target_segment = GLOSSARY_URLS.get(target_lang, 'glossary')
            
            if slug:
                # Detail page - find equivalent translation
                try:
                    source_trans = GlossaryTermTranslation.objects.select_related('term').get(
                        language=source_lang,
                        slug=slug,
                        status__in=['approved', 'published']
                    )
                    target_trans = GlossaryTermTranslation.objects.filter(
                        term=source_trans.term,
                        language=target_lang,
                        status__in=['approved', 'published']
                    ).first()
                    
                    if target_trans:
                        return redirect(f'/{target_lang}/{target_country}/{target_segment}/{target_trans.slug}/')
                except GlossaryTermTranslation.DoesNotExist:
                    pass
                
                # Fallback to index if translation not found
                return redirect(f'/{target_lang}/{target_country}/{target_segment}/')
            else:
                # Index page
                return redirect(f'/{target_lang}/{target_country}/{target_segment}/')
    
    # Fallback: go to target language homepage
    target_country = COUNTRY_NAMES.get(target_lang, 'croatia')
    return redirect(f'/{target_lang}/{target_country}/')
