from django.contrib import admin
from django.utils.html import format_html
from django.utils.timezone import now

from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "title",
        "user",
        "catalog",
        "type_notification",
        "is_read",
        "created_at",
        "colored_status",
    )

    list_filter = (
        "type_notification",
        "is_read",
        "created_at",
    )

    search_fields = (
        "title",
        "message",
        "user__email",
        "user__username",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "read_at",
    )

    autocomplete_fields = (
        "user",
        "catalog",
    )

    list_per_page = 25

    ordering = ("-created_at",)

    fieldsets = (
        ("Informações principais", {
            "fields": (
                "title",
                "message",
                "type_notification",
            )
        }),
        ("Relacionamentos", {
            "fields": (
                "user",
                "catalog",
            )
        }),
        ("Ação", {
            "fields": (
                "action_url",
                "payload",
            )
        }),
        ("Status", {
            "fields": (
                "is_read",
                "read_at",
            )
        }),
        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    actions = [
        "mark_as_read",
        "mark_as_unread",
    ]

    @admin.action(description="Marcar como lida")
    def mark_as_read(self, request, queryset):

        queryset.update(is_read=True, read_at=now())

    @admin.action(description="Marcar como não lida")
    def mark_as_unread(self, request, queryset):

        queryset.update(is_read=False, read_at=None)

    def colored_status(self, obj):

        if obj.is_read:

            return format_html(

                '<span style="color: green; font-weight: bold;">Lida</span>'

            )
        
        return format_html(

            '<span style="color: red; font-weight: bold;">Não lida</span>'

        )

    colored_status.short_description = "Status"