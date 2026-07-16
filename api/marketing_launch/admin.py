from django.contrib import admin

from .models import CampaignMarketingLaunch, MarketingLaunch


@admin.register(CampaignMarketingLaunch)
class CampaignMarketingLaunchAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "slug",
        "is_active",
        "starts_at",
        "ends_at",
        "created_at",
    )

    list_display_links = (
        "name",
    )

    search_fields = (
        "name",
        "slug",
        "description",
    )

    list_filter = (
        "is_active",
        "created_at",
        "starts_at",
        "ends_at",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )


    fieldsets = (
        (
            "Informações",
            {
                "fields": (
                    "name",
                    "slug",
                    "description",
                )
            },
        ),
        (
            "Arquivos",
            {
                "fields": (
                    "file_url",
                )
            },
        ),
        (
            "Disponibilidade",
            {
                "fields": (
                    "is_active",
                    "starts_at",
                    "ends_at",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )


@admin.register(MarketingLaunch)
class MarketingLaunchAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "email",
        "whatsapp",
        "monthly_revenue",
        "campaign_marketing",
        "created_at",
    )

    list_display_links = (
        "name",
        "email",
    )

    search_fields = (
        "name",
        "email",
        "whatsapp",
        "campaign_marketing__name",
    )

    list_filter = (
        "monthly_revenue",
        "campaign_marketing",
        "created_at",
    )

    autocomplete_fields = (
        "campaign_marketing",
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (
            "Lead",
            {
                "fields": (
                    "name",
                    "email",
                    "whatsapp",
                    "monthly_revenue",
                    "campaign_marketing",
                )
            },
        ),
        (
            "Datas",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )