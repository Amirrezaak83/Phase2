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








