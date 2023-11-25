from captcha.fields import CaptchaField, CaptchaTextInput
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class CustomCaptchaTextInput(CaptchaTextInput):
    template_name = 'blog/custom_captcha_field.html'


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=128, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(max_length=128, label='Пароль',
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=128, label='Имя пользователя',
                               widget=forms.TextInput(attrs={'class': 'form-control'}))

    email = forms.EmailField(max_length=128, label='Почта', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    password1 = forms.CharField(max_length=128, label='Пароль',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    password2 = forms.CharField(max_length=128, label='Подтверждение пароля',
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    captcha = CaptchaField(label='Введите символы с картинки', widget=CustomCaptchaTextInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
