from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from decimal import Decimal

from api.catalog.models import Catalog
from api.customer.models import Customer
from api.wishlist.models import Wishlist
from api.coupon.models import Coupon


class Order(models.Model):

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name="Catalogo",
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name="Cliente",
        related_name="orders"
    )

    subtotal = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Subtotal"
    )

    coupon = models.ForeignKey(
        Coupon,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Cupom"
    )

    discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        verbose_name="Desconto"
    )

    total = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Total"
    )

    is_paid = models.BooleanField(
        default=False,
        verbose_name="Pago"
    )

    payment_method = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        verbose_name="Forma de pagamento"
    )

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
        verbose_name_plural = "Pedidos"
        ordering = ["-updated_at"]

    def __str__(self):

        return f'Pedido #{self.id} de {self.customer.full_name} - {self.catalog.name} às {self.created_at}'

    def calculate_totals(self):

        subtotal = sum(
            [(item.wishlist_product.price * item.wishlist_product.quantity) for item in self.items.all()]
        )

        discount = Decimal("0.00")

        if self.coupon and self.coupon.is_valid():

            discount = self.coupon.calculate_discount(subtotal)

        total = subtotal - discount

        self.subtotal = subtotal
        self.discount = discount
        self.total = total if total > 0 else Decimal("0.00")

    def save(self, *args, **kwargs):

        self.calculate_totals()
        
        super().save(*args, **kwargs)


class ProductOrder(models.Model):

    order = models.ForeignKey(
        Order,
        verbose_name='Pedido',
        on_delete=models.CASCADE,
        related_name='items',
        db_index=True,
    )

    wishlist_product = models.ForeignKey(
        Wishlist,
        verbose_name='Produto dos favoritos',
        on_delete=models.CASCADE,
        related_name='order_items',
        db_index=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True
    )

    class Meta:

        verbose_name = "Produto do pedido"
        verbose_name_plural = "Produtos dos pedidos"
        ordering = ["-created_at"]

    def __str__(self):

        return f'{self.wishlist_product} ({self.quantity}x)'