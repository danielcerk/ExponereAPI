from django.db import models
from api.order.models import Order


class NF(models.Model):

    order = models.OneToOneField(
        Order,
        verbose_name="Pedido",
        related_name="nf",
        on_delete=models.CASCADE,
        db_index=True,
        help_text="Pedido relacionado a esta nota fiscal."
    )

    number = models.CharField(
        verbose_name="Número da nota fiscal",
        max_length=50,
        blank=True,
        null=True,
        db_index=True,
        help_text="Número identificador da nota fiscal."
    )

    access_key = models.CharField(
        verbose_name="Chave de acesso",
        max_length=44,
        blank=True,
        null=True,
        unique=True,
        db_index=True
    )

    file_url = models.URLField(
        verbose_name="Arquivo da nota fiscal",
        blank=True,
        null=True,
        help_text="URL do PDF ou XML da nota fiscal."
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True
    )

    class Meta:
        
        verbose_name = "Nota Fiscal"
        verbose_name_plural = "Notas Fiscais"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["number"]),
        ]

    def __str__(self):

        if self.number:

            return f"NF {self.number} - Pedido {self.order_id}"
        
        return f"NF do Pedido {self.order_id}"
