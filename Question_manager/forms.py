from django import forms
from django.forms.widgets import CheckboxSelectMultiple
from Question_manager.models import AllPossibleAnswers
from Test_manager.models import League, Questions


class AddQuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['add_question', 'question_possible_answer', 'question_correct_answer', 'for_league']
        widgets = {
            "add_question": forms.Textarea(attrs={'placeholder': "Pytanie", "cols": 80, "rows":2}),
            "question_possible_answer": forms.CheckboxSelectMultiple,
            "question_correct_answer": forms.CheckboxSelectMultiple,
            "for_league": forms.CheckboxSelectMultiple
        }
        labels = {
            "add_question": "Pytanie",
            "question_possible_answer": "Możliwe odpowiedzi",
            "question_correct_answer": "Prawidłowe odpowiedzi",
            "for_league": "Dla klasy"
        }