from django.contrib import admin
from .models import NF


@admin.register(NF)
class NFAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "order",
        "number",
        "access_key",
        "file_url",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "order",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    search_fields = (
        "order__id",
        "number",
        "access_key",
    )

    ordering = (
        "-created_at",
    )

    date_hierarchy = "created_at"

    list_per_page = 25

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "order",
    )

    fieldsets = (
        ("Informações da Nota Fiscal", {
            "fields": (
                "order",
                "number",
                "access_key",
                "file_url",
            ),
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            ),
            "classes": ("collapse",),
        }),
    )

    save_on_top = True

    def get_queryset(self, request):

        qs = super().get_queryset(request)

        return qs.select_related("order")
