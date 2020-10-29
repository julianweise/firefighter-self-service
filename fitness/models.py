import datetime

from django.db import models
from django.db.models import CASCADE
from django.utils.timezone import now

from personal_data.models import Firefighter


class FitnessLevel(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"FitnessLevel {self.name}"


class Fitness(models.Model):
    firefighter = models.ForeignKey(Firefighter, on_delete=CASCADE)
    level = models.ForeignKey(FitnessLevel, on_delete=CASCADE)
    issue_date = models.DateField()
    expiration_date = models.DateField()

    class Meta:
        ordering = ['-expiration_date']

    def valid(self):
        return self.expiration_date >= now().date()

    def about_to_expire(self):
        return self.expiration_date <= now().date() + datetime.timedelta(days=90)

    def __str__(self):
        return f'{self.level} for {self.firefighter} until {self.expiration_date}'
