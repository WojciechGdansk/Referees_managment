from django import forms
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from User_manager.models import User


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': "Imię",
                                                                              "required": "true"}), label="Imię")
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': "Nazwisko",
                                                                             "required": 'true'}), label="Nazwisko")
    phone_number = forms.IntegerField(label="Numer telefonu",
                                      widget=forms.NumberInput(attrs={"placeholder": "Numer telefonu",
                                                                      "step": 1,
                                                                      'required': 'true'}))
    username = forms.CharField(label="Adres email", widget=forms.EmailInput(attrs={"placeholder": "Adres email",
                                                                                   'required': 'true'}),
                               validators=[validate_email])
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={"placeholder": "Hasło",
                                                                                'required': 'true'}))
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło",
                                                                                         'required': 'true'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Podane hasła nie są idetyczne")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError("Podana nazwa jest już zajęta")
        return email

class LoginForm(forms.Form):
    email = forms.CharField(label="Adres email", widget=forms.EmailInput(attrs={"placeholder": "Adres email",
                                                                                'required': 'true'}),
                            validators=[validate_email])
    password = forms.CharField(label="Hasło", widget=forms.PasswordInput(attrs={"placeholder": "Hasło",
                                                                                'required': 'true'}))


class CreateGroupForm(forms.Form):
    name = forms.CharField(label='Nazwa', widget=forms.TextInput(attrs={'placeholder': "Nazwa grupy"}))


class EditUserForm(forms.Form):
    first_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': "Imię",
                                                                              "required": "true"}), label="Imię")
    last_name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': "Nazwisko",
                                                                             "required": 'true'}), label="Nazwisko")
    phone_number = forms.IntegerField(label="Numer telefonu",
                                      widget=forms.NumberInput(attrs={"placeholder": "Numer telefonu",
                                                                      "step": 1,
                                                                      'required': 'true'}))
    username = forms.CharField(label="Adres email", widget=forms.EmailInput(attrs={"placeholder": "Adres email",
                                                                                   'required': 'true'}),
                               validators=[validate_email])

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Podane hasła nie są idetyczne")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user = User.objects.filter(email=email)
        if user:
            raise ValidationError("Podana nazwa jest już zajęta")
        return email


class ResetPasswordForm(forms.Form):
    password = forms.CharField(label="Nowe hasło", widget=forms.PasswordInput(attrs={"placeholder": "Nowe hasło",
                                                                                'required': 'true'}))
    password2 = forms.CharField(label="Powtórz hasło", widget=forms.PasswordInput(attrs={"placeholder": "Powtórz hasło",
                                                                                         'required': 'true'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        if password != password2:
            raise ValidationError("Podane hasła nie są idetyczne")