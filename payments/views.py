from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Payment
from .serializers import PaymentSerializer
from .mpesa import stk_push
from tickets.models import Ticket
from notifications.utils import send_payment_confirmation
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class InitiatePaymentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        ticket_id = request.data.get('ticket_id')
        phone_number = request.data.get('phone_number')

        # Validate inputs
        if not ticket_id or not phone_number:
            return Response(
                {'error': 'ticket_id and phone_number are required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get ticket
        try:
            ticket = Ticket.objects.get(id=ticket_id, user=request.user)
        except Ticket.DoesNotExist:
            return Response(
                {'error': 'Ticket not found.'},
                status=status.HTTP_404_NOT_FOUND
            )

        # Check if already paid
        if Payment.objects.filter(ticket=ticket, status='completed').exists():
            return Response(
                {'error': 'This ticket has already been paid for.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        amount = ticket.event.ticket_price

        # Create pending payment record
        payment = Payment.objects.create(
            user=request.user,
            ticket=ticket,
            amount=amount,
            phone_number=phone_number,
            status='pending'
        )

        # Initiate STK Push
        response = stk_push(
            phone_number=phone_number,
            amount=amount,
            account_reference=f"TICKET-{ticket.ticket_id}",
            description=f"Payment for {ticket.event.title}"
        )

        if response.get('ResponseCode') == '0':
            payment.mpesa_checkout_id = response.get('CheckoutRequestID')
            payment.save()
            return Response(
                {
                    'message': 'Payment initiated. Check your phone for the M-Pesa prompt.',
                    'checkout_request_id': payment.mpesa_checkout_id,
                    'payment_id': payment.id
                },
                status=status.HTTP_200_OK
            )
        else:
            payment.status = 'failed'
            payment.save()
            return Response(
                {'error': 'Failed to initiate payment. Try again.', 'details': response},
                status=status.HTTP_400_BAD_REQUEST
            )


@method_decorator(csrf_exempt, name='dispatch')
class MpesaCallbackView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        data = request.data
        callback = data.get('Body', {}).get('stkCallback', {})
        result_code = callback.get('ResultCode')
        checkout_id = callback.get('CheckoutRequestID')

        try:
            payment = Payment.objects.get(mpesa_checkout_id=checkout_id)
        except Payment.DoesNotExist:
            return Response({'status': 'ok'})

        if result_code == 0:
            items = callback.get('CallbackMetadata', {}).get('Item', [])
            receipt = next((i['Value'] for i in items if i['Name'] == 'MpesaReceiptNumber'), None)
            payment.mpesa_receipt_number = receipt
            payment.status = 'completed'
            payment.save()

            # Send SMS confirmation
            send_payment_confirmation(payment.user, payment)
        else:
            payment.status = 'failed'
            payment.save()

        return Response({'status': 'ok'})


class PaymentHistoryView(generics.ListAPIView):
    """List all payments for the logged in user"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user)