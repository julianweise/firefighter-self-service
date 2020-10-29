from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea
from django.utils.translation import ugettext_lazy as _

from attendance.models import Attendance, OtherService, Operation
from qualification.models import Training


class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)


class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class AttendanceForm(ModelForm):

    def clean(self):
        cleaned_data = super().clean()
        AttendanceForm._check_start_before_end(cleaned_data)
        self._attendees_available(cleaned_data)

    @staticmethod
    def _check_start_before_end(cleaned_data):
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if start and end:
            if start >= end:
                raise ValidationError(
                    _('Invalid time range: End lies before start %(end)s < %(start)s'),
                    code='invalid',
                    params={'start': start, 'end': end},
                )

    def _attendees_available(self, cleaned_data):
        attendees = cleaned_data.get("attendees")
        start = cleaned_data.get("start")
        end = cleaned_data.get("end")
        if attendees:
            intersecting_attendances = Attendance.objects.filter(attendees__in=[a.id for a in attendees],
                                                                 start__gte=start, end__lte=end) \
                .exclude(pk=self.instance.id)
            if len(intersecting_attendances) > 0:
                flat_list = [i.attendees for i in intersecting_attendances]
                raise ValidationError(
                    _('You have selected firefighters that have been marked attending already other overlapping '
                      'activities: A firefighter can not attend two activities at the same time.'),
                    code='invalid',
                    params={'activities': flat_list},
                )


class TrainingForm(AttendanceForm):
    class Meta:
        model = Training
        fields = ('start', 'end', 'topic', 'satisfies_required_trainings', 'person_in_charge', 'comment', 'attendees')
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': Textarea(attrs={'cols': 80, 'rows': 4}),
        }


class OperationForm(AttendanceForm):
    class Meta:
        model = Operation
        fields = ('start', 'end', 'code_word', 'operation_id', 'person_in_charge', 'comment', 'attendees')
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': Textarea(attrs={'cols': 80, 'rows': 4}),
        }


class OtherServiceForm(AttendanceForm):
    class Meta:
        model = OtherService
        fields = ('start', 'end', 'name', 'person_in_charge', 'comment', 'attendees')
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
            'comment': Textarea(attrs={'cols': 80, 'rows': 4}),
        }
