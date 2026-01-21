import json
from django.core.management.base import BaseCommand, CommandError
from main.glossary_models import TermCategory

class Command(BaseCommand):
    help = 'Seed TermCategory from JSON taxonomy file. Idempotent.'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str)

    def handle(self, *args, **options):
        with open(options['json_file'], 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        taxonomies = data.get('taxonomies', [])
        created = updated = 0
        
        for tax in taxonomies:
            cat, cat_created = TermCategory.objects.update_or_create(
                group=tax['group'],
                key=tax['key'],
                defaults={'label': tax.get('label', tax['key']), 'order': tax.get('order', 0)}
            )
            if cat_created:
                created += 1
                self.stdout.write(self.style.SUCCESS(f"+ {tax['group']}/{tax['key']}"))
            else:
                updated += 1
        
        self.stdout.write(self.style.SUCCESS(f"\nDone! Created: {created}, Updated: {updated}"))
