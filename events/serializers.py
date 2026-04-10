from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    is_sold_out = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'venue', 'date',
            'ticket_price', 'total_capacity', 'available_tickets',
            'status', 'organizer', 'organizer_name',
            'is_sold_out', 'created_at'
        ]
        read_only_fields = ['organizer', 'available_tickets', 'created_at']

    def get_is_sold_out(self, obj):
        return obj.available_tickets == 0