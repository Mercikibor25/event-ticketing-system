from django.urls import path
from . import views

urlpatterns = [
    path('initiate/', views.InitiatePaymentView.as_view(), name='initiate-payment'),
    path('callback/', views.MpesaCallbackView.as_view(), name='mpesa-callback'),
    path('history/', views.PaymentHistoryView.as_view(), name='payment-history'),
]