#!/usr/bin/env python3
"""
NEWS-EINORDNUNG MODUL - KÖNIGSKLASSE EDITION
Transformiert Immobilien-News in neutrale, KI-zitierbare Analysen für 123-Kroatien.
RSS-Feed → KI-Analyse → SEO-optimierter Content
"""

import os
import json
import feedparser
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Sprach-Konfiguration
LANGUAGES = {
    'ge': {'instruction': 'Schreibe auf Deutsch.', 'country': 'kroatien'},
    'en': {'instruction': 'Write in English.', 'country': 'croatia'},
    'fr': {'instruction': 'Écris en français.', 'country': 'croatie'},
    'hr': {'instruction': 'Piši na hrvatskom.', 'country': 'hrvatska'},
    'gr': {'instruction': 'Γράψε στα ελληνικά.', 'country': 'kroatia'},
    'pl': {'instruction': 'Pisz po polsku.', 'country': 'chorwacja'},
    'cz': {'instruction': 'Piš česky.', 'country': 'chorvatsko'},
    'ru': {'instruction': 'Пиши по-русски.', 'country': 'horvatiya'},
    'sw': {'instruction': 'Skriv på svenska.', 'country': 'kroatien'},
    'no': {'instruction': 'Skriv på norsk.', 'country': 'kroatia'},
    'sk': {'instruction': 'Píš po slovensky.', 'country': 'chorvatsko'},
    'nl': {'instruction': 'Schrijf in het Nederlands.', 'country': 'kroatie'},
}

# Beispiel RSS-Feeds für Kroatien Immobilien/Wirtschaft
RSS_FEEDS = [
    'https://www.total-croatia-news.com/feed',
    'https://www.croatiaweek.com/feed/',
]

# =============================================================================
# MASTER-PROMPT: NEWS-EINORDNUNG (KÖNIGSKLASSE)
# =============================================================================

NEWS_ANALYSIS_PROMPT = """You are a real-estate news analyst
specialized in the Croatian property market.

Your task is to transform a news article
into a NEUTRAL, VALUE-ADDING, AI-CITABLE contextual analysis
for the portal 123-Kroatien.

The output must NOT duplicate the original article.

The content must be suitable for:
- SEO publication
- AI citation
- chatbot answers
- editorial curation

------------------------------------------------
LANGUAGE HANDLING
------------------------------------------------

{lang_instruction}

- Do NOT translate the article word-by-word.
- Summarize and contextualize it for the Croatian real estate market.
- The brand name "123-kroatien.eu" must NOT be translated.

------------------------------------------------
STRUCTURE (MANDATORY - FOLLOW EXACTLY)
------------------------------------------------

**[Create a clear headline describing the implication for real estate in Croatia]**

**Was ist passiert?**
[2-3 sentences: Neutral summary of the news]

**Warum ist das wichtig für den kroatischen Immobilienmarkt?**
[Direct relevance, affected stakeholders]

**Regionale Auswirkungen**
[Which regions or buyer groups may be affected]

**Praktische Konsequenzen**
[What buyers, sellers or investors should consider]

**Kernpunkte**
• [Factual takeaway 1]
• [Factual takeaway 2]
• [Factual takeaway 3]

**Quellenhinweis:** Basierend auf öffentlich verfügbaren Informationen.

**Letztes Update: {month_year}**

------------------------------------------------
STRICT RULES
------------------------------------------------

- No copied sentences from the original
- No opinions or speculation
- No marketing language
- No calls to action
- No mention of the original publisher by name
- Neutral, fact-based analysis only
- Focus on implications for real estate market

------------------------------------------------
OUTPUT FORMAT
------------------------------------------------

- Plain text with ** for headings
- Use • for bullet points
- No HTML tags
- Clear paragraph separation

------------------------------------------------
ORIGINAL ARTICLE TO ANALYZE:
------------------------------------------------

Title: {article_title}

Content:
{article_content}

------------------------------------------------
BEGIN ANALYSIS NOW
------------------------------------------------"""


def fetch_rss_articles(feed_url, max_articles=5):
    """
    Lädt Artikel aus einem RSS-Feed.
    
    Args:
        feed_url: URL des RSS-Feeds
        max_articles: Maximale Anzahl Artikel
    
    Returns:
        Liste von Artikeln mit title, content, link, published
    """
    try:
        feed = feedparser.parse(feed_url)
        articles = []
        
        for entry in feed.entries[:max_articles]:
            article = {
                'title': entry.get('title', ''),
                'content': entry.get('summary', entry.get('description', '')),
                'link': entry.get('link', ''),
                'published': entry.get('published', ''),
            }
            articles.append(article)
        
        return articles
        
    except Exception as e:
        print(f"Fehler beim Laden des RSS-Feeds: {e}")
        return []


def analyze_news_article(article_title, article_content, language='ge'):
    """
    Analysiert einen News-Artikel und erstellt eine KI-Einordnung.
    
    Args:
        article_title: Titel des Artikels
        article_content: Inhalt des Artikels
        language: Zielsprache
    
    Returns:
        dict mit 'content', 'slug', 'url'
    """
    lang_config = LANGUAGES.get(language)
    if not lang_config:
        raise ValueError(f"Unbekannte Sprache: {language}")
    
    month_year = datetime.now().strftime('%B %Y')
    
    prompt = NEWS_ANALYSIS_PROMPT.format(
        lang_instruction=lang_config['instruction'],
        article_title=article_title,
        article_content=article_content[:2000],  # Begrenzen
        month_year=month_year
    )
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a professional real estate news analyst."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        
        # Slug aus erstem Absatz generieren
        first_line = content.split('\n')[0].replace('**', '').strip()
        slug = first_line[:50].lower()
        slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug)
        slug = slug.strip().replace(' ', '-')
        
        # URL generieren
        date_slug = datetime.now().strftime('%Y-%m-%d')
        url = f"https://123-kroatien.eu/{language}/{lang_config['country']}/news/{date_slug}-{slug}/"
        
        return {
            'content': content,
            'slug': slug,
            'url': url,
            'original_title': article_title,
            'language': language,
            'generated_at': datetime.now().isoformat(),
        }
        
    except Exception as e:
        print(f"Fehler bei News-Analyse: {e}")
        return None


def analyze_article_all_languages(article_title, article_content):
    """Analysiert einen Artikel in allen 12 Sprachen."""
    analyses = {}
    
    for lang_code in LANGUAGES.keys():
        print(f"  🌍 {lang_code}...", end=" ")
        analysis = analyze_news_article(article_title, article_content, lang_code)
        
        if analysis:
            analyses[lang_code] = analysis
            print("✅")
        else:
            print("❌")
        
        import time
        time.sleep(1)
    
    return analyses


def process_rss_feed(feed_url, max_articles=3, language='ge'):
    """
    Verarbeitet einen RSS-Feed und erstellt Analysen.
    
    Args:
        feed_url: URL des RSS-Feeds
        max_articles: Anzahl Artikel
        language: Zielsprache
    
    Returns:
        Liste von Analysen
    """
    print(f"\n📡 Lade RSS-Feed: {feed_url}")
    articles = fetch_rss_articles(feed_url, max_articles)
    
    analyses = []
    for i, article in enumerate(articles):
        print(f"\n📰 Artikel {i+1}/{len(articles)}: {article['title'][:50]}...")
        
        analysis = analyze_news_article(
            article['title'], 
            article['content'], 
            language
        )
        
        if analysis:
            analysis['original_link'] = article['link']
            analyses.append(analysis)
            print("  ✅ Analysiert")
        else:
            print("  ❌ Fehler")
        
        import time
        time.sleep(1)
    
    return analyses


# =============================================================================
# DEMO / TEST
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("📰 NEWS-EINORDNUNG - KÖNIGSKLASSE TEST")
    print("=" * 60)
    
    # Test mit einem Beispiel-Artikel
    test_article = {
        'title': 'Croatia Tourism Numbers Reach Record High in 2024',
        'content': '''Croatia welcomed over 21 million tourists in 2024, 
        marking a new record for the country. The coastal regions of Dalmatia 
        and Istria saw the highest visitor numbers. Hotel occupancy rates 
        exceeded 85% during peak season. The government announced plans to 
        invest in sustainable tourism infrastructure. Real estate experts 
        note increased interest from foreign investors in vacation properties.'''
    }
    
    print(f"\n📄 Test-Artikel: {test_article['title']}")
    print("-" * 40)
    
    analysis = analyze_news_article(
        test_article['title'], 
        test_article['content'], 
        'ge'
    )
    
    if analysis:
        print(f"\n✅ URL: {analysis['url']}\n")
        print(analysis['content'])
    else:
        print("❌ Fehler")
