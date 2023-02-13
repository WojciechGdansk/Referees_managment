from django import forms

from Test_manager.models import AllTest


class CreateTestForm(forms.ModelForm):
    class Meta:
        model = AllTest
        fields = ['test_name', 'date', 'for_league']
        widgets = {"for_league": forms.RadioSelect(),
                   "test_name": forms.TextInput(attrs={'placeholder': 'Nazwa testu'})}
        labels = {"test_name": "Nazwa",
                  "date": "Data",
                  "for_league": "Dla klasy"}