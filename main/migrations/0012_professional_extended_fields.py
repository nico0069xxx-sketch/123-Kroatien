from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_lead'),
    ]

    operations = [
        migrations.AddField(
            model_name='professional',
            name='service_regions',
            field=models.JSONField(blank=True, default=list, verbose_name='Serviceregionen * (mind. 1)'),
        ),
        migrations.AddField(
            model_name='professional',
            name='spoken_languages',
            field=models.JSONField(blank=True, default=list, verbose_name='Sprachen * (mind. 1)'),
        ),
        migrations.AddField(
            model_name='professional',
            name='opening_hours',
            field=models.JSONField(blank=True, default=dict, verbose_name='Öffnungszeiten'),
        ),
    ]
