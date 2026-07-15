from django.contrib import admin

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "user",
        "short_message",
        "created_at",
    )

    list_display_links = (
        "email",
    )

    search_fields = (
        "email",
        "message",
        "user__username",
        "user__email",
        "user__first_name",
        "user__last_name",
    )

    list_filter = (
        "created_at",
        "user",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "user",
    )

    fieldsets = (
        (
            "Informações",
            {
                "fields": (
                    "user",
                    "email",
                    "message",
                ),
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description="Feedback")
    def short_message(self, obj):
        if len(obj.message) > 80:
            return f"{obj.message[:80]}..."
        return obj.message