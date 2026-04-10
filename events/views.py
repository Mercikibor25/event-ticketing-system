from django.shortcuts import render

# Create your views here.
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Event
from .serializers import EventSerializer

class IsAdminUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

class EventListView(generics.ListAPIView):
    """Anyone can view events"""
    queryset = Event.objects.filter(status__in=['upcoming', 'ongoing'])
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class EventDetailView(generics.RetrieveAPIView):
    """Anyone can view a single event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

class EventCreateView(generics.CreateAPIView):
    """Only admin users can create events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save(
            organizer=self.request.user,
            available_tickets=serializer.validated_data['total_capacity']
        )

class EventUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    """Only admin users can edit or delete events"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminUser]