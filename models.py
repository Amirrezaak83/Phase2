from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import *

class CustomUser(AbstractUser):
    user_types = [
        ('patient', 'Patient'),
        ('clinic', 'Clinic'),
    ]
    user_type = models.CharField(max_length=20, choices=user_types)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255,unique=True)
    password = models.CharField(validators=[MinLengthValidator(8)], max_length=255)
    email = models.EmailField(unique=True)
    #solving conflict with auth.group
    groups = models.ManyToManyField(
        "auth.Group",
        related_name="custom_user_groups",
        blank=True,
        help_text="The groups this user belongs to.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="custom_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )
class Clinics(models.Model):
    Clinic_id = models.IntegerField(primary_key=True, null=False, blank=False, unique=True)
    name = models.CharField(max_length=255, null=False, blank=False)
    address = models.TextField(null=True, blank=False)
    phone_number = models.CharField(max_length=20, null=True, blank=False)
    services = models.TextField(null=True, blank=True)
    availability = models.BooleanField(null=True, blank=False)


class Appointments(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    clinic_id = models.ForeignKey(Clinics, on_delete=models.CASCADE)
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    datetime = models.DateTimeField(null=False, blank=False)
    status = models.CharField(max_length=255)
    class Meta:
        unique_together = ('clinic_id', 'user_id') # aggregation of clinic_id and user_id should be unique