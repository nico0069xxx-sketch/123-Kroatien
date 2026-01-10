"""
Helper function for on-demand AI content generation in listing views.
Import this in main/views.py
"""
import json


def get_listing_content_with_ai(listing, user_language):
    """
    Get listing content for a language.
    If content doesn't exist, generate it on-demand with AI.
    Returns parsed JSON dict.
    """
    from listings.ai_content_generator import get_or_generate_json
    
    # Try to get/generate AI content
    ai_content = get_or_generate_json(listing, user_language)
    
    if ai_content:
        return ai_content
    
    # Fallback to original get_json() method
    return listing.get_json()
