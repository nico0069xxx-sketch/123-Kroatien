"""
2-Pass Import: Terms + Translations first, then related_terms resolution.
"""
import json
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from main.glossary_models import GlossaryTerm, GlossaryTermTranslation, TermCategory

class Command(BaseCommand):
    help = 'Import glossary from JSON (2-pass: terms, then relations)'

    def add_arguments(self, parser):
        parser.add_argument('json_files', nargs='+', type=str)
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        all_items = []
        
        for json_file in options['json_files']:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                all_items.extend(data if isinstance(data, list) else [data])
            self.stdout.write(f"Loaded: {json_file}")
        
        # Validation
        errors = []
        for item in all_items:
            key = item.get('canonical_key', '?')
            trans = item.get('translation', {})
            if len(trans.get('short_def', '')) > 120:
                errors.append(f"[{key}] short_def > 120 chars")
        
        if errors:
            for e in errors:
                self.stdout.write(self.style.ERROR(e))
            raise CommandError(f"{len(errors)} validation error(s)")
        
        if dry_run:
            self.stdout.write(self.style.SUCCESS(f"[DRY-RUN] {len(all_items)} terms valid."))
            return
        
        # PASS 1: Create/update terms and translations
        self.stdout.write(self.style.HTTP_INFO("\n=== PASS 1: Terms & Translations ==="))
        created = updated = 0
        related_map = {}  # canonical_key -> [related_keys]
        
        with transaction.atomic():
            for item in all_items:
                term, is_new = GlossaryTerm.objects.update_or_create(
                    canonical_key=item['canonical_key'],
                    defaults={'is_published': item.get('is_published', True)}
                )
                created += is_new
                updated += not is_new
                
                # Categories
                for group, keys in item.get('categories', {}).items():
                    for key in keys:
                        try:
                            term.categories.add(TermCategory.objects.get(group=group, key=key))
                        except TermCategory.DoesNotExist:
                            pass
                
                # Translation
                trans = item.get('translation', {})
                if trans:
                    GlossaryTermTranslation.objects.update_or_create(
                        term=term, language=trans.get('language', 'ge'),
                        defaults={
                            'title': trans.get('title', ''),
                            'slug': trans.get('slug', ''),
                            'short_def': trans.get('short_def', ''),
                            'long_def': trans.get('long_def', ''),
                            'synonyms': trans.get('synonyms', []),
                            'keywords': trans.get('keywords', []),
                            'faqs': trans.get('faqs', []),
                            'status': trans.get('status', 'approved'),
                        }
                    )
                
                # Store related_terms for pass 2
                if item.get('related_terms'):
                    related_map[item['canonical_key']] = item['related_terms']
                
                self.stdout.write(f"{'+ ' if is_new else '= '}{item['canonical_key']}")
        
        self.stdout.write(self.style.SUCCESS(f"Pass 1 done: Created {created}, Updated {updated}"))
        
        # PASS 2: Resolve related_terms
        self.stdout.write(self.style.HTTP_INFO("\n=== PASS 2: Related Terms ==="))
        linked = 0
        missing = []
        
        with transaction.atomic():
            for canonical_key, related_keys in related_map.items():
                try:
                    term = GlossaryTerm.objects.get(canonical_key=canonical_key)
                    for rel_key in related_keys:
                        try:
                            related_term = GlossaryTerm.objects.get(canonical_key=rel_key)
                            term.related_terms.add(related_term)
                            linked += 1
                        except GlossaryTerm.DoesNotExist:
                            missing.append(f"{canonical_key} -> {rel_key}")
                except GlossaryTerm.DoesNotExist:
                    pass
        
        self.stdout.write(self.style.SUCCESS(f"Pass 2 done: {linked} relations linked"))
        if missing:
            self.stdout.write(self.style.WARNING(f"Missing targets: {len(missing)}"))
            for m in missing[:10]:
                self.stdout.write(f"  ! {m}")
