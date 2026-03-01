from django.contrib import admin
from .models import Wishlist


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):

	list_display = (
		"id",
		"product",
		"session_key",
		"quantity",
		"is_active",
		"created_at",
		"updated_at",
	)

	list_display_links = (
		"id",
		"product",
	)

	list_filter = (
		"is_active",
		"created_at",
		"updated_at",
	)

	search_fields = (
		"product__name",
		"user__username",
		"session_key",
	)

	ordering = (
		"-created_at",
	)

	date_hierarchy = "created_at"

	list_per_page = 25

	readonly_fields = (
		"created_at",
		"updated_at",
	)

	autocomplete_fields = (
		"product",
	)

	fieldsets = (
		("Informações", {
			"fields": (
				"product",
				"quantity",
	
				"session_key",
				"is_active",
			),
		}),
		("Datas", {
			"fields": (
				"created_at",
				"updated_at",
			),
			"classes": ("collapse",),
		}),
	)

	save_on_top = True

	def get_queryset(self, request):
		
		qs = super().get_queryset(request)
		
		return qs.select_related("product", "user")