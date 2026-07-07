from django.contrib import admin

from .models import AuthorPlugin, Plugin


@admin.register(AuthorPlugin)
class AuthorPluginAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "created_at",
        "updated_at",
    )

    search_fields = ("name",)
    ordering = ("name",)
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informações do autor", {
            "fields": ("name",)
        }),
        ("Datas", {
            "fields": ("created_at", "updated_at")
        }),
    )


@admin.register(Plugin)
class PluginAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "author",
        "catalog",
        "is_active",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "author__name",
        "catalog__name",
        "catalog__slug",
    )

    list_filter = (
        "author",
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "author",
        "catalog",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    ordering = ("name",)

    fieldsets = (
        ("Informações do plugin", {
            "fields": (
                "name",
                "author",
                "catalog",
            )
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )