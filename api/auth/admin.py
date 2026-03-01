from django.contrib import admin
from .models import UserProfile, Profile

from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib import admin

#admin.site.register(TOTPDevice)

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