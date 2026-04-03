from django.contrib import admin
from .models import Order, ProductOrder


class ProductOrderInline(admin.TabularInline):
    model = ProductOrder
    extra = 0
    autocomplete_fields = ['wishlist_product']
    readonly_fields = ['created_at', 'updated_at']
    show_change_link = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'customer',
        'catalog',
        'subtotal',
        'discount',
        'total',
        'is_paid',
        'payment_method',
        'created_at',
    )

    list_filter = (
        'is_paid',
        'payment_method',
        'created_at',
        'catalog',
    )

    search_fields = (
        'id',
        'customer__full_name',
        'customer__email',
        'catalog__name',
    )

    autocomplete_fields = [
        'customer',
        'catalog',
        'coupon',
    ]

    readonly_fields = (
        'subtotal',
        'discount',
        'total',
        'created_at',
        'updated_at',
    )

    inlines = [ProductOrderInline]

    date_hierarchy = 'created_at'

    ordering = ('-updated_at',)


@admin.register(ProductOrder)
class ProductOrderAdmin(admin.ModelAdmin):
    
    list_display = (
        'id',
        'order',
        'wishlist_product',
        'created_at',
    )

    list_filter = (
        'created_at',
        'order__catalog',
    )

    search_fields = (
        'order__id',
        'wishlist_product__product__name',
    )

    autocomplete_fields = [
        'order',
        'wishlist_product',
    ]

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)