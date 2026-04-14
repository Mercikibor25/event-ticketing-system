from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ticket
from .serializers import TicketSerializer
from .utils import generate_qr_code
from events.models import Event
from notifications.utils import send_ticket_confirmation

class BookTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        event_id = request.data.get('event_id')

        # Check event exists
        try:
            event = Event.objects.get(id=event_id)
        except Event.DoesNotExist:
            return Response(
                {'error': 'Event not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check tickets are available
        if event.available_tickets <= 0:
            return Response(
                {'error': 'Sorry, this event is sold out.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check user hasn't already booked this event
        if Ticket.objects.filter(user=request.user, event=event, status='active').exists():
            return Response(
                {'error': 'You have already booked a ticket for this event.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create ticket
        ticket = Ticket.objects.create(user=request.user, event=event)

        # Reduce available tickets
        event.available_tickets -= 1
        event.save()

        # Generate QR code
        generate_qr_code(ticket)
        
        
        send_ticket_confirmation(request.user, ticket)

        serializer = TicketSerializer(ticket)
        return Response(
            {
                'message': 'Ticket booked successfully!',
                'ticket': serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
class MyTicketsView(generics.ListAPIView):
    """List all tickets for the logged in user"""
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

class TicketDetailView(generics.RetrieveAPIView):
    """View a single ticket"""
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

class ValidateTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ticket_id = request.data.get('ticket_id')

        try:
            ticket = Ticket.objects.get(ticket_id=ticket_id)
        except Ticket.DoesNotExist:
            return Response(
                {'valid': False, 'message': 'Invalid ticket.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if ticket.status == 'used':
            return Response(
                {'valid': False, 'message': 'Ticket has already been used.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if ticket.status == 'cancelled':
            return Response(
                {'valid': False, 'message': 'Ticket has been cancelled.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if ticket has been paid for
        from payments.models import Payment
        payment = Payment.objects.filter(
            ticket=ticket,
            status='completed'
        ).first()

        if not payment:
            return Response(
                {
                    'valid': False,
                    'message': 'Ticket has not been paid for. Please pay before entry.'
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mark ticket as used
        ticket.status = 'used'
        ticket.save()

        return Response(
            {
                'valid': True,
                'message': 'Ticket validated successfully.',
                'attendee': ticket.user.username,
                'event': ticket.event.title
            },
            status=status.HTTP_200_OK
        )