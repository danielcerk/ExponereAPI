from django.contrib import admin
from .models import Keyword


@admin.register(Keyword)
class KeywordAdmin(admin.ModelAdmin):

    list_display = (
        "keyword",
        "catalog",
        "is_active",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_active",
        "catalog",
        "created_at",
    )

    search_fields = (
        "keyword",
        "slug",
        "catalog__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    prepopulated_fields = {
        "slug": ("keyword",)
    }

    ordering = (
        "keyword",
    )