from __future__ import annotations

import datetime
from typing import List

from django.db import models
from django.db.models import CASCADE
from django.utils.timezone import now
from django.utils.translation import ugettext_lazy as _

from attendance.models import Attendance
from fitness.models import FitnessLevel, Fitness
from personal_data.models import Firefighter, Authority, CategoryOfDriverLicense, Role, DriverLicense, RoleAssignment


class CourseRequirement(models.Model):
    fitness_requirement = models.ManyToManyField(FitnessLevel, help_text="Select fitness levels that each individually "
                                                                         "satisfy this requirement.", blank=True)
    driver_license_requirement = models.ManyToManyField(CategoryOfDriverLicense,
                                                        help_text="Select driver license categories that each "
                                                                  "individually satisfy this requirement.", blank=True)
    qualification_requirement = models.ManyToManyField("Course", help_text="Select courses that each individually"
                                                                           "satisfy this requirement.", blank=True)

    def fulfilled_by(self, firefighter: Firefighter):
        for fitness_level in self.fitness_requirement.all():
            if not Fitness.objects.filter(firefighter=firefighter, level=fitness_level).exists():
                return False

        if self.driver_license_requirement:
            if not DriverLicense.objects.filter(owner=firefighter, categories__in=self.driver_license_requirement,
                                                expiration_date__gte=now()).exists():
                return False

        for course in self.qualification_requirement.all():
            if not Qualification.objects.filter(firefighter=firefighter, course=course).exists():
                return False

        return True


class Course(models.Model):
    ADMINISTRATION_LEVEL = (
        ('ci', 'City'),
        ('co', 'County'),
        ('st', 'State'),
    )

    name = models.CharField(max_length=200)
    abbreviation = models.CharField(max_length=5, null=False, blank=False)
    show_in_overview = models.BooleanField(default=False, help_text="Show Course in Overview of Firefighter?",
                                           verbose_name="show in overview")
    sorting_order = models.IntegerField(null=False, blank=False, unique=True)
    administration_level = models.CharField(max_length=2, choices=ADMINISTRATION_LEVEL, blank=False, default='ci',
                                            help_text='Administration level')
    requirements = models.ManyToManyField(CourseRequirement, blank=True, help_text='Specify admission restrictions')

    def requirements_satisfied_by(self, firefighter: Firefighter):
        for requirement in self.requirements.all():
            if requirement.satisfied_by(firefighter):
                return True
            return False

    def __str__(self):
        return f'{_("Course")} {self.name}'

    class Meta:
        ordering = ['sorting_order']


class Qualification(models.Model):
    issue_date = models.DateField(null=False, blank=False)
    course = models.ForeignKey(Course, on_delete=models.PROTECT, related_name="required_for_qualification")
    firefighter = models.ForeignKey(Firefighter, on_delete=models.CASCADE, null=False, related_name='qualification')
    issuer = models.ForeignKey(Authority, on_delete=models.PROTECT, null=False)

    def valid(self):
        requirements = QualificationRequirement.objects.filter(course=self.course)
        if not requirements.exists():
            return True
        else:
            for requirement in requirements:
                if not requirement.satisfied_by(self):
                    return False
        return True

    def __str__(self):
        return f'{self.course} obtained on {self.issue_date} by {self.firefighter}'

    @staticmethod
    def group_by_course(qualifications: List[Qualification]):
        grouped_qualifications = dict()
        for qualification in qualifications:
            grouped_qualifications.setdefault(qualification.course, qualification)
        return grouped_qualifications

    class Meta:
        ordering = ['issue_date']


class LegallyRequiredRecurringTraining(models.Model):
    RECURRING_INTERVALS = (
        ('an', 'annually'),
        ('365', 'every 365 days'),
    )

    name = models.CharField(max_length=200, null=False, blank=False)
    training_course = models.ForeignKey(Course, on_delete=CASCADE, related_name="required_training")
    recurring_interval = models.CharField(max_length=3, choices=RECURRING_INTERVALS, blank=False, null=False)

    def is_satisfied_by(self, training: Training, qualification: Qualification):
        if self.recurring_interval == 'an':
            return qualification.issue_date.year >= now().year or training and training.end.year >= now().year - 1
        elif self.recurring_interval == '365':
            return qualification.issue_date >= now().date() - datetime.timedelta(days=365) or \
                   training and training.end.date() >= now().date() - datetime.timedelta(days=365)
        else:
            return False

    def __str__(self):
        return f'{self.name} for {self.training_course}'


class Training(Attendance):
    topic = models.CharField(max_length=200)
    satisfies_required_trainings = models.ManyToManyField(LegallyRequiredRecurringTraining, blank=True,
                                                          help_text="Select satisfied required trainings",
                                                          related_name="satisfied_by")

    def __str__(self):
        return f'{self.topic} {self.start}'


class QualificationRequirement(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, blank=False, null=False, related_name="requires")
    fitness_level = models.ForeignKey(FitnessLevel, on_delete=models.SET_NULL, blank=True, null=True)
    required_training = models.ForeignKey(LegallyRequiredRecurringTraining, on_delete=models.SET_NULL, blank=True,
                                          null=True)

    def satisfied_by(self, qualification: Qualification):
        if self.fitness_level:
            fitness = Fitness.objects.filter(firefighter=qualification.firefighter, level=self.fitness_level) \
                .order_by('-expiration_date').last()
            if not fitness.valid():
                return False
        if self.required_training:
            training = Training.objects.filter(satisfies_required_trainings__in=[self.required_training],
                                               attendees__in=[qualification.firefighter]) \
                .order_by('-end').first()
            if not self.required_training.is_satisfied_by(training, qualification):
                return False
        return True

    def __str__(self):
        return f'{self.course} requires fitness level {self.fitness_level} and training {self.required_training}'
