# Generated by Django 3.1.4 on 2021-06-13 17:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('personal_data', '0004_auto_20210613_1918'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('qualification', '0003_populate_default_data_brandenburg'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='administration_level',
            field=models.CharField(choices=[('ci', 'City'), ('co', 'County'), ('st', 'Federate State')], default='ci', help_text='Administration level', max_length=2),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='required_for_qualification', to='qualification.course', verbose_name='Course'),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='firefighter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualification', to=settings.AUTH_USER_MODEL, verbose_name='Firefighter'),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='issue_date',
            field=models.DateField(verbose_name='Issue Date'),
        ),
        migrations.AlterField(
            model_name='qualification',
            name='issuer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_data.authority', verbose_name='Issuing Authority'),
        ),
        migrations.AlterField(
            model_name='training',
            name='satisfies_required_trainings',
            field=models.ManyToManyField(blank=True, help_text='Select satisfied required trainings', related_name='satisfied_by', to='qualification.LegallyRequiredRecurringTraining', verbose_name='satisfies required training'),
        ),
        migrations.AlterField(
            model_name='training',
            name='topic',
            field=models.CharField(max_length=200, verbose_name='Topic'),
        ),
    ]
