from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import *



def register_view(request):
    if request.method == 'POST':
        form = register_form(request.POST)
        if form.is_valid():
            form.check_email()
            form.check_username()
            user = form.save()
            messages.info(request, 'Your account has been created! You can now log in.')
            return redirect('login')
    else:
        form = register_form()
    return render(request, 'register.html', {'form': form})





