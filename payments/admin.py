from django.contrib import admin
from .models import Payment

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'ticket', 'amount', 'status', 'mpesa_receipt_number', 'created_at']
    list_filter = ['status']
    search_fields = ['user__username', 'mpesa_receipt_number']