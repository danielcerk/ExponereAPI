from django.contrib import admin
from .models import Carrier, ShippingStatus

@admin.register(Carrier)
class CarrierAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "slug",
        "created_at",
        "updated_at",
    )

    list_display_links = ("id", "name")

    search_fields = (
        "name",
        "slug",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    ordering = ("-updated_at",)

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informações", {
            "fields": (
                "name",
                "slug",
            )
        }),

        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    list_per_page = 25

@admin.register(ShippingStatus)
class ShippingStatusAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "tracking_code",
        "status",
        "location",
        "updated_at",
    )

    list_filter = (
        "status",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "tracking_code",
        "order__id",
        "description",
        "location",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("-updated_at",)

    list_select_related = ("order",)

    date_hierarchy = "updated_at"

    fieldsets = (
        ("Informações principais", {
            "fields": (
                "order",
                "tracking_code",
                "status",
            )
        }),
        ("Detalhes do rastreio", {
            "fields": (
                "description",
                "location",
            )
        }),
        ("Dados da API", {
            "fields": (
                "raw_response",
            ),
            "classes": ("collapse",) 
        }),
        ("Controle", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def has_add_permission(self, request):

        return True

    def has_delete_permission(self, request, obj=None):

        return True