from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(
        max_length=15,
        help_text='Номер телефона. Формат +7xxxxxxxxxx',
        label='Номер телефона'
    )
    password1 = forms.CharField(
        label='Введите пароль',
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='Ваш пароль должен содержать как минимум 8 символов и не может состоять только из цифр',
    )

    class Meta:
        model = User
        fields = ('username', 'phone_number', 'email', 'password1', 'password2', )