from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.urls import reverse
from .forms import *
from .models import *
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect



def register_view(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        print(form.data) #for debugging
        if form.is_valid():
            user = form.save()
            messages.info(request, 'Your account has been created! You can now log in.')
            return redirect('login')
        else:
            messages.error(request, 'Invalid form submission.')
            print(form.errors) #for debugging
            return redirect('register')
    else:
        form = register_form()
    return render(request, 'register.html', {'form': form})




def your_home_view(request):
    login_url = reverse('login')  # Use reverse to get the 'login' URL
    return render(request, 'home.html', {'login_url': login_url})



def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('your_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")

    form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def your_dashboard(request):
    if request.user.is_authenticated:
        user_type = request.user.user_type
        if user_type == 'clinic':
            add_clinic = reverse('addclinic')
            return render(request, 'clinic/clinic_dashboard.html')
        elif user_type == 'patient':
            updateprofile = reverse('update_profile')
            appointments = Appointments.objects.filter(user_id=request.user).order_by('datetime')
            return render(request, 'patient/patient_dashboard.html', {'appointments': appointments})




def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST)
        if form.is_valid():
            new_username = form.cleaned_data['new_username']
            new_password = form.cleaned_data['new_password']
            confirm_password = form.cleaned_data['confirm_password']

            user = request.user


            if new_password != confirm_password:
                raise ValidationError("Passwords are not the same")          
             
            if new_username:
                user.username = new_username
                
            if new_password and new_password == confirm_password:
                user.password = make_password(new_password)
                
            user.save()

            messages.info(request, 'Profile updated successfully.')
            return redirect('your_dashboard')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = UpdateProfileForm()

    return render(request, 'patient/update_profile.html', {'form': form})


def search_clinic(request):
    if 'query' in request.GET:
        form = ClinicSearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            clinics = Clinics.objects.filter(name__icontains=query)
    else:
        form = ClinicSearchForm()
        clinics = Clinics.objects.all()
    return render(request, 'search_clinic.html', {'form': form, 'clinics': clinics})


def get_available_slots(request, clinic_id):
    appointments = Appointments.objects.filter(clinic_id=clinic_id, status="Available").order_by('datetime')
    return render(request, 'view_appointments.html', {'appointments': appointments})


def make_appointment(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        appointment = get_object_or_404(Appointments, id=appointment_id, status="Available")
        appointment.status = "Booked"
        appointment.user = request.user
        appointment.save()
        return HttpResponseRedirect('/appointments/')
    else:
        form = AppointmentForm()
        return render(request, 'patient/make_appointment.html', {'form': form})


def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    if request.user == appointment.user:
        appointment.delete()
        messages.success(request, 'Appointment cancelled successfully.')
    else:
        messages.error(request, 'You do not have permission to cancel this appointment.')
    return redirect('view_appointments')


def view_appointments(request):
    appointments = Appointments.objects.filter(user_id=request.user).order_by('datetime')
    return render(request, 'patient/view_appointments.html', {'appointments': appointments})




def add_clinic(request):
    if request.method == 'POST':
        form = AddClinicForm(request.POST)
        if form.is_valid():
            clinic = form.save()
            messages.info(request, 'Your clinic has been created!')
            return redirect('your_dashboard')
        else:
            messages.error(request, 'Invalid form submission.')
            print(form.errors) #for debugging
            return redirect('addclinic')
    else:
        form = AddClinicForm()
    return render(request, 'add_clinic.html', {'form': form})


def view_current_appointments(request):
    appointments = Appointments.objects.filter(status="Scheduled").order_by('datetime')
    return render(request, 'clinic/view_current_appointments.html', {'appointments': appointments})


def cancel_appointment_by_clinic(request, appointment_id):
    try:
        appointment = Appointments.objects.get(pk=appointment_id)
        appointment.delete()
        message = "Appointment canceled successfully."
    except Appointments.DoesNotExist:
        message = "Appointment not found."
    return render(request, 'clinic/cancel_appointment_by_clinic.html', {'message': message})


def increase_appointment_capacity(request):
    if request.method == 'POST':
        clinic_id = request.POST.get('clinic_id')
        additional_capacity = request.POST.get('additional_capacity')
        clinic = Clinics.objects.get(pk=clinic_id)
        clinic.capacity += int(additional_capacity)
        clinic.save()
        return redirect('view_current_appointments')
    return render(request, 'clinic/increase_capacity.html')






