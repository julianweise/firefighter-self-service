# Generated by Django 3.1.1 on 2020-10-29 15:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start', models.DateTimeField()),
                ('end', models.DateTimeField()),
                ('attendees', models.ManyToManyField(help_text='Select all attendees of this event', related_name='attendee', to=settings.AUTH_USER_MODEL)),
                ('person_in_charge', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='person_in_charge', to=settings.AUTH_USER_MODEL)),
                ('comment', models.CharField(blank=True, default='', max_length=2000, null=True)),
                ('content_type', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, to='contenttypes.contenttype'),)
            ],
            options={'permissions': [('view_all', 'Get an overview of all firefighters')]},
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('attendance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='attendance.attendance')),
                ('code_word', models.CharField(choices=[('bkl', 'B:Klein'), ('bpkw', 'B:PKW'), ('blkw', 'B:LKW'), ('bss', 'B:Schornstein'), ('bgk', 'B:Gebäude klein'), ('bgg', 'B:Gebäude groß'), ('bso', 'B:Sonderobjekt'), ('bbma', 'B:BMA'), ('bfl', 'B:Fläche'), ('bw', 'B:Wald'), ('bwg', 'B:Wald groß'), ('bschiene', 'B:Schiene'), ('bb', 'B:Boot'), ('bschiff', 'B:Schiff'), ('bkf', 'B:Kleinflugzeug'), ('bgf', 'B:Großflugzeug'), ('bex', 'B:Explosion'), ('hkl', 'H:Klein'), ('hnat', 'H:Natur'), ('hhilf', 'H:Hilfeleistung'), ('htuer', 'H:Türnotöffnung'), ('hvuop', 'H:VU ohne P'), ('hvump', 'H:VU mit P'), ('hvukl', 'H:VU Klemm'), ('hvulkw', 'H:VU LKW/Bus'), ('hvuschiene', 'H:VU Schiene'), ('hvuschiff', 'H:VU Schiff'), ('hflk', 'H:Flugzeugunfall klein'), ('hflg', 'H:Flugzeugunfall groß'), ('hps', 'H:Person auf Schiene'), ('hpw', 'H:Person im Wasser/Eis'), ('hrht', 'H:Rettung aus Höhen/Tiefen'), ('hg', 'H:Gas'), ('hgkl', 'H:Gefahrgut klein'), ('hggr', 'H:Gefahrgut groß'), ('he', 'H:Einsturz'), ('hoell', 'H:ÖL Land'), ('hoelw', 'H:ÖL auf Wasser'), ('htin', 'H:Tier in Not'), ('hkom', 'H:Kommunal'), ('htmr', 'H:Person-TMR')], max_length=10)),
                ('operation_id', models.IntegerField()),
            ],
            bases=('attendance.attendance',),
        ),
        migrations.CreateModel(
            name='OtherService',
            fields=[
                ('attendance_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='attendance.attendance')),
                ('name', models.CharField(max_length=200)),
            ],
            bases=('attendance.attendance',),
        ),
    ]
