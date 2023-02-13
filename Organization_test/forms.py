from django import forms
from django.forms import ModelForm, RadioSelect, DateTimeInput

from Organization_test.models import OrganiseTest


class OrganizeTestForm(ModelForm):
    class Meta:
        model = OrganiseTest
        exclude = ['slug']
        widgets = {
            "test_for_league": RadioSelect(choices=[]),
            "test_number": RadioSelect(choices=[]),
            "date_time": DateTimeInput()
        }
        labels = {
            "test_for_league": "Dla klasy",
            "test_number": "Który test",
            "date_time": "Data/godzina"
        }

class SolveTestForm(forms.Form):
    answer = forms.CharField(max_length=50)
