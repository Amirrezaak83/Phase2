"""
URL configuration for AP_2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Phase2.views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', your_home_view, name='home'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('your_dashboard/', your_dashboard, name='your_dashboard'),
    path('patient/update_profile/', update_profile, name='update_profile'),
    path('patient/make_appointment/', make_appointment, name='make_appointment'),
    path('/search_clinic/', search_clinic, name='search_clinic'),
    path('/get_available_slots/', get_available_slots, name='get_available_slots'),
    path('patient/cancel_appointment/<int:appointment_id>/', cancel_appointment, name='cancel_appointment'),
    path('patient/view_appointments/', view_appointments, name='view_appointments'),

]

