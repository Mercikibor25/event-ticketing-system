from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_date = serializers.DateTimeField(source='event.date', read_only=True)
    event_venue = serializers.CharField(source='event.venue', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Ticket
        fields = [
            'id', 'ticket_id', 'user', 'username', 'event',
            'event_title', 'event_date', 'event_venue',
            'status', 'qr_code', 'booked_at'
        ]
        read_only_fields = ['ticket_id', 'user', 'status', 'qr_code', 'booked_at']