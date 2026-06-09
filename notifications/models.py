from django.db import models
from accounts.models import CustomUser

class Notification(models.Model):
    TYPE_CHOICES = [
        ('ticket_confirmation', 'Ticket Confirmation'),
        ('event_reminder', 'Event Reminder'),
        ('event_update', 'Event Update'),
        ('payment_confirmation', 'Payment Confirmation'),
    ]

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    message = models.TextField()
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type} - {self.user.username} - {self.status}"

    class Meta:
        ordering = ['-created_at']