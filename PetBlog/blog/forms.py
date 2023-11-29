from captcha.fields import CaptchaField, CaptchaTextInput
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Profile, Post


# from .models import Profile


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


class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(label='Аватар', required=False, widget=forms.FileInput(attrs={'class': 'form-control'}))
    about_me = forms.CharField(label="Обо мне", required=False, widget=CKEditorUploadingWidget())

    class Meta:
        model = Profile
        fields = ['avatar', 'about_me']


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image', 'category', 'tags', 'is_published']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': CKEditorUploadingWidget(),
            'image': forms.FileInput(attrs={'class': 'form-control'})
        }


class MailingForm(forms.Form):
    title = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))
    context = forms.CharField(label='Название', widget=forms.TextInput(attrs={'class': 'form-control'}))

