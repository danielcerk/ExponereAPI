from django.contrib import admin

from .models import AnalyticRoute


@admin.register(AnalyticRoute)
class AnalyticRouteAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'catalog',
        'slug',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

    search_fields = (
        'slug',
        'catalog__name',
        'catalog__user__email',
        'catalog__user__username',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    ordering = ('-created_at',)

    fieldsets = (
        (
            'Informações principais',
            {
                'fields': (
                    'catalog',
                    'slug',
                )
            },
        ),
        (
            'Datas',
            {
                'fields': (
                    'created_at',
                    'updated_at',
                )
            },
        ),
    )