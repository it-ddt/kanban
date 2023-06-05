from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    username = forms.CharField(
        max_length=30,
        required=True,
        help_text='Обязательное поле. 150 символов и меньше. Буквы, цифры, специальные символы (@/./+/-/_).',
        label="Имя пользователя",
    )
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Необязательное поле.',
        label="Имя",
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Необязательное поле.',
        label="Фамилия",
    )
    email = forms.EmailField(
        max_length=254,
        help_text='Введите существующий адрес электронной почты.',
        label="Адрес электронной почты"
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput,
        help_text="<li>Ваш пароль должен содержать как минимум 5 символов.</li>",
        label="Пароль",
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput,
        label="Подтверждение пароля",
    )

    class Meta:
        model = User
        fields = [
            'username', 
            'first_name', 
            'last_name', 
            'email', 
            'password1', 
            'password2', 
            ]