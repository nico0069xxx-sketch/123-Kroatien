from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_add_extended_profile_fields'),
    ]

    operations = [
        # Add service_regions (multi-select JSON)
        migrations.AddField(
            model_name='professional',
            name='service_regions',
            field=models.JSONField(blank=True, default=list, verbose_name='Serviceregionen (Mehrfachauswahl)'),
        ),
        # Change specializations from TextField to JSONField
        migrations.AlterField(
            model_name='professional',
            name='specializations',
            field=models.JSONField(blank=True, default=list, verbose_name='Spezialisierungen (Mehrfachauswahl)'),
        ),
        # Add spoken_languages (multi-select JSON)
        migrations.AddField(
            model_name='professional',
            name='spoken_languages',
            field=models.JSONField(blank=True, default=list, verbose_name='Gesprochene Sprachen (Mehrfachauswahl)'),
        ),
        # Add opening_hours (JSON for each day)
        migrations.AddField(
            model_name='professional',
            name='opening_hours',
            field=models.JSONField(blank=True, default=dict, verbose_name='Öffnungszeiten'),
        ),
        # Update region choices (old field remains for backward compatibility)
        migrations.AlterField(
            model_name='professional',
            name='region',
            field=models.CharField(
                blank=True,
                choices=[
                    ('istrien', 'Istrien'),
                    ('kvarner', 'Kvarner Bucht'),
                    ('norddalmatien', 'Norddalmatien'),
                    ('mitteldalmatien', 'Mitteldalmatien'),
                    ('sueddalmatien', 'Süddalmatien'),
                    ('zagreb', 'Stadt Zagreb'),
                    ('zagreber_umland', 'Zagreber Umland'),
                    ('nordkroatien', 'Nordkroatien (Varaždin & Međimurje)'),
                    ('slawonien', 'Slawonien'),
                    ('zentralkroatien', 'Zentralkroatien (Karlovac & Sisak)'),
                    ('lika', 'Lika'),
                    ('gorski_kotar', 'Gorski Kotar'),
                ],
                max_length=50,
                null=True
            ),
        ),
    ]
