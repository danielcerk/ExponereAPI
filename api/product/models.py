from django.db import models
from django.utils.text import slugify

from api.catalog.models import Catalog
from api.category.models import Category

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

        blank=True,
        null=True, max_length=100

    )

    description = models.TextField(

        verbose_name='Descrição',
        null=False, blank=True

    )

    category = models.ManyToManyField(
        Category,
        verbose_name='Categorias',
        blank=True
        
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor mínimo por pedido para frete grátis"
    )

    promotional_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Preço promocional"
    )

    promotion_is_active = models.BooleanField(

        default=True, verbose_name='Preço promocional está ativo'

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

    def save(self, *args, **kwargs):

        if not self.slug and self.title:

            base_slug = slugify(self.title)
            slug = base_slug

            self.slug = slug

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

        ordering = ['-updated_at']

        indexes = [

            models.Index(fields=['catalog']),
            models.Index(fields=['title']),
            models.Index(fields=['slug']),
            models.Index(fields=['is_active'])

        ]

class ProductLogisticInfo(models.Model):

    class UnitOfMeasure(models.TextChoices):
        UNIT = "unit", "Unidade"
        KG = "kg", "Quilograma"
        G = "g", "Grama"
        L = "l", "Litro"
        ML = "ml", "Mililitro"
        M = "m", "Metro"
        CM = "cm", "Centímetro"

    class PackagingType(models.TextChoices):
        BOX = "box", "Caixa"
        BAG = "bag", "Saco"
        PALLET = "pallet", "Pallet"
        BOTTLE = "bottle", "Garrafa"
        UNIT = "unit", "Unidade"
        OTHER = "other", "Outro"

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="logistic_info",
        db_index=True,
        verbose_name="Produto"
    )

    weight = models.DecimalField(
        max_digits=10,
        decimal_places=3,
        null=True,
        blank=True,
        verbose_name="Peso"
    )

    height = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Altura"
    )

    width = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Largura"
    )

    length = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Comprimento"
    )

    volume = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        verbose_name="Volume"
    )

    unit_of_measure = models.CharField(
        max_length=20,
        choices=UnitOfMeasure.choices,
        null=True,
        blank=True,
        verbose_name="Unidade de medida",
        db_index=True
    )

    packaging_type = models.CharField(
        max_length=20,
        choices=PackagingType.choices,
        null=True,
        blank=True,
        verbose_name="Tipo de embalagem",
        db_index=True
    )

    quantity_per_box = models.PositiveIntegerField(
        null=True,
        blank=True,
        verbose_name="Quantidade por caixa"
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

        return f"Logística de {self.product.title}"

    @property
    def calculated_volume(self):

        if self.height and self.width and self.length:

            return self.height * self.width * self.length
        
        return None

    class Meta:

        verbose_name = "Informação p/ Logística do Produto"
        verbose_name_plural = "Informações p/ Logística dos Produtos"

        ordering = ["-updated_at"]

        indexes = [
            models.Index(fields=["product"]),
            models.Index(fields=["unit_of_measure"]),
            models.Index(fields=["packaging_type"]),
        ]

class Image(models.Model):

    product = models.ForeignKey(
        'Product',
        verbose_name='Produto',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='images',
        db_index=True,
    )

    image = models.URLField(
        verbose_name='Foto',
        max_length=500,
        default='https://upload.wikimedia.org/wikipedia/commons/a/a3/Image-not-found.png'
    )

    alt_text = models.TextField(

        verbose_name='Texto alternativo',
        null=True, blank=True

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
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['is_main']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):

        return f'Imagem #{self.pk}'

    def save(self, *args, **kwargs):

        self.alt_text = f'Foto de {self.product.title} da {self.product.catalog.name} localizado(a) em {self.product.catalog.user.address}'

        super().save(*args, **kwargs)