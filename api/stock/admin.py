from django.contrib import admin

from .models import Stock, StockMovement, AlertProductStock

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
        "purchase_price",
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
    
@admin.register(AlertProductStock)
class AlertProductStockAdmin(admin.ModelAdmin):

    list_display = (
        'email',
        'product',
        'is_active',
        'notified',
        'is_pending_display',
        'created_at',
    )

    list_filter = (
        'is_active',
        'notified',
        'created_at',
    )

    search_fields = (
        'email',
        'product__title',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)

    list_select_related = ('product',)

    actions = (
        'activate_alerts',
        'deactivate_alerts',
        'mark_as_notified',
        'mark_as_not_notified',
    )

    fieldsets = (
        ('Informações principais', {
            'fields': ('email', 'product')
        }),
        ('Status', {
            'fields': ('is_active', 'notified')
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    def is_pending_display(self, obj):

        return obj.is_pending
    
    is_pending_display.boolean = True
    is_pending_display.short_description = 'Pendente'

    @admin.action(description='Ativar alertas selecionados')
    def activate_alerts(self, request, queryset):

        queryset.update(is_active=True)

    @admin.action(description='Desativar alertas selecionados')
    def deactivate_alerts(self, request, queryset):

        queryset.update(is_active=False)

    @admin.action(description='Marcar como notificado')
    def mark_as_notified(self, request, queryset):

        queryset.update(notified=True)

    @admin.action(description='Marcar como não notificado')
    def mark_as_not_notified(self, request, queryset):

        queryset.update(notified=False)