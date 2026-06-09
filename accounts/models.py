from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('attendee', 'Attendee'),
        ('admin', 'Admin'),
    ]
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='attendee')
    national_id = models.CharField(max_length=20, blank=True)
    kra_pin = models.CharField(max_length=20, blank=True)
    taxpayer_name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"