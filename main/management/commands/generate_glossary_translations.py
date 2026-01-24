"""
Generate glossary translations for 11 languages using Emergent LLM.
"""
import json
import asyncio
import re
from pathlib import Path
from django.core.management.base import BaseCommand
from emergentintegrations.llm.chat import LlmChat, UserMessage

EMERGENT_LLM_KEY = "sk-emergent-113674f2aA7337d756"

LANGUAGE_NAMES = {
    "en": "English",
    "hr": "Croatian",
    "fr": "French",
    "nl": "Dutch",
    "pl": "Polish",
    "cz": "Czech",
    "sk": "Slovak",
    "ru": "Russian",
    "gr": "Greek",
    "sw": "Swedish",
    "no": "Norwegian"
}

class Command(BaseCommand):
    help = 'Generate glossary translations from German source'

    def add_arguments(self, parser):
        parser.add_argument('--source', default='data/glossary/ge/glossary_all.json')
        parser.add_argument('--targets', nargs='+', default=['en','hr','fr','nl','pl','cz','sk','ru','gr','sw','no'])
        parser.add_argument('--out-root', default='data/glossary/')

    def handle(self, *args, **options):
        asyncio.run(self.async_handle(options))

    async def async_handle(self, options):
        source_path = Path(options['source'])
        out_root = Path(options['out_root'])
        targets = options['targets']

        with open(source_path, 'r', encoding='utf-8') as f:
            source_data = json.load(f)

        self.stdout.write(f"Loaded {len(source_data)} terms from {source_path}")

        for lang in targets:
            self.stdout.write(self.style.HTTP_INFO(f"\n=== Generating {lang.upper()} ({LANGUAGE_NAMES.get(lang, lang)}) ==="))
            translated = await self.translate_all(source_data, lang)
            
            out_dir = out_root / lang
            out_dir.mkdir(parents=True, exist_ok=True)
            out_file = out_dir / 'glossary_all.json'
            
            with open(out_file, 'w', encoding='utf-8') as f:
                json.dump(translated, f, ensure_ascii=False, indent=2)
            
            self.stdout.write(self.style.SUCCESS(f"Written {len(translated)} terms to {out_file}"))

    async def translate_all(self, source_data, target_lang):
        translated = []
        slugs_used = set()
        
        for idx, item in enumerate(source_data):
            self.stdout.write(f"  [{idx+1}/{len(source_data)}] {item['canonical_key']}")
            
            try:
                trans_item = await self.translate_item(item, target_lang, slugs_used)
                translated.append(trans_item)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"    Error: {e}"))
                # Fallback: keep German with target language code
                fallback = self.create_fallback(item, target_lang, slugs_used)
                translated.append(fallback)
        
        return translated

    async def translate_item(self, item, target_lang, slugs_used):
        source_trans = item['translation']
        lang_name = LANGUAGE_NAMES.get(target_lang, target_lang)
        
        prompt = f"""Translate this real estate glossary term from German to {lang_name}.

SOURCE (German):
- title: {source_trans['title']}
- short_def: {source_trans['short_def']}
- long_def: {source_trans['long_def']}
- synonyms: {json.dumps(source_trans.get('synonyms', []), ensure_ascii=False)}
- keywords: {json.dumps(source_trans.get('keywords', []), ensure_ascii=False)}

RULES:
1. short_def MUST be <= 120 characters (critical!)
2. Keep terminology professional (real estate, Croatia context)
3. No legal guarantees or promises
4. synonyms: 0-3 relevant synonyms in target language
5. keywords: 3-8 short keywords in target language
6. If term is Croatia-specific (like Kapara, OIB), explain but keep original term

RESPOND IN THIS EXACT JSON FORMAT (no extra text):
{{"title": "...", "short_def": "...", "long_def": "...", "synonyms": [...], "keywords": [...]}}"""

        chat = LlmChat(
            api_key=EMERGENT_LLM_KEY,
            session_id=f"glossary-{target_lang}-{item['canonical_key']}",
            system_message="You are a professional real estate translator. Output only valid JSON."
        ).with_model("openai", "gpt-4o")

        response = await chat.send_message(UserMessage(text=prompt))
        
        # Parse JSON from response
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in response")
        
        trans_data = json.loads(json_match.group())
        
        # Validate short_def length
        if len(trans_data.get('short_def', '')) > 120:
            trans_data['short_def'] = trans_data['short_def'][:117] + '...'
        
        # Generate unique slug
        slug = self.slugify(trans_data['title'], target_lang)
        slug = self.ensure_unique_slug(slug, slugs_used)
        slugs_used.add(slug)
        
        return {
            "canonical_key": item['canonical_key'],
            "is_published": item.get('is_published', True),
            "categories": item.get('categories', {}),
            "translation": {
                "language": target_lang,
                "title": trans_data['title'],
                "slug": slug,
                "short_def": trans_data['short_def'],
                "long_def": trans_data['long_def'],
                "synonyms": trans_data.get('synonyms', []),
                "keywords": trans_data.get('keywords', []),
                "faqs": [],
                "status": "needs_review"
            },
            "related_terms": item.get('related_terms', [])
        }

    def create_fallback(self, item, target_lang, slugs_used):
        source_trans = item['translation']
        slug = self.slugify(source_trans['title'], target_lang)
        slug = self.ensure_unique_slug(slug, slugs_used)
        slugs_used.add(slug)
        
        return {
            "canonical_key": item['canonical_key'],
            "is_published": item.get('is_published', True),
            "categories": item.get('categories', {}),
            "translation": {
                "language": target_lang,
                "title": source_trans['title'],
                "slug": slug,
                "short_def": source_trans['short_def'][:120],
                "long_def": source_trans['long_def'],
                "synonyms": [],
                "keywords": [],
                "faqs": [],
                "status": "needs_review"
            },
            "related_terms": item.get('related_terms', [])
        }

    def slugify(self, text, lang):
        text = text.lower()
        replacements = {
            'ä': 'ae', 'ö': 'oe', 'ü': 'ue', 'ß': 'ss',
            'á': 'a', 'à': 'a', 'â': 'a', 'ã': 'a',
            'é': 'e', 'è': 'e', 'ê': 'e', 'ë': 'e',
            'í': 'i', 'ì': 'i', 'î': 'i', 'ï': 'i',
            'ó': 'o', 'ò': 'o', 'ô': 'o', 'õ': 'o',
            'ú': 'u', 'ù': 'u', 'û': 'u',
            'ñ': 'n', 'ç': 'c',
            'č': 'c', 'ć': 'c', 'š': 's', 'ž': 'z', 'đ': 'd',
            'ą': 'a', 'ę': 'e', 'ł': 'l', 'ń': 'n', 'ś': 's', 'ź': 'z', 'ż': 'z',
            'ř': 'r', 'ě': 'e', 'ů': 'u', 'ý': 'y',
            'å': 'a', 'ø': 'o', 'æ': 'ae',
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(r'[^a-z0-9]+', '-', text)
        return text.strip('-')

    def ensure_unique_slug(self, slug, used):
        if slug not in used:
            return slug
        i = 2
        while f"{slug}-{i}" in used:
            i += 1
        return f"{slug}-{i}"
