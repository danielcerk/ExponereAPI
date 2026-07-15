from django.contrib import admin

from .models import Launch


@admin.register(Launch)
class LaunchAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "whatsapp",
        "created_at",
    )

    list_display_links = (
        "name",
        "email",
    )

    search_fields = (
        "name",
        "email",
        "whatsapp",
    )

    list_filter = (
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Informações",
            {
                "fields": (
                    "name",
                    "email",
                    "whatsapp",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )