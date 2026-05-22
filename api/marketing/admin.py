from django.contrib import admin

from .models import (

    TagManager,
    MetaPixel,
    GA4

)

@admin.register(TagManager)
class TagManagerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "catalog",
        "container_id",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "container_id",
        "catalog__name",
        "catalog__slug",
    )

    list_filter = (
        "is_active",
        "created_at",
        "author",
    )

    autocomplete_fields = (
        "author",
        "catalog",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_editable = ("is_active",)

    fieldsets = (
        ("Configuração GTM", {
            "fields": (
                "name",
                "author",
                "catalog",
                "container_id",
                "is_active",
            )
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(MetaPixel)
class MetaPixelAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "catalog",
        "pixel_id",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "pixel_id",
        "catalog__name",
        "catalog__slug",
    )

    list_filter = (
        "is_active",
        "created_at",
        "author",
    )

    autocomplete_fields = (
        "author",
        "catalog",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_editable = ("is_active",)

    fieldsets = (
        ("Configuração Meta Pixel", {
            "fields": (
                "name",
                "author",
                "catalog",
                "pixel_id",
                "is_active",
            )
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )


@admin.register(GA4)
class GA4Admin(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "catalog",
        "measurement_id",
        "property_id",
        "is_active",
        "created_at",
    )

    search_fields = (
        "name",
        "measurement_id",
        "property_id",
        "catalog__name",
        "catalog__slug",
    )

    list_filter = (
        "is_active",
        "created_at",
        "author",
    )

    autocomplete_fields = (
        "author",
        "catalog",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_editable = ("is_active",)

    fieldsets = (
        ("Configuração Google Analytics 4", {
            "fields": (
                "name",
                "author",
                "catalog",
                "measurement_id",
                "property_id",
                "is_active",
            )
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )
