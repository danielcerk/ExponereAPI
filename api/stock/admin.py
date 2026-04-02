from django.contrib import admin

from .models import Stock, StockMovement

class StockMovementInline(admin.TabularInline):
    model = StockMovement
    extra = 0
    readonly_fields = (
        "type",
        "quantity",
        "reference",
        "created_at",
    )
    ordering = ("-created_at",)
    show_change_link = True


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "product",
        "quantity",
        "reserved_quantity",
        "available_quantity",
        "min_quantity",
        "max_quantity",
        "is_active",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "updated_at",
        "product__catalog",
    )

    search_fields = (
        "product__title",
        "product__slug",
        "product__catalog__name",
    )

    readonly_fields = (
        "available_quantity",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "product",
    )

    inlines = [StockMovementInline]

    ordering = ("-updated_at",)

    date_hierarchy = "updated_at"

    list_per_page = 25

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        return qs.select_related("product", "product__catalog")


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "stock",
        "type",
        "quantity",
        "reference",
        "created_at",
    )

    list_filter = (
        "type",
        "created_at",
        "stock__product__catalog",
    )

    search_fields = (
        "stock__product__title",
        "reference",
    )

    readonly_fields = (
        "created_at",
    )

    autocomplete_fields = (
        "stock",
    )

    ordering = ("-created_at",)

    date_hierarchy = "created_at"

    list_per_page = 25

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        return qs.select_related("stock", "stock__product")