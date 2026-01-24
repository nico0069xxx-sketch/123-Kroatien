import re
from django.core.management.base import BaseCommand
from main.glossary_models import GlossaryTermTranslation, GlossaryTermAlias

class Command(BaseCommand):
    help = 'Create aliases from synonyms. Idempotent.'

    def handle(self, *args, **options):
        created = skipped = 0
        
        for trans in GlossaryTermTranslation.objects.filter(status__in=['approved', 'published']):
            for synonym in trans.synonyms or []:
                slug = re.sub(r'[^a-z0-9]+', '-', synonym.lower().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')).strip('-')
                
                if slug == trans.slug:
                    continue
                
                alias, is_new = GlossaryTermAlias.objects.get_or_create(
                    language=trans.language,
                    slug=slug,
                    defaults={'translation': trans}
                )
                if is_new:
                    created += 1
                    self.stdout.write(self.style.SUCCESS(f"+ {slug} -> {trans.slug}"))
                else:
                    skipped += 1
        
        self.stdout.write(self.style.SUCCESS(f"\nDone! Created: {created}, Skipped: {skipped}"))
