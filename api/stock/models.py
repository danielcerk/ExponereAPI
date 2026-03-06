from django.db import models
from django.core.exceptions import ValidationError

from api.product.models import Product

class Stock(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="stocks",
        db_index=True,
        verbose_name="Produto"
    )

    batch = models.CharField(
        max_length=255,
        verbose_name="Lote",
        null=True,
        blank=True,
        db_index=True
    )

    serial_number = models.CharField(
        max_length=255,
        verbose_name="Número de série",
        null=True,
        blank=True,
        db_index=True
    )

    quantity_now = models.PositiveBigIntegerField(
        verbose_name="Quantidade atual",
        null=True,
        default=0
    )

    quantity_min = models.PositiveBigIntegerField(
        verbose_name="Quantidade mínima",
        null=True,
        default=0
    )

    quantity_max = models.PositiveBigIntegerField(
        verbose_name="Quantidade máxima",
        null=True,
        default=0
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

        if self.batch:

            return f"{self.product.name} - Lote {self.batch}"
        
        if self.serial_number:

            return f"{self.product.name} - SN {self.serial_number}"
        
        return f"Estoque de {self.product.name}"

    def clean(self):

        if self.quantity_min is not None and self.quantity_max is not None:

            if self.quantity_min > self.quantity_max:

                raise ValidationError(

                    {"quantity_min": "Quantidade mínima não pode ser maior que a máxima."}

                )

        if self.quantity_now is not None and self.quantity_max is not None:

            if self.quantity_now > self.quantity_max:

                raise ValidationError(

                    {"quantity_now": "Quantidade atual não pode ultrapassar a quantidade máxima."}

                )

    @property
    def is_below_minimum(self):

        if self.quantity_now is None or self.quantity_min is None:

            return False
        
        return self.quantity_now < self.quantity_min

    @property
    def is_above_maximum(self):

        if self.quantity_now is None or self.quantity_max is None:

            return False
        
        return self.quantity_now > self.quantity_max

    @property
    def needs_restock(self):

        return self.is_below_minimum

    class Meta:

        verbose_name = "Estoque de Produto"
        verbose_name_plural = "Estoques de Produtos"
        ordering = ["-updated_at"]

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["batch"]),
            models.Index(fields=["serial_number"]),
        ]

        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity_now__gte=0),
                name="stock_quantity_now_positive"
            ),
            models.CheckConstraint(
                check=models.Q(quantity_min__gte=0),
                name="stock_quantity_min_positive"
            ),
            models.CheckConstraint(
                check=models.Q(quantity_max__gte=0),
                name="stock_quantity_max_positive"
            ),
        ]

class StockMovement(models.Model):

    class MovementType(models.TextChoices):
        
        PURCHASE = "purchase", "Compra"
        SALE = "sale", "Venda"
        ADJUSTMENT = "adjustment", "Ajuste"
        RETURN = "return", "Devolução"

    stock = models.ForeignKey(
        Stock,
        on_delete=models.CASCADE,
        related_name="stocks_mov",
        db_index=True,
        verbose_name="Estoque"
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
        verbose_name="Tipo de movimentação",
        db_index=True
    )

    quantity_moved = models.PositiveBigIntegerField(
        verbose_name="Quantidade movimentada",
        default=0
    )

    observation = models.TextField(
        verbose_name="Observação",
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

    def __str__(self):

        return f"{self.get_movement_type_display()} - {self.stock.product.name} ({self.quantity_moved})"

    def apply_movement(self):

        stock = self.stock
        qty = self.quantity_moved

        if self.movement_type == self.MovementType.PURCHASE:

            stock.quantity_now += qty

        elif self.movement_type == self.MovementType.RETURN:

            stock.quantity_now += qty

        elif self.movement_type == self.MovementType.SALE:

            if stock.quantity_now < qty:

                raise ValidationError("Estoque insuficiente para venda.")
            
            stock.quantity_now -= qty

        elif self.movement_type == self.MovementType.ADJUSTMENT:

            stock.quantity_now = qty

        stock.save(update_fields=["quantity_now", "updated_at"])

    def save(self, *args, **kwargs):

        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:

            self.apply_movement()

    class Meta:

        verbose_name = "Movimentação de Estoque"
        verbose_name_plural = "Movimentações de Estoques"
        ordering = ["-created_at"]

        indexes = [
            models.Index(fields=["movement_type"]),
            models.Index(fields=["created_at"]),
        ]