from django import forms
from User_manager.models import League

class CreateTestForm(forms.Form):
    name = forms.CharField(label="Nazwa", max_length=50)
    for_league = forms.ChoiceField(choices=[(item.id, item.which_league) for item in League.objects.all()],
                                   widget=forms.RadioSelect(), label="Dla")