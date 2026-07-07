from django.contrib import admin
from .models import Customer

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "catalog",
        "cpf_cnpj",
        "whatsapp",
        "session_key",
        "is_integration",
        "is_active",
        "created_at",
    )

    list_display_links = ("id", "full_name")

    search_fields = (
        "full_name",
        "first_name",
        "last_name",
        "cpf_cnpj",
        "whatsapp",
        "session_key",
    )

    list_filter = (
        "is_active",
        "is_integration",
        "created_at",
        "catalog",
    )

    list_select_related = ("catalog", "address")

    ordering = ("-created_at",)

    readonly_fields = (
        "slug",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        ("Informações básicas", {
            "fields": (
                "catalog",
                ("first_name", "last_name"),
                "full_name",
                "slug",
                "session_key",
            )
        }),

        ("Documentos", {
            "fields": ("cpf_cnpj",)
        }),

        ("Contato", {
            "fields": (
                "whatsapp",
                "address",
            )
        }),

        ("Origem", {
            "fields": ("is_integration",)
        }),

        ("Status", {
            "fields": ("is_active",)
        }),

        ("Datas", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "catalog",
                "full_name",
                "cpf_cnpj",
                "whatsapp",
                "address",
                "is_integration",
                "is_active",
            ),
        }),
    )

    autocomplete_fields = ("catalog", "address")

    list_per_page = 25

    actions = ["activate_customers", "deactivate_customers"]

    @admin.action(description="Ativar clientes selecionados")
    def activate_customers(self, request, queryset):
        
        queryset.update(is_active=True)

    @admin.action(description="Desativar clientes selecionados")
    def deactivate_customers(self, request, queryset):

        queryset.update(is_active=False)

    def get_queryset(self, request):

        qs = super().get_queryset(request)
        
        return qs.select_related("catalog", "address")