from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class register_form(UserCreationForm): #user_creation_form have username and password by default

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    user_type = forms.ChoiceField(choices=CustomUser.user_types)

    class meta:
        model = CustomUser
        field = ['user_type', 'first_name', 'last_name', 'username', 'password', 'email']
    def check_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
    def check_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already in use.')
        return username


        
