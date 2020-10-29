from django.forms import ModelForm

from attendance.forms import DateInput
from qualification.models import Qualification


class CreateQualificationForm(ModelForm):
    class Meta:
        model = Qualification
        fields = ['firefighter', 'course', 'issue_date', 'issuer']
        widgets = {
            'issue_date': DateInput(attrs={'type': 'date'})
        }
