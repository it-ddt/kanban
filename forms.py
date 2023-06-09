from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        label="имя",
    )
    email = forms.EmailField(
        max_length=254,
        label="электронная почта"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        label="пароль",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="повторите пароль",
    )

    class Meta:
        model = User
        fields = [
            'username',
            'email', 
            'password1', 
            'password2', 
            ]