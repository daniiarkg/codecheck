from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import *

class RegistrationForm(forms.ModelForm):
    def clean(self):
        cleaned_data = super().clean()
        get_user = User.objects.filter(username=cleaned_data['login'])
        if len(get_user)>0:
            raise ValidationError('Логин уже занят!')
    login = forms.CharField(max_length=100, label='Логин')
    password = forms.CharField(max_length=100, label='Пароль', widget=forms.PasswordInput,min_length=8)
    class Meta:
        model = Coder
        exclude = ['user',]