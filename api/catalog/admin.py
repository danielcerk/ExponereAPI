from django.contrib import admin
from django.utils.html import format_html

from .models import Catalog, Link

class LinkInline(admin.TabularInline):
    
    model = Link
    extra = 1
    readonly_fields = ("social_name", "created_at", "updated_at")
    fields = ("url", "social_name", "created_at", "updated_at")


@admin.register(Catalog)
class CatalogAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "photo_preview",
        "banner_preview",
        "created_at",
        "updated_at",
    )

    search_fields = ("user__username", "user__email")
    readonly_fields = ("slug", "created_at", "updated_at", "photo_preview", "banner_preview")

    inlines = [LinkInline]

    fieldsets = (
        ("Usuário", {
            "fields": ("user",)
        }),

        ("Imagens", {
            "fields": ("photo_img", "photo_preview", "banner_img", "banner_preview")
        }),

        ("Informações", {
            "fields": ("about", "slug")
        }),

        ("Datas", {
            "fields": ("created_at", "updated_at")
        }),
    )

    def photo_preview(self, obj):

        if obj.photo_img:

            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;border-radius:6px;" />',
                obj.photo_img
            )
        
        return "—"
    
    photo_preview.short_description = "Logo"

    def banner_preview(self, obj):

        if obj.banner_img:

            return format_html(
                '<img src="{}" width="120" height="40" style="object-fit:cover;border-radius:6px;" />',
                obj.banner_img
            )
        
        return "—"
    banner_preview.short_description = "Banner"


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):

    list_display = (
        "catalog",
        "social_name",
        "url",
        "created_at",
    )

    list_filter = ("social_name", "created_at")

    search_fields = (
        "catalog__user__username",
        "url",
    )

    readonly_fields = ("social_name", "created_at", "updated_at")

    fieldsets = (
        ("Relação", {
            "fields": ("catalog",)
        }),

        ("Link", {
            "fields": ("url", "social_name")
        }),

        ("Datas", {
            "fields": ("created_at", "updated_at")
        }),
    )