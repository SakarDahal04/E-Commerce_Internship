from django.db import models
from django.contrib.auth.models import AbstractUser

class Address(models.Model):
    street = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    postal_code = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100)

class CustomUser(AbstractUser):
    native_name = models.CharField(max_length=100, blank=True, help_text="please enter your name")
    address = models.OneToOneField(Address, on_delete=models.CASCADE, help_text="Enter the address")
    phone_no = models.PositiveBigIntegerField()
    # profile_picture = models.ImageField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


