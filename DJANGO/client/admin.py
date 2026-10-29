from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Patient


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("OdontoNova", {"fields": ("phone",)}),
    )


@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'document_type',
        'document_number',
        'first_name',
        'last_name',
        'email',
        'phone',
        'created_at',
    )
    list_filter = ('document_type',)
    search_fields = ('document_number', 'first_name', 'last_name', 'email')