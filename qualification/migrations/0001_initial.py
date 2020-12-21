# Generated by Django 3.1.1 on 2020-10-29 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('personal_data', '0001_initial'),
        ('attendance', '0001_initial'),
        ('fitness', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('abbreviation', models.CharField(max_length=5)),
                ('show_in_overview', models.BooleanField(default=False, help_text='Show Course in Overview of Firefighter?', verbose_name='show in overview')),
                ('sorting_order', models.IntegerField(unique=True)),
                ('administration_level', models.CharField(choices=[('ci', 'City'), ('co', 'County'), ('st', 'State')], default='ci', help_text='Administration level', max_length=2)),
                ('requirements', models.ManyToManyField(blank=True, help_text='Select required courses', related_name='_course_requirements_+', to='qualification.Course')),
            ],
            options={
                'ordering': ['sorting_order'],
            },
        ),
        migrations.CreateModel(
            name='LegallyRequiredRecurringTraining',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('recurring_interval', models.CharField(choices=[('an', 'annually'), ('365', 'every 365 days')], max_length=3)),
                ('training_course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='required_training', to='qualification.course')),
            ],
        ),
        migrations.CreateModel(
            name='Training',
            fields=[
                ('attendance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='attendance.attendance')),
                ('topic', models.CharField(max_length=200)),
                ('satisfies_required_trainings', models.ManyToManyField(blank=True, help_text='Select satisfied required trainings', related_name='satisfied_by', to='qualification.LegallyRequiredRecurringTraining')),
            ],
            options={
                'default_permissions': ('add', 'view', 'delete'),
            },
            bases=('attendance.attendance',),
        ),
        migrations.CreateModel(
            name='QualificationRequirement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requires', to='qualification.course')),
                ('fitness_level', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='fitness.fitnesslevel')),
                ('required_training', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='qualification.legallyrequiredrecurringtraining')),
            ],
        ),
        migrations.CreateModel(
            name='Qualification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='required_for_qualification', to='qualification.course')),
                ('firefighter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='qualification', to=settings.AUTH_USER_MODEL)),
                ('issuer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='personal_data.authority')),
            ],
            options={
                'ordering': ['issue_date'],
            },
        ),
    ]