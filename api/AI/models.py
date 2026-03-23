from django.db import models

from api.catalog.models import Catalog
from api.product.models import Product

class CopyProduct(models.Model):

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='Catalogo',
    )

    product = models.ForeignKey(
        'Product',
        verbose_name='Produto',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='copies',
        db_index=True,
    )

    description = models.TextField(

        verbose_name='Descrição',
        null=False, blank=True

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

        verbose_name = 'Imagem de Anúncio'
        verbose_name_plural = 'Imagens de Anúncios'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['is_main']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):

        return f'Copy #{self.pk} do produto {self.product.title}'

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)