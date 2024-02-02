from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import *
from django.core.exceptions import *

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



class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']



class UpdateProfileForm(forms.ModelForm):
    new_username = forms.CharField(required=False)
    new_password = forms.CharField(widget=forms.PasswordInput, required=False)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['new_username', 'new_password', 'confirm_password']



class AddClinicForm(forms.ModelForm):
    name = forms.CharField(max_length=255, required=True)
    address = forms.CharField(widget=forms.Textarea, required=True)
    phone_number = forms.CharField(max_length=20, required=True)
    services = forms.CharField(widget=forms.Textarea, required=True)
    availability = forms.BooleanField(required=True)

    class Meta:
        model = Clinics
        fields = ['name', 'address', 'phone_number', 'services', 'availability']
        exclude = ['clinic_id']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['appointment_id', 'clinic_id', 'user_id', 'datetime', 'status']


class ClinicSearchForm(forms.Form):
    query = forms.CharField(label='Search for clinics', max_length=100)
