from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='ticket.event.title', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id', 'user', 'username', 'ticket', 'event_title',
            'amount', 'phone_number', 'mpesa_checkout_id',
            'mpesa_receipt_number', 'status', 'created_at'
        ]
        read_only_fields = [
            'user', 'mpesa_checkout_id', 'mpesa_receipt_number',
            'status', 'created_at'
        ]