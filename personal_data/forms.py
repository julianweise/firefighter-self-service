import datetime

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import ModelForm, forms, ModelMultipleChoiceField
from django.utils.translation import ugettext_lazy as _

from attendance.forms import DateInput
from equipment.models import Pager, Key, Locker
from personal_data.models import Firefighter, DriverLicense, RankAssignment, HonorAssignment, RoleAssignment


class UpdatePersonalDataPersonalForm(ModelForm):
    class Meta:
        model = Firefighter
        fields = ['first_name', 'last_name', 'staff_id', 'email', 'street', 'zip', 'city', 'phone_number']

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']

        if data + datetime.timedelta(weeks=52 * 15) > datetime.date.today():
            raise ValidationError(_("A firefighter has to be at least 15 years old."))

        return data


class CreatePersonalDataForm(ModelForm):
    class Meta:
        model = Firefighter
        fields = ['first_name', 'last_name', 'staff_id', 'date_of_birth', 'email', 'phone_number', 'street', 'zip',
                  'city', 'pager', 'locker', 'key', 'status', 'active_since']
        widgets = {
            'date_of_birth': DateInput(attrs={'type': 'date'}),
            'active_since': DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(CreatePersonalDataForm, self).__init__(*args, **kwargs)
        self.fields['pager'].queryset = Pager.objects.filter(owner__isnull=True)
        self.fields['key'].queryset = Key.objects.filter(owner__isnull=True)
        self.fields['locker'].queryset = Locker.objects.filter(owner__isnull=True)

    def clean_date_of_birth(self):
        data = self.cleaned_data['date_of_birth']

        if data + datetime.timedelta(weeks=52 * 15) > datetime.date.today():
            raise ValidationError(_("A firefighter has to be at least 15 years old."))

        return data


class UpdatePersonalDataForm(CreatePersonalDataForm):

    def __init__(self, *args, **kwargs):
        super(UpdatePersonalDataForm, self).__init__(*args, **kwargs)
        self.fields['pager'].queryset = Pager.objects.filter(Q(owner__isnull=True) | Q(owner=kwargs['instance']))
        self.fields['key'].queryset = Key.objects.filter(Q(owner__isnull=True) | Q(owner=kwargs['instance']))
        self.fields['locker'].queryset = Locker.objects.filter(Q(owner__isnull=True) | Q(owner=kwargs['instance']))


class CreateDriverLicenseForm(ModelForm):
    class Meta:
        model = DriverLicense
        fields = ['owner', 'license_id', 'issue_date', 'expiration_date', 'categories']
        widgets = {
            'issue_date': DateInput(attrs={'type': 'date'}),
            'expiration_date': DateInput(attrs={'type': 'date'}),
        }


class CreateRankAssignmentForm(ModelForm):
    class Meta:
        model = RankAssignment
        fields = ['rank', 'firefighter', 'issue_date', 'issuer']
        widgets = {
            'issue_date': DateInput(attrs={'type': 'date'}),
        }


class CreateHonorAssignmentForm(ModelForm):
    class Meta:
        model = HonorAssignment
        fields = ['firefighter', 'honor', 'issue_date', 'issuer']
        widgets = {
            'issue_date': DateInput(attrs={'type': 'date'}),
        }


class CreateRoleAssignmentForm(ModelForm):
    class Meta:
        model = RoleAssignment
        fields = ['role', 'firefighter', 'start', 'end', 'issuer']
        widgets = {
            'start': DateInput(attrs={'type': 'date'}),
            'end': DateInput(attrs={'type': 'date'}),
        }


class GroupAdminForm(ModelForm):
    class Meta:
        model = Group
        exclude = []

    users = ModelMultipleChoiceField(
         queryset=get_user_model().objects.all(),
         required=False,
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()
        return instance
