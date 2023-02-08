from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from Question_manager.models import AllPossibleAnswers
from Test_manager.models import League


class AddQuestionForm(forms.Form):
    add_question = forms.CharField(label="Pytanie", widget=forms.Textarea(attrs={"cols": 100,
                                                                                 "rows": 2}))
    possible_answer = forms.MultipleChoiceField(
        choices=[(item.id, item.all_kind_answers) for item in AllPossibleAnswers.objects.all()],
        widget=CheckboxSelectMultiple(attrs={'style': 'margin-left: 20px'}), label="Możliwe odpowiedzi")
    correct_answer = forms.MultipleChoiceField(
        choices=[(item.id, item.all_kind_answers) for item in AllPossibleAnswers.objects.all()],
        widget=CheckboxSelectMultiple(attrs={'style': 'margin-left: 20px'}), label="Prawidłowe odpowiedzi")
    for_league = forms.MultipleChoiceField(choices=[(item.id, item.which_league) for item in League.objects.all()],
                                           widget=CheckboxSelectMultiple(attrs={'style': 'margin-left: 20px'}),
                                           label="Dla")