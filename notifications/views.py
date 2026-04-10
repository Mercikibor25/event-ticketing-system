from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from .utils import send_event_update
from events.models import Event
from tickets.models import Ticket

class NotificationListView(generics.ListAPIView):
    """List all SMS notifications for the logged in user"""
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)


class SendEventUpdateView(APIView):
    """Admin sends an update SMS to all ticket holders of an event"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Only admin can send updates
        if request.user.role != 'admin':
            return Response(
                {'error': 'Only admins can send event updates.'},
                status=status.HTTP_403_FORBIDDEN
            )

        event_id = request.data.get('event_id')
        message = request.data.get('message')

        if not event_id or not message:
            return Response(
                {'error': 'event_id and message are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Get all active ticket holders for this event
        tickets = Ticket.objects.filter(event=event, status='active')

        if not tickets.exists():
            return Response(
                {'message': 'No active ticket holders found for this event.'},
                status=status.HTTP_200_OK
            )

        sent_count = 0
        for ticket in tickets:
            user = ticket.user
            if user.phone_number:
                send_event_update(user, event, message)
                sent_count += 1

        return Response(
            {'message': f'Update sent to {sent_count} attendees.'},
            status=status.HTTP_200_OK
        )