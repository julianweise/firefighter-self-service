import datetime

from django.db import models
from django.db.models import CASCADE
from django.utils.timezone import now
from django.utils.translation import gettext as _

from personal_data.models import Firefighter


class FitnessLevel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"FitnessLevel {self.name}"


class Fitness(models.Model):
    firefighter = models.ForeignKey(Firefighter, verbose_name=_('Firefighter'), on_delete=CASCADE)
    level = models.ForeignKey(FitnessLevel, verbose_name=_('Fitness Level'), on_delete=CASCADE)
    issue_date = models.DateField(verbose_name=_('Issue Date'))
    expiration_date = models.DateField(verbose_name=_('Expiration Date'))

    class Meta:
        ordering = ['-expiration_date']

    def valid(self):
        return self.expiration_date >= now().date()

    def about_to_expire(self):
        return self.expiration_date <= now().date() + datetime.timedelta(days=90)

    def __str__(self):
        return f'{self.level} for {self.firefighter} until {self.expiration_date}'
