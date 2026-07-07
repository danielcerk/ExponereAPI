from django.contrib import admin
from .models import NewsletterEmail


@admin.register(NewsletterEmail)
class NewsletterEmailAdmin(admin.ModelAdmin):
    list_display = ("email", "created_at", "updated_at")
    search_fields = ("email",)
    list_filter = ("created_at", "updated_at")
    ordering = ("-created_at",)
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        ("Informações", {
            "fields": ("email",)
        }),
        ("Datas", {
            "fields": ("created_at", "updated_at")
        }),
    )