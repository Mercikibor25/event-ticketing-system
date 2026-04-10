

# Register your models here.
from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'venue', 'date', 'ticket_price', 'available_tickets', 'status']
    list_filter = ['status', 'date']
    search_fields = ['title', 'venue']