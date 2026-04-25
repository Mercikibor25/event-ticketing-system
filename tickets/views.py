from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Ticket
from .serializers import TicketSerializer
from .utils import generate_qr_code
from events.models import Event

class BookTicketView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        event_id = request.data.get('event_id')
        quantity = int(request.data.get('quantity', 1))

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
                {'error': 'Sorry this event is sold out.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check enough tickets available for requested quantity
        if event.available_tickets < quantity:
            return Response(
                {'error': f'Only {event.available_tickets} tickets available.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check quantity is valid
        if quantity < 1 or quantity > 10:
            return Response(
                {'error': 'You can book between 1 and 10 tickets at a time.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Calculate total amount
        total_amount = event.ticket_price * quantity

        # Create tickets
        tickets = []
        for i in range(quantity):
            ticket = Ticket.objects.create(
                user=request.user,
                event=event
            )
            # Generate QR code for each ticket
            generate_qr_code(ticket)
            tickets.append(ticket)

        # Reduce available tickets
        event.available_tickets -= quantity
        event.save()

        # Send one SMS for all tickets booked
        from notifications.utils import send_ticket_confirmation
        send_ticket_confirmation(request.user, tickets[0], quantity, total_amount)

        serializer = TicketSerializer(tickets, many=True)
        return Response(
            {
                'message': f'{quantity} ticket(s) booked successfully!',
                'tickets': serializer.data,
                'total_amount': str(total_amount),
                'quantity': quantity
            },
            status=status.HTTP_201_CREATED
        )


class MyTicketsView(generics.ListAPIView):
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(user=self.request.user)

class TicketDetailView(generics.RetrieveAPIView):
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