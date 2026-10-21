from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    organizer_name = serializers.CharField(source='organizer.username', read_only=True)
    is_sold_out = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = [
            'id', 'title', 'description', 'venue', 'date',
            'ticket_price', 'total_capacity', 'available_tickets',
            'status', 'organizer', 'organizer_name',
            'is_sold_out', 'image', 'image_url', 'created_at'
        ]
        read_only_fields = ['organizer', 'available_tickets', 'created_at']

    def get_is_sold_out(self, obj):
        return obj.available_tickets == 0

    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None