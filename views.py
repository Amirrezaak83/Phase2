from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.urls import reverse
from .forms import *
from django.contrib.auth.hashers import make_password



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
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username= username, password= password)
            if user is not None:
                login(request, user)
                return redirect('your_dashboard')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        else:
            messages.error(request, f'invalid form submission,  error: {form.errors}')
            return redirect('login')
    else:
        form = LoginForm()
        return render(request, 'login.html', {'form': form})




def your_dashboard(request):
    user_type = request.CustomUser.user_type
    if user_type == 'clinic':
        add_clinic = reverse('addclinic')
        return render(request, 'clinic_dashboard.html')
    elif user_type == 'patient':
        updateprofile = reverse('update_profile')
        return render(request, 'patient_dashboard.html')




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

    return render(request, 'update_profile.html', {'form': form})



