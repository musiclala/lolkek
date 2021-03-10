from django import forms
from django.core.exceptions import ValidationError
from .models import News
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from django.contrib.auth.models import User
import re


class ContactForm(forms.Form):
    email = forms.EmailField(label='Ваш емаил', widget=forms.EmailInput())
    subject = forms.CharField(label='Тема', widget=forms.TextInput())
    content = forms.CharField(label='Текст', widget=forms.Textarea())


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput())


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput())
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput())
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput())
    email = forms.EmailField(label='Email', widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(),
            'content': forms.Textarea(),
            'category': forms.Select(),
            'photo': forms.ClearableFileInput(),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры!')
        return title
