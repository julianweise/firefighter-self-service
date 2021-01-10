from __future__ import annotations

import datetime
from datetime import date
from typing import List

import django
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import CASCADE
from django.urls import reverse
from django.utils.timezone import now
from django.utils.translation import gettext as _

from equipment.models import Key, Locker, Pager


class Authority(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.name}'


class CategoryOfDriverLicense(models.Model):
    name = models.CharField(max_length=2)

    def __str__(self):
        """String for representing the Category of Driver License object."""
        return f'{self.name}'


class Rank(models.Model):
    sorting_order = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        """String for representing the Rank object."""
        return f'{self.name}'

    class Meta:
        ordering = ['sorting_order']


class UserStatus(models.Model):
    name = models.CharField(max_length=100)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}'


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class Firefighter(AbstractUser):
    username = None
    first_name = models.CharField(_('First Name'), null=False, blank=False, max_length=200)
    last_name = models.CharField(_('Last Name'), null=False, blank=False, max_length=200)
    email = models.EmailField(_('E-Mail'), unique=True)
    picture = models.ImageField(_('Picture'), upload_to='uploads/profile_pictures',
                                default='static/img/no_profile_picture.jpg', blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'street', 'zip', 'city', 'phone_number', 'date_of_birth']

    objects = CustomUserManager()

    staff_id = models.IntegerField(_('Staff ID'), null=True, blank=True)
    status = models.ForeignKey(UserStatus, on_delete=models.PROTECT, null=True)
    joined = models.DateField(_('Joined'), auto_now_add=True, null=True)
    active_since = models.DateField(_('Active since'), default=django.utils.timezone.now, null=False, blank=False)
    street = models.CharField(_('Street'), max_length=200)
    zip = models.IntegerField(_('Zip'))
    city = models.CharField(_('City'), max_length=100)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(_('Phone number'), validators=[phone_regex], max_length=17)
    date_of_birth = models.DateField(_('Date of birth'))

    # Equipment
    pager = models.OneToOneField(Pager, verbose_name=_('Pager'), on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="owner")
    locker = models.OneToOneField(Locker, verbose_name=_('Locker'), on_delete=models.SET_NULL, null=True, blank=True,
                                  related_name="owner")
    key = models.OneToOneField(Key, verbose_name=_('Key'), on_delete=models.SET_NULL, null=True, blank=True,
                               related_name="owner")

    class Meta:
        ordering = ['last_name', 'first_name']
        permissions = [
            ("view_all_firefighter", "Get an overview of all firefighters"),
            ("view_detail_firefighter", "Get detailed information about a firefighter")
        ]

    def age(self):
        date_of_birth = self.date_of_birth
        today = date.today()
        return today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.first_name}  {self.last_name}'

    def get_absolute_url(self):
        return reverse('firefighter-detail', args=[str(self.id)])


class RankAssignment(models.Model):
    rank = models.ForeignKey(Rank, verbose_name=_('Rank'), on_delete=CASCADE, null=False, blank=False)
    firefighter = models.ForeignKey(Firefighter, verbose_name=_('Firefighter'),  on_delete=CASCADE, null=False, blank=False, related_name="ranks")
    issue_date = models.DateField(verbose_name=_('Issue Date'))
    issuer = models.ForeignKey(Authority, verbose_name=_('Issuing Authority'),  on_delete=models.PROTECT, null=False, blank=False)

    @staticmethod
    def get_for(firefighter: Firefighter):
        return RankAssignment.objects.get(firefighter=firefighter).order_by('-issue_date')

    @staticmethod
    def group_by_rank(assignments: List[RankAssignment]):
        grouped_assignments = dict()
        for assignment in assignments:
            grouped_assignments.setdefault(assignment.rank, assignment)
        return grouped_assignments

    def __str__(self):
        """String for representing the Rank Assignment object."""
        return f'{self.firefighter.first_name} {self.firefighter.last_name} is {self.rank.name}'


class DriverLicense(models.Model):
    owner = models.ForeignKey(Firefighter, verbose_name=_('Firefighter'), on_delete=models.CASCADE)
    license_id = models.CharField(max_length=11, verbose_name=_('License ID'))
    issue_date = models.DateField(verbose_name=_('Issue Date'))
    expiration_date = models.DateField(verbose_name=_('Expiration Date'))
    categories = models.ManyToManyField(CategoryOfDriverLicense, verbose_name=_('Categories of Driver License'),
                                        help_text='Select a vehicle categories the driver licenses covers')

    def valid(self):
        return self.expiration_date >= date.today()

    def about_to_expire(self):
        return self.expiration_date <= datetime.date.today() + datetime.timedelta(days=90)

    def __str__(self):
        return f'DriverLicense#{self.license_id}-for-{self.owner}'


class Honor(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    sorting_order = models.IntegerField(null=False, blank=False, unique=True)

    def __str__(self):
        return f'Honor {self.name}'

    class Meta:
        ordering = ['sorting_order']


class HonorAssignment(models.Model):
    firefighter = models.ForeignKey(Firefighter, verbose_name=_('Firefighter'), on_delete=models.CASCADE, null=False, blank=False)
    honor = models.ForeignKey(Honor, verbose_name=_('Honor'), on_delete=models.PROTECT, null=False, blank=False)
    issue_date = models.DateField(verbose_name=_('Issue Date'))
    issuer = models.ForeignKey(Authority, verbose_name=_('Issuing Authority'), on_delete=models.PROTECT, null=False, blank=False)

    @staticmethod
    def group_by_honor(assignments: List[HonorAssignment]):
        grouped_assignments = dict()
        for assignment in assignments:
            grouped_assignments.setdefault(assignment.honor, assignment)
        return grouped_assignments

    def __str__(self):
        return f'Honor {self.honor.name} for {self.firefighter.first_name} {self.firefighter.last_name}'


class Role(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False)
    sorting_order = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f'Role {self.name}'

    class Meta:
        ordering = ['sorting_order']


class RoleAssignment(models.Model):
    role = models.ForeignKey(Role, verbose_name=_('Role'), on_delete=models.PROTECT, null=False, blank=False)
    firefighter = models.ForeignKey(Firefighter, verbose_name=_('Firefighter'), on_delete=models.CASCADE, null=False, blank=False)
    start = models.DateField(verbose_name=_('Start'))
    end = models.DateField(null=True, blank=True, verbose_name=_('End'))
    issuer = models.ForeignKey(Authority, verbose_name=_('Issuing Authority'), on_delete=models.PROTECT, null=False, blank=False)

    def __str__(self):
        return f'{self.firefighter} is/was {self.role} from {self.start} until {self.end} in {self.issuer}'
