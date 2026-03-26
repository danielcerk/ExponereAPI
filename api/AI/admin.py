from django.contrib import admin
from .models import CopyProduct


@admin.register(CopyProduct)
class CopyProductAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'product',
        'catalog',
        'short_description',
        'created_at',
    )

    list_filter = (
        'catalog',
        'created_at',
    )

    search_fields = (
        'id',
        'product__title',
        'catalog__name',
        'description',
    )

    autocomplete_fields = [
        'product',
        'catalog',
    ]

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)

    date_hierarchy = 'created_at'

    def short_description(self, obj):

        if obj.description:

            return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
        
        return "-"
    
    short_description.short_description = "Descrição"