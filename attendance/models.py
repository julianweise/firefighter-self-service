from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext as _

from personal_data.models import Firefighter


class Attendance(models.Model):
    start = models.DateTimeField(verbose_name=_("Start"))
    end = models.DateTimeField(verbose_name=_("End"))
    attendees = models.ManyToManyField(Firefighter, verbose_name=_("Attendees"), related_name='attendee',
                                       help_text='Select all attendees of this event')
    person_in_charge = models.ForeignKey(Firefighter, verbose_name=_("Person in charge"), on_delete=models.PROTECT,
                                         related_name='person_in_charge')
    comment = models.CharField(verbose_name=_("Comment"), max_length=2000, null=True, blank=True, default="")
    content_type = models.ForeignKey(ContentType, editable=False, null=True, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ("view_all_attendance", "Get an overview of all attendances"),
        ]

    def duration(self):
        return (self.end - self.start).total_seconds()

    def save(self, *args, **kwargs):
        if not self.content_type:
            self.content_type = ContentType.objects.get_for_model(self.__class__)
        super(Attendance, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.content_type} {_("started")}: {self.start} {_("ended")}: {self.end}'


class Operation(Attendance):
    CODE_WORDS = (
        ('bkl', 'B:Klein'),
        ('bpkw', 'B:PKW'),
        ('blkw', 'B:LKW'),
        ('bss', 'B:Schornstein'),
        ('bgk', 'B:Gebäude klein'),
        ('bgg', 'B:Gebäude groß'),
        ('bso', 'B:Sonderobjekt'),
        ('bbma', 'B:BMA'),
        ('bfl', 'B:Fläche'),
        ('bw', 'B:Wald'),
        ('bwg', 'B:Wald groß'),
        ('bschiene', 'B:Schiene'),
        ('bb', 'B:Boot'),
        ('bschiff', 'B:Schiff'),
        ('bkf', 'B:Kleinflugzeug'),
        ('bgf', 'B:Großflugzeug'),
        ('bex', 'B:Explosion'),
        ('hkl', 'H:Klein'),
        ('hnat', 'H:Natur'),
        ('hhilf', 'H:Hilfeleistung'),
        ('htuer', 'H:Türnotöffnung'),
        ('hvuop', 'H:VU ohne P'),
        ('hvump', 'H:VU mit P'),
        ('hvukl', 'H:VU Klemm'),
        ('hvulkw', 'H:VU LKW/Bus'),
        ('hvuschiene', 'H:VU Schiene'),
        ('hvuschiff', 'H:VU Schiff'),
        ('hflk', 'H:Flugzeugunfall klein'),
        ('hflg', 'H:Flugzeugunfall groß'),
        ('hps', 'H:Person auf Schiene'),
        ('hpw', 'H:Person im Wasser/Eis'),
        ('hrht', 'H:Rettung aus Höhen/Tiefen'),
        ('hg', 'H:Gas'),
        ('hgkl', 'H:Gefahrgut klein'),
        ('hggr', 'H:Gefahrgut groß'),
        ('he', 'H:Einsturz'),
        ('hoell', 'H:ÖL Land'),
        ('hoelw', 'H:ÖL auf Wasser'),
        ('htin', 'H:Tier in Not'),
        ('hkom', 'H:Kommunal'),
        ('htmr', 'H:Person-TMR'),
    )

    code_word = models.CharField(max_length=10, verbose_name=_("Code Word"), choices=CODE_WORDS)
    operation_id = models.IntegerField(verbose_name=_("Operation ID"))

    def __str__(self):
        return f'{self.get_code_word_display()} {self.operation_id} {self.start.strftime("%Y-%m-%d %H:%M:%S")}'


class OtherService(Attendance):
    name = models.CharField(max_length=200, verbose_name=_("Service Notation"))

    def __str__(self):
        return f'{self.name} {self.start}'
