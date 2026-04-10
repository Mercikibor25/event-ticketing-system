from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.BookTicketView.as_view(), name='book-ticket'),
    path('my-tickets/', views.MyTicketsView.as_view(), name='my-tickets'),
    path('<int:pk>/', views.TicketDetailView.as_view(), name='ticket-detail'),
    path('validate/', views.ValidateTicketView.as_view(), name='validate-ticket'),
]