from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.urls import reverse
from .forms import *




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





