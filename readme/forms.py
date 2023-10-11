from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        widgets = {
            'birthdate': DateInput()
        }
        fields = ['username', 'email', 'password1',
                  'password2', 'birthdate']
