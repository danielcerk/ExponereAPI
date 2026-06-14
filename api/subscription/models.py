from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Plan(models.Model):
    
    class Duration(models.TextChoices):

        MONTHLY = 'monthly', 'Mensal'
        YEARLY = 'yearly', 'Anual'

    name = models.CharField(max_length=100, unique=True, help_text="Nome do plano (ex: Básico, Premium)")
    lookup_key_plan = models.CharField(max_length=100, unique=True, null=True, blank=True)

    description = models.TextField(blank=True, null=True, help_text="Descrição do plano")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Valor do plano em BRL")
    currency = models.CharField(max_length=10, default='BRL', help_text="Moeda do plano")

    duration = models.CharField(max_length=10, choices=Duration.choices, default=Duration.MONTHLY, help_text="Periodicidade do plano")

    is_active = models.BooleanField(default=True, help_text="Se o plano está disponível para assinaturas")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['price']

    def __str__(self):

        return f"{self.name} - {self.price} {self.currency}"

class CheckoutSessionRecord(models.Model):

    class PaymentStatus(models.TextChoices):

        PENDING = 'pending', 'Pendente'
        COMPLETED = 'completed', 'Concluído'
        FAILED = 'failed', 'Falhou'
        CANCELED = 'canceled', 'Cancelado'

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='checkout_sessions',
        help_text='O usuário que iniciou o checkout.'
    )

    plan = models.ForeignKey(

        Plan,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Plano do Usuário'

    )

    stripe_customer_id = models.CharField(
        max_length=255,
        help_text='ID do cliente no Stripe.'
    )

    stripe_checkout_session_id = models.CharField(
        max_length=255,
        help_text='ID da sessão de checkout no Stripe.'
    )

    stripe_price_id = models.CharField(
        max_length=255,
        help_text='ID do preço do produto/assinatura no Stripe.'
    )

    stripe_subscription_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='ID da assinatura no Stripe, se aplicável.'
    )

    stripe_payment_intent_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='ID do Payment Intent no Stripe.'
    )

    status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        help_text='Status do pagamento.'
    )

    has_access = models.BooleanField(
        default=False,
        help_text='Indica se o usuário ganhou acesso ao produto/serviço.'
    )

    is_completed = models.BooleanField(
        default=False,
        help_text='Indica se o fluxo de checkout foi finalizado.'
    )

    plan_start_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de início do plano.'
    )

    plan_end_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Data de fim do plano, caso o usuário cancele.'
    )

    amount_total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Valor total da compra (em BRL).'
    )

    currency = models.CharField(
        max_length=10,
        default='BRL',
        help_text='Moeda utilizada na transação.'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        
        verbose_name = 'Checkout'
        verbose_name_plural = 'Checkouts'
        ordering = ['-created_at']

    def __str__(self):

        return f'Checkout de {self.user.username} - {self.get_status_display()}'

    def mark_as_completed(self):

        self.status = self.PaymentStatus.COMPLETED

        self.has_access = True
        self.is_completed = True

        self.save(update_fields=['status', 'has_access', 'is_completed', 'updated_at'])

    def mark_as_failed(self):

        self.status = self.PaymentStatus.FAILED

        self.has_access = False
        self.is_completed = True

        self.save(update_fields=['status', 'has_access', 'is_completed', 'updated_at'])
