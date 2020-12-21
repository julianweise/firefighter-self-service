from django.forms import ModelForm

from attendance.forms import DateTimeInput
from event.models import Event, CourseEvent


class CreateEventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'start', 'end', 'person_in_charge']
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class CreateCourseEventForm(ModelForm):
    class Meta:
        model = CourseEvent
        fields = ['name', 'start', 'end', 'person_in_charge', 'course']
        widgets = {
            'start': DateTimeInput(attrs={'type': 'datetime-local'}),
            'end': DateTimeInput(attrs={'type': 'datetime-local'}),
        }
