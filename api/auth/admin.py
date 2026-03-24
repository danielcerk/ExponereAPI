from django.contrib import admin
from .models import UserProfile, Profile, PasswordReset

from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import admin

@admin.register(UserProfile)
class UserProfileModelAdmin(admin.ModelAdmin):

    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'is_superuser', 'is_staff', 'is_active',
        'created_at', 'updated_at'
    )

    list_filter = (
        'is_superuser', 'is_staff', 'is_active'
    )

    search_fields = (
        'username',
        'first_name',
        'last_name',
        'email',
    )


@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):

    list_display = (
        'user', 'slug', 'cpf_cnpj', 'whatsapp'
    )

@admin.register(PasswordReset)
class PasswordResetAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "user",
        "token",
        "is_used",
        "created_at",
        "expires_at",
        "used_at",
    )

    list_filter = (
        "is_used",
        "created_at",
        "expires_at",
    )

    search_fields = (
        "email",
        "user__email",
        "token",
    )

    ordering = ("-created_at",)

    readonly_fields = (
        "token",
        "created_at",
        "used_at",
        "ip_address",
        "user_agent",
    )

    fieldsets = (
        ("User Information", {
            "fields": ("user", "email")
        }),
        ("Token", {
            "fields": ("token", "is_used", "expires_at", "used_at")
        }),
        ("Request Metadata", {
            "fields": ("ip_address", "user_agent")
        }),
        ("Timestamps", {
            "fields": ("created_at",)
        }),
    )