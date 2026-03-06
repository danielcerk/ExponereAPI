from django.contrib import admin

from .models import Stock, StockMovement


class StockMovementInline(admin.TabularInline):

    model = StockMovement
    extra = 0
    readonly_fields = (
        "movement_type",
        "quantity_moved",
        "observation",
        "created_at",
        "updated_at",
    )
    can_delete = False
    show_change_link = True


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "batch",
        "serial_number",
        "quantity_now",
        "quantity_min",
        "quantity_max",
        "needs_restock",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "product__title",
        "batch",
        "serial_number",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "is_below_minimum",
        "is_above_maximum",
        "needs_restock",
    )

    autocomplete_fields = (
        "product",
    )

    inlines = [
        StockMovementInline
    ]

    ordering = (
        "-updated_at",
    )


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):

    list_display = (
        "stock",
        "movement_type",
        "quantity_moved",
        "created_at",
    )

    list_filter = (
        "movement_type",
        "created_at",
    )

    search_fields = (
        "stock__product__title",
        "observation",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "stock",
    )

    ordering = (
        "-created_at",
    )