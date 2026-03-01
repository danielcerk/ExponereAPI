from django.db import models
from django.utils.text import slugify

from api.catalog.models import Catalog

# Alinhar com Estoque
# Alinhar com categorias

class Product(models.Model):

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='Catalogo',
    )

    title = models.CharField(

        verbose_name='Título', max_length=155,
        null=True, blank=True

    )

    slug = models.SlugField(

        unique=True, blank=True,
        null=True, max_length=100

    )

    description = models.TextField(

        verbose_name='Descrição',
        null=False, blank=True

    )

    is_active = models.BooleanField(

        default=True, verbose_name='Está ativo'

    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True
    )

class Image(models.Model):

    product = models.ForeignKey(
        'Product',
        verbose_name='Anúncio',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='images'
    )

    image = models.URLField(
        verbose_name='Foto',
        max_length=500,
        default='https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png'
    )

    is_main = models.BooleanField(
        verbose_name='Imagem principal',
        default=False,
        help_text='Define se esta é a imagem principal do anúncio.'
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
        ordering = ['order', '-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['is_main']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):

        if self.title:

            return self.title
        
        return f'Imagem #{self.pk}'

    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(self.title) if self.title else f'image-{self.pk or ""}'
            self.slug = base_slug

        super().save(*args, **kwargs)