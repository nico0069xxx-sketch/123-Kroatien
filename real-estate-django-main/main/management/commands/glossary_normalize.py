# main/management/commands/glossary_normalize.py
"""
Management Command: Glossar-Normalisierung

Erstellt Alias-Slugs aus Synonymen und normalisiert bestehende Slugs.

Verwendung:
    python manage.py glossary_normalize
    python manage.py glossary_normalize --dry-run
"""

from django.core.management.base import BaseCommand
from django.utils.text import slugify
from main.glossary_models import GlossaryTermTranslation, GlossaryTermAlias


class Command(BaseCommand):
    help = "Erstellt Alias-Slugs aus Synonymen der Glossar-Übersetzungen."
    
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Zeigt nur, was erstellt würde, ohne tatsächlich zu speichern."
        )
        parser.add_argument(
            "--language",
            type=str,
            help="Nur für eine bestimmte Sprache ausführen (z.B. 'ge', 'en')."
        )
    
    def handle(self, *args, **options):
        dry_run = options.get("dry_run", False)
        language_filter = options.get("language")
        
        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - Keine Änderungen werden gespeichert.\n"))
        
        # Hole alle Übersetzungen
        translations = GlossaryTermTranslation.objects.all()
        
        if language_filter:
            translations = translations.filter(language=language_filter)
            self.stdout.write(f"Filtere nach Sprache: {language_filter}\n")
        
        created_count = 0
        skipped_count = 0
        error_count = 0
        
        for translation in translations:
            synonyms = translation.synonyms or []
            
            if not synonyms:
                continue
            
            self.stdout.write(f"\n[{translation.language.upper()}] {translation.title}")
            self.stdout.write(f"  Synonyme: {synonyms}")
            
            for synonym in synonyms:
                if not synonym or not isinstance(synonym, str):
                    continue
                
                # Normalisiere Synonym zu Slug
                alias_slug = slugify(synonym)
                
                if not alias_slug:
                    self.stdout.write(self.style.WARNING(f"    Übersprungen (leerer Slug): {synonym}"))
                    skipped_count += 1
                    continue
                
                # Überspringe, wenn identisch mit Original-Slug
                if alias_slug == translation.slug:
                    self.stdout.write(f"    Übersprungen (identisch): {alias_slug}")
                    skipped_count += 1
                    continue
                
                # Prüfe, ob Alias bereits existiert
                existing_alias = GlossaryTermAlias.objects.filter(
                    language=translation.language,
                    slug=alias_slug
                ).first()
                
                if existing_alias:
                    if existing_alias.translation_id == translation.id:
                        self.stdout.write(f"    Existiert bereits: {alias_slug}")
                    else:
                        self.stdout.write(self.style.WARNING(
                            f"    Konflikt! {alias_slug} zeigt auf anderen Begriff: {existing_alias.translation.title}"
                        ))
                        error_count += 1
                    skipped_count += 1
                    continue
                
                # Prüfe, ob der Slug bereits als Haupt-Slug verwendet wird
                existing_translation = GlossaryTermTranslation.objects.filter(
                    language=translation.language,
                    slug=alias_slug
                ).first()
                
                if existing_translation:
                    self.stdout.write(self.style.WARNING(
                        f"    Übersprungen (existiert als Haupt-Slug): {alias_slug} → {existing_translation.title}"
                    ))
                    skipped_count += 1
                    continue
                
                # Erstelle Alias
                if not dry_run:
                    GlossaryTermAlias.objects.create(
                        language=translation.language,
                        slug=alias_slug,
                        translation=translation
                    )
                    self.stdout.write(self.style.SUCCESS(f"    Erstellt: {alias_slug} → {translation.slug}"))
                else:
                    self.stdout.write(self.style.SUCCESS(f"    Würde erstellen: {alias_slug} → {translation.slug}"))
                
                created_count += 1
        
        # Zusammenfassung
        self.stdout.write("\n" + "=" * 50)
        self.stdout.write(self.style.SUCCESS(f"Erstellt: {created_count}"))
        self.stdout.write(f"Übersprungen: {skipped_count}")
        if error_count:
            self.stdout.write(self.style.ERROR(f"Fehler/Konflikte: {error_count}"))
        
        if dry_run:
            self.stdout.write(self.style.WARNING("\nDRY RUN - Führe ohne --dry-run aus, um Änderungen zu speichern."))
