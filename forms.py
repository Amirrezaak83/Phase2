from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import *
from django.core.exceptions import *
from django.contrib.auth import authenticate



class register_form(UserCreationForm): #user_creation_form have username and password by default

    email = forms.EmailField()
    first_name = forms.CharField()
    last_name = forms.CharField()
    user_type = forms.ChoiceField(choices=CustomUser.user_types)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'password1', 'password2', 'email', 'user_type']

    def check_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email address is already in use.')
        return email
    def check_username(self):
        username = self.cleaned_data.get('username')
        if CustomUser.objects.filter(username=username).exists():
            raise ValidationError('This username is already in use.')
        return username



class LoginForm(forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
    )

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError("Invalid username or password.")

        return cleaned_data

