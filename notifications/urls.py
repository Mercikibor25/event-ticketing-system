from django.urls import path
from . import views

urlpatterns = [
    path('my-notifications/', views.NotificationListView.as_view(), name='my-notifications'),
    path('send-update/', views.SendEventUpdateView.as_view(), name='send-event-update'),
]