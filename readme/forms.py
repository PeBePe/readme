from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class DateInput(forms.DateInput):
    input_type = 'date'


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = "__all__"


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        widgets = {
            'birthdate': DateInput()
        }
        fields = ['name', 'username', 'email', 'password1',
                  'password2', 'birthdate']

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                "User with this username already exists.", code='unique')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(
                "User with this email already exists.", code='unique')
        return email
