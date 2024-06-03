from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.contrib.auth.models import User
from .models import Datatesting, Datatraining


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    email = forms.CharField(label="Email", widget=forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={'class': 'form-control', 'required': 'required'}))

    model = User
    fields = ('username', 'email', 'password1', 'password2')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password1')
        password_repeat = cleaned_data.get('password2')

        if password != password_repeat:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': "form-control", 'required': 'required'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': "form-control", 'required': 'required'}))

    model = User
    fields = ('username', 'password')
