from django import forms



# class OrganizeTestForm(ModelForm):
#     class Meta:
#         model = OrganiseTest
#         fields = "__all__"
#         widgets = {
#             "test_for_league": RadioSelect(choices=[]),
#             "test_number": RadioSelect(choices=[]),
#             "date_time": DateTimeInput()
#         }
#         labels = {
#             "test_for_league": "Dla klasy",
#             "test_number": "Który test",
#             "date_time": "Data/godzina"
#         }

class OrganizeTestForm(forms.Form):
    test_for_league = forms.CharField(widget=forms.RadioSelect(choices=[]))
    test_number = forms.CharField(widget=forms.RadioSelect(choices=[]))
    date_time = forms.DateTimeField(widget=forms.DateTimeInput())
