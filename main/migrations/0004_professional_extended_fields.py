from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_add_extended_profile_fields'),
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
        migrations.AlterField(
            model_name='professional',
            name='specializations',
            field=models.JSONField(blank=True, default=list, verbose_name='Spezialisierungen * (mind. 1)'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Firmenname *'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='email',
            field=models.EmailField(max_length=500, verbose_name='E-Mail *'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='phone',
            field=models.CharField(max_length=50, verbose_name='Telefon *'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='city',
            field=models.CharField(max_length=200, verbose_name='Stadt *'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='address',
            field=models.CharField(max_length=500, verbose_name='Adresse *'),
        ),
        migrations.AlterField(
            model_name='professional',
            name='oib_number',
            field=models.CharField(max_length=20, verbose_name='OIB-Nummer * (intern)'),
        ),
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
        migrations.RemoveField(
            model_name='professional',
            name='languages',
        ),
    ]
