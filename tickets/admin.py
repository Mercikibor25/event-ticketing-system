from django.contrib import admin
from .models import Ticket

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_id', 'user', 'event', 'status', 'booked_at']
    list_filter = ['status', 'event']
    search_fields = ['ticket_id', 'user__username', 'event__title']