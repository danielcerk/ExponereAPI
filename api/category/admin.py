from django.contrib import admin
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "catalog",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_display_links = (
        "id",
        "name",
    )

    list_filter = (
        "is_active",
        "created_at",
        "updated_at",
        "catalog",
    )

    search_fields = (
        "name",
        "slug",
        "catalog__name",
    )

    ordering = (
        "name",
    )

    date_hierarchy = "created_at"

    list_per_page = 25

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "catalog",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    fieldsets = (
        ("Informações", {
            "fields": (
                "catalog",
                "name",
                "slug",
                "is_active",
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
        
        return qs.select_related("catalog")