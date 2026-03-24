from django.contrib import admin
from .models import QRCode


@admin.register(QRCode)
class QRCodeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "catalog",
        "img",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "catalog__name",
        "img",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "catalog",
    )

    fieldsets = (
        ("Informações do QR Code", {
            "fields": (
                "catalog",
                "img",
            )
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )