from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'phone_number', 'status', 'created_at']
    list_filter = ['status', 'notification_type']
    search_fields = ['user__username', 'phone_number']