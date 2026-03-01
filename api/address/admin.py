from django.contrib import admin

from .models import Address

@admin.register(Address)
class AddressModelAdmin(admin.ModelAdmin):

    list_display = [

        'street', 'neighborhood', 'cep', 'city',
        'state', 'full_address'

    ]

    list_filter = [

        'city', 'state'

    ]