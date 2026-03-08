from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator

from api.address.models import Address

'''

- Subtotal
- Desconto
- Valor total
- Forma de Pagamento, 
- Modelo da entrega

'''

class CustomerInfo(models.Model):

    session_key = models.CharField(
        max_length=40,
        null=True,
        blank=True,
        db_index=True,
        verbose_name="Session key"
    )

    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name="Primeiro nome"
    )

    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name="Último nome"
    )

    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Nome completo"
    )

    birth_date = models.DateField(
        verbose_name="Data de nascimento",
        null=True,
        blank=True
    )

    email = models.EmailField(
        max_length=255,
        unique=True,
        verbose_name="Email"
    )

    cpf = models.CharField(
        verbose_name="CPF",
        max_length=14,
        validators=[
            RegexValidator(
                regex=r'^\d{3}\.\d{3}\.\d{3}-\d{2}$',
                message="Digite um CPF válido (XXX.XXX.XXX-XX)"
            )
        ],
        unique=True,
        null=True,
        blank=True
    )

    whatsapp = models.CharField(
        verbose_name="WhatsApp",
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?55\d{10,11}$',
                message="Digite um número válido com DDD (ex: +5511999999999)"
            )
        ],
        null=True,
        blank=True
    )

    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        verbose_name="Endereço",
        null=True,
        blank=True,
        related_name="customers"
    )

    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True
    )

    def __str__(self):

        return self.full_name or self.email or "Cliente"

    def save(self, *args, **kwargs):

        if not self.full_name:

            name_parts = filter(None, [self.first_name, self.last_name])

            self.full_name = " ".join(name_parts)

        super().save(*args, **kwargs)

    @property
    def age(self):

        if not self.birth_date:

            return None

        today = timezone.now().date()
        age = today.year - self.birth_date.year

        if (today.month, today.day) < (self.birth_date.month, self.birth_date.day):

            age -= 1

        return age

    class Meta:

        verbose_name = "Informação do cliente"
        verbose_name_plural = "Informações dos clientes"
        ordering = ["-updated_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["cpf"]),
            models.Index(fields=["session_key"]),
        ]

class Order(models.Model):

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True
    )

    class Meta:

        verbose_name = "Pedido"
        verbose_name_plural = "Pedido"

        ordering = ["-updated_at"]