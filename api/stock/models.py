from django.db import models, transaction
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from decimal import Decimal

from api.product.models import Product

class Stock(models.Model):

    product = models.OneToOneField(
        Product,
        verbose_name='Produto',
        on_delete=models.CASCADE,
        related_name='stocks',
        db_index=True,
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Quantidade disponível',
        default=0,
        validators=[MinValueValidator(0)]
    )

    reserved_quantity = models.PositiveIntegerField(
        verbose_name='Quantidade reservada',
        default=0,
        validators=[MinValueValidator(0)]
    )

    min_quantity = models.PositiveIntegerField(
        verbose_name='Quantidade mínima',
        default=0,
        validators=[MinValueValidator(0)]
    )

    max_quantity = models.PositiveIntegerField(
        verbose_name='Quantidade máxima',
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    is_active = models.BooleanField(
        verbose_name='Ativo',
        default=True
    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True
    )

    class Meta:
        verbose_name = 'Estoque'
        verbose_name_plural = 'Estoques'
        ordering = ['-updated_at']

    def clean(self):
        if self.reserved_quantity > self.quantity:
            raise ValidationError('Quantidade reservada não pode ser maior que a disponível.')

        if self.max_quantity is not None and self.quantity > self.max_quantity:
            raise ValidationError('Quantidade não pode ser maior que o máximo definido.')

    @property
    def available_quantity(self):
        return self.quantity - self.reserved_quantity

    def add(self, amount):
        if amount < 0:
            raise ValidationError('Quantidade inválida.')

        self.quantity += amount
        self.full_clean()
        self.save(update_fields=['quantity', 'updated_at'])

    def remove(self, amount):
        if amount < 0:
            raise ValidationError('Quantidade inválida.')

        if amount > self.available_quantity:
            raise ValidationError('Estoque insuficiente.')

        self.quantity -= amount
        self.full_clean()
        self.save(update_fields=['quantity', 'updated_at'])

    def reserve(self, amount):
        if amount < 0:
            raise ValidationError('Quantidade inválida.')

        if amount > self.available_quantity:
            raise ValidationError('Estoque insuficiente para reserva.')

        self.reserved_quantity += amount
        self.full_clean()
        self.save(update_fields=['reserved_quantity', 'updated_at'])

    def release(self, amount):
        if amount < 0:
            raise ValidationError('Quantidade inválida.')

        if amount > self.reserved_quantity:
            raise ValidationError('Quantidade a liberar maior que a reservada.')

        self.reserved_quantity -= amount
        self.full_clean()
        self.save(update_fields=['reserved_quantity', 'updated_at'])

    def __str__(self):
        return f'{self.product} - {self.available_quantity} disponíveis'


class StockMovement(models.Model):

    IN = 'IN'
    OUT = 'OUT'
    RESERVE = 'RESERVE'
    RELEASE = 'RELEASE'

    MOVEMENT_TYPE_CHOICES = [
        (IN, 'Entrada'),
        (OUT, 'Saída'),
        (RESERVE, 'Reserva'),
        (RELEASE, 'Liberação'),
    ]

    stock = models.ForeignKey(
        Stock,
        verbose_name='Estoque',
        on_delete=models.CASCADE,
        related_name='movements',
        db_index=True,
    )

    type = models.CharField(
        verbose_name='Tipo',
        max_length=10,
        choices=MOVEMENT_TYPE_CHOICES,
    )

    quantity = models.PositiveIntegerField(
        verbose_name='Quantidade',
        validators=[MinValueValidator(1)]
    )

    reference = models.CharField(
        verbose_name='Referência',
        max_length=255,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    class Meta:

        verbose_name = 'Movimentação de estoque'
        verbose_name_plural = 'Movimentações de estoque'
        ordering = ['-created_at']

    def clean(self):

        if self.quantity <= 0:

            raise ValidationError('Quantidade deve ser maior que zero.')

    def save(self, *args, **kwargs):

        with transaction.atomic():

            stock = self.stock

            if self.type == self.IN:

                stock.add(self.quantity)

            elif self.type == self.OUT:

                stock.remove(self.quantity)

            elif self.type == self.RESERVE:

                stock.reserve(self.quantity)

            elif self.type == self.RELEASE:

                stock.release(self.quantity)

            super().save(*args, **kwargs)

    def __str__(self):

        return f'{self.type} - {self.quantity} ({self.stock.product})'