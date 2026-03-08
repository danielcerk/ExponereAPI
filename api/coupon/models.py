from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal

from api.catalog.models import Catalog


class Coupon(models.Model):

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name="Catálogo",
        related_name="coupons"
    )

    name = models.CharField(
        verbose_name="Nome do cupom",
        max_length=25,
        unique=True
    )

    code = models.CharField(
        verbose_name="Código do cupom",
        max_length=30,
        unique=True
    )

    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True
    )

    usage_limit = models.PositiveIntegerField(
        verbose_name="Limite total de usos",
        null=True,
        blank=True
    )

    usage_count = models.PositiveIntegerField(
        verbose_name="Quantidade utilizada",
        default=0
    )

    start_date = models.DateTimeField(
        verbose_name="Data de início",
        null=True,
        blank=True
    )

    end_date = models.DateTimeField(
        verbose_name="Data de expiração",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True
    )

    def is_valid(self):

        from django.utils import timezone

        now = timezone.now()

        if not self.is_active:

            return False

        if self.start_date and now < self.start_date:

            return False

        if self.end_date and now > self.end_date:

            return False

        if self.usage_limit and self.usage_count >= self.usage_limit:
            
            return False

        return True

    class Meta:

        abstract = True


class CouponProgressive(Coupon):

    min_purchase_value = models.DecimalField(
        verbose_name="Valor mínimo da compra",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    max_purchase_value = models.DecimalField(
        verbose_name="Valor máximo da compra",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.00"))]
    )

    percent_discount = models.DecimalField(
        verbose_name="Desconto percentual",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    class Meta:

        verbose_name = "Cupom Progressivo"
        verbose_name_plural = "Cupons Progressivos"
        ordering = ["-updated_at"]

    def calculate_discount(self, order_total):

        if order_total < self.min_purchase_value:

            return Decimal("0.00")

        if order_total > self.max_purchase_value:

            return Decimal("0.00")

        return order_total * (self.percent_discount / 100)


class CouponFixedValue(Coupon):

    discount_value = models.DecimalField(
        verbose_name="Valor do desconto",
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )

    min_purchase_value = models.DecimalField(
        verbose_name="Valor mínimo da compra",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = "Cupom com Valor Fixo"
        verbose_name_plural = "Cupons com Valores Fixos"
        ordering = ["-updated_at"]

    def calculate_discount(self, order_total):

        if self.min_purchase_value and order_total < self.min_purchase_value:

            return Decimal("0.00")

        return min(self.discount_value, order_total)


class CouponPercentValue(Coupon):

    percent_discount = models.DecimalField(
        verbose_name="Desconto percentual",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    min_purchase_value = models.DecimalField(
        verbose_name="Valor mínimo da compra",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    max_discount_value = models.DecimalField(
        verbose_name="Desconto máximo",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = "Cupom com Valor Percentual"
        verbose_name_plural = "Cupons com Valores Percentuais"
        ordering = ["-updated_at"]

    def calculate_discount(self, order_total):

        if self.min_purchase_value and order_total < self.min_purchase_value:

            return Decimal("0.00")

        discount = order_total * (self.percent_discount / 100)

        if self.max_discount_value:

            return min(discount, self.max_discount_value)

        return discount


class CouponFirstBuy(Coupon):

    percent_discount = models.DecimalField(
        verbose_name="Desconto percentual",
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    min_purchase_value = models.DecimalField(
        verbose_name="Valor mínimo da compra",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = "Cupom Primeira Compra"
        verbose_name_plural = "Cupons Primeira Compra"
        ordering = ["-updated_at"]

    def calculate_discount(self, order_total):

        if self.min_purchase_value and order_total < self.min_purchase_value:

            return Decimal("0.00")

        return order_total * (self.percent_discount / 100)