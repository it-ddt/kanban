from django import forms
from django.contrib.auth import password_validation as pv
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class user_register_form(UserCreationForm):
    first_name = forms.CharField(label="Имя: ", max_length=150)
    last_name = forms.CharField(label="Фамилия: ", max_length=150)
    username = forms.CharField(label="Псевдоним: ", max_length=150)
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="<p>[!] Ваш пароль должен содержать как минимум 5 символов.</p>"
    )
    password2 = forms.CharField(
        label="Подтверждение пароля: ",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User

        # TODO Email
        fields = [
            "first_name",
            "last_name",
            "username",
            "password1",
            "password2",
        ]
