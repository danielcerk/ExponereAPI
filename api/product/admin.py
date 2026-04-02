from django.contrib import admin

from .models import Product, ProductLogisticInfo, Image


class ImageInline(admin.TabularInline):

    model = Image
    extra = 0

    fields = (
        "image",
        "is_main",
        "created_at",
        "updated_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


class ProductLogisticInfoInline(admin.StackedInline):

    model = ProductLogisticInfo
    extra = 0
    max_num = 1

    readonly_fields = (
        "created_at",
        "updated_at",
        "calculated_volume",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "catalog",
        "slug",
        "price",
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
        "title",
        "slug",
        "description",
        "catalog__name",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "catalog",
    )

    filter_horizontal = (
        "category",
        "subcategory"
    )

    inlines = [
        ProductLogisticInfoInline,
        ImageInline,
    ]

    prepopulated_fields = {
        "slug": ("title",)
    }

    ordering = (
        "-updated_at",
    )


@admin.register(ProductLogisticInfo)
class ProductLogisticInfoAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "weight",
        "height",
        "width",
        "length",
        "volume",
        "unit_of_measure",
        "packaging_type",
        "quantity_per_box",
        "updated_at",
    )

    list_filter = (
        "unit_of_measure",
        "packaging_type",
        "created_at",
    )

    search_fields = (
        "product__title",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "calculated_volume",
    )

    autocomplete_fields = (
        "product",
    )

    ordering = (
        "-updated_at",
    )


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    list_display = (
        "product",
        "alt_text",
        "is_main",
        "created_at",
    )

    list_filter = (
        "is_main",
        "created_at",
    )

    search_fields = (
        "product__title",
        "image",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    autocomplete_fields = (
        "product",
    )

    ordering = (
        "-created_at",
    )