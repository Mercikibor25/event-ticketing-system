

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('attendee', 'Attendee'),
        ('admin', 'Admin'),
    ]
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='attendee')

    def __str__(self):
        return f"{self.username} ({self.role})"