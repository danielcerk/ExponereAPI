from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "author",
        "is_published",
        "published_at",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "is_published",
        "published_at",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "subtitle",
        "content",
        "author",
        "slug",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "published_at",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    ordering = (
        "-published_at",
        "-created_at",
    )

    list_editable = (
        "is_published",
    )

    fieldsets = (
        ("Informações principais", {
            "fields": (
                "title",
                "subtitle",
                "slug",
                "author",
            )
        }),

        ("Conteúdo", {
            "fields": (
                "image",
                "content",
            )
        }),

        ("Publicação", {
            "fields": (
                "is_published",
                "published_at",
            )
        }),

        ("Datas do sistema", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )