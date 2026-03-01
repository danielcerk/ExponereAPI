from django.contrib import admin
from .models import CheckoutSessionRecord, Plan

from django.contrib import admin
from .models import Plan

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'lookup_key_plan',
        'price',
        'currency',
        'duration',
        'is_active',
        'created_at',
        'updated_at',
    )

    list_display_links = ('id', 'name')
    
    list_filter = (
        'duration',
        'is_active',
        'currency',
        'created_at',
    )

    search_fields = (
        'name',
        'description',
    )

    ordering = ('price',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Informações do Plano', {
            'fields': ('name','lookup_key_plan', 'description', 'price', 'currency', 'duration', 'is_active'),
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

    actions = ['ativar_planos', 'desativar_planos']

    def ativar_planos(self, request, queryset):

        count = queryset.update(is_active=True)

        self.message_user(request, f'{count} plano(s) ativado(s).')
        
    ativar_planos.short_description = 'Ativar planos selecionados'

    def desativar_planos(self, request, queryset):

        count = queryset.update(is_active=False)

        self.message_user(request, f'{count} plano(s) desativado(s).')

    desativar_planos.short_description = 'Desativar planos selecionados'


@admin.register(CheckoutSessionRecord)
class CheckoutSessionRecordAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'plan',
        'status',
        'has_access',
        'is_completed',
        'amount_total',
        'currency',
        'plan_start_date',
        'plan_end_date',
        'created_at',
        'updated_at',
    )

    list_display_links = ('id', 'user', 'status')

    list_filter = (
        'plan',
        'status',
        'has_access',
        'is_completed',
        'currency',
        'created_at',
        'plan_start_date',
        'plan_end_date',
    )

    search_fields = (
        'user__name',
        'user__email',
        'stripe_customer_id',
        'stripe_checkout_session_id',
        'stripe_subscription_id',
        'stripe_payment_intent_id',
    )

    ordering = ('-created_at',)

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user', 'has_access', 'is_completed', 'status'),
        }),
        ('Informações do Plano', {

            'fields': ('plan',)

        }),
        ('Stripe IDs', {
            'classes': ('collapse',),
            'fields': (
                'stripe_customer_id',
                'stripe_checkout_session_id',
                'stripe_price_id',
                'stripe_subscription_id',
                'stripe_payment_intent_id',
            ),
        }),
        ('Pagamento', {
            'fields': ('amount_total', 'currency'),
        }),
        ('Datas', {
            'fields': ('plan_start_date', 'plan_end_date', 'created_at', 'updated_at'),
        }),
    )

    actions = ['marcar_como_concluido', 'marcar_como_falhou']

    def marcar_como_concluido(self, request, queryset):
        count = 0
        for checkout in queryset:
            checkout.mark_as_completed()
            count += 1
        self.message_user(request, f'{count} checkout(s) marcados como concluído(s).')

    marcar_como_concluido.short_description = 'Marcar como concluído'

    def marcar_como_falhou(self, request, queryset):
        count = 0
        for checkout in queryset:
            checkout.mark_as_failed()
            count += 1
        self.message_user(request, f'{count} checkout(s) marcados como falho(s).')

    marcar_como_falhou.short_description = 'Marcar como falho'
