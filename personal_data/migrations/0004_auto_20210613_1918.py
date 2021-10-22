# Generated by Django 3.1.4 on 2021-06-13 17:18

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0002_auto_20210613_1918'),
        ('personal_data', '0003_firefighter_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='firefighter',
            name='picture',
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='categories',
            field=models.ManyToManyField(help_text='Select a vehicle categories the driver licenses covers', to='personal_data.CategoryOfDriverLicense', verbose_name='Führerscheinklassen'),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='expiration_date',
            field=models.DateField(verbose_name='Ablaufdatum'),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='issue_date',
            field=models.DateField(verbose_name='Ausstellungsdatum'),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='license_id',
            field=models.CharField(max_length=11, verbose_name='Führerscheinnummer'),
        ),
        migrations.AlterField(
            model_name='driverlicense',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Einsatzkraft'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='active_since',
            field=models.DateField(default=django.utils.timezone.now, verbose_name='Aktiv seit'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='city',
            field=models.CharField(max_length=100, verbose_name='Stadt'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='date_of_birth',
            field=models.DateField(verbose_name='Geburtsdatum'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='joined',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='Mitglied seit'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='key',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to='equipment.key', verbose_name='Schlüssel'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='locker',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to='equipment.locker', verbose_name='Spint'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='pager',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='owner', to='equipment.pager', verbose_name='Melder'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='phone_number',
            field=models.CharField(max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Telefonnummer'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='staff_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Personalnummer'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='street',
            field=models.CharField(max_length=200, verbose_name='Straße'),
        ),
        migrations.AlterField(
            model_name='firefighter',
            name='zip',
            field=models.IntegerField(verbose_name='Postleitzahl'),
        ),
        migrations.AlterField(
            model_name='honorassignment',
            name='firefighter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Einsatzkraft'),
        ),
        migrations.AlterField(
            model_name='honorassignment',
            name='honor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_data.honor', verbose_name='Ehrung'),
        ),
        migrations.AlterField(
            model_name='honorassignment',
            name='issue_date',
            field=models.DateField(verbose_name='Ausstellungsdatum'),
        ),
        migrations.AlterField(
            model_name='honorassignment',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_data.authority', verbose_name='Ausgebende Behörde'),
        ),
        migrations.AlterField(
            model_name='rankassignment',
            name='firefighter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ranks', to=settings.AUTH_USER_MODEL, verbose_name='Einsatzkraft'),
        ),
        migrations.AlterField(
            model_name='rankassignment',
            name='issue_date',
            field=models.DateField(verbose_name='Ausstellungsdatum'),
        ),
        migrations.AlterField(
            model_name='rankassignment',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_data.authority', verbose_name='Ausgebende Behörde'),
        ),
        migrations.AlterField(
            model_name='rankassignment',
            name='rank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='personal_data.rank', verbose_name='Dienstrang'),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='end',
            field=models.DateField(blank=True, null=True, verbose_name='Ende'),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='firefighter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Einsatzkraft'),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_data.authority', verbose_name='Ausgebende Behörde'),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_data.role', verbose_name='Funktion'),
        ),
        migrations.AlterField(
            model_name='roleassignment',
            name='start',
            field=models.DateField(verbose_name='Beginn'),
        ),
    ]