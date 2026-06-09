from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'phone_number', 'national_id', 'kra_pin', 'role', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'role', 'national_id', 'kra_pin', 'taxpayer_name')}),
    )