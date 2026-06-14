from django.contrib import admin

from .models import (
    CouponProgressive,
    CouponFixedValue,
    CouponPercentValue,
    CouponFirstBuy,
    CouponUsage,
    Coupon
)

@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "name",
        "code",
        "catalog",
        "is_active",
        "usage_count",
        "usage_limit",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "is_active",
        "catalog",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "catalog__name",
    )

    readonly_fields = (
        "usage_count",
        "created_at",
        "updated_at",
    )

    ordering = ("-updated_at",)

class BaseCouponAdmin(admin.ModelAdmin):

    list_display = (
        "name",
        "code",
        "catalog",
        "is_active",
        "usage_count",
        "usage_limit",
        "start_date",
        "end_date",
        "created_at",
    )

    list_filter = (
        "is_active",
        "catalog",
        "start_date",
        "end_date",
        "created_at",
    )

    search_fields = (
        "name",
        "code",
        "catalog__name",
    )

    readonly_fields = (
        "usage_count",
        "created_at",
        "updated_at",
    )

    ordering = ("-updated_at",)

    list_per_page = 25


@admin.register(CouponProgressive)
class CouponProgressiveAdmin(BaseCouponAdmin):

    list_display = BaseCouponAdmin.list_display + (
        "percent_discount",
        "min_purchase_value",
        "max_purchase_value",
    )


@admin.register(CouponFixedValue)
class CouponFixedValueAdmin(BaseCouponAdmin):

    list_display = BaseCouponAdmin.list_display + (
        "discount_value",
        "min_purchase_value",
    )


@admin.register(CouponPercentValue)
class CouponPercentValueAdmin(BaseCouponAdmin):

    list_display = BaseCouponAdmin.list_display + (
        "percent_discount",
        "min_purchase_value",
        "max_discount_value",
    )


@admin.register(CouponFirstBuy)
class CouponFirstBuyAdmin(BaseCouponAdmin):

    list_display = BaseCouponAdmin.list_display + (
        "percent_discount",
        "min_purchase_value",
    )

@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "coupon",
        "customer",
        "order",
        "created_at",
    )

    list_select_related = (
        "coupon",
        "customer",
        "order",
    )

    search_fields = (
        "coupon__code",
        "customer__full_name",
        "customer__email",
        "order__id",
    )

    list_filter = (
        "created_at",
        "coupon",
    )

    ordering = ("-created_at",)

    autocomplete_fields = (
        "coupon",
        "customer",
        "order",
    )

    readonly_fields = (
        "created_at",
    )

    date_hierarchy = "created_at"

    list_per_page = 25