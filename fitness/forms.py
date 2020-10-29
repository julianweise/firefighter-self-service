from django.forms import ModelForm

from attendance.forms import DateInput
from fitness.models import Fitness


class CreateFitnessForm(ModelForm):
    class Meta:
        model = Fitness
        fields = ['firefighter', 'level', 'issue_date', 'expiration_date']
        widgets = {
            'issue_date': DateInput(attrs={'type': 'date'}),
            'expiration_date': DateInput(attrs={'type': 'date'}),
        }
