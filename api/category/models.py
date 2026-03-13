from django.db import models
from django.utils.text import slugify

from api.catalog.models import Catalog

class BusinessCategory(models.Model):

    name = models.CharField(

        verbose_name='Categoria da Empresa', max_length=155,
        null=True, blank=True

    )

    slug = models.SlugField(

        unique=True, blank=True,
        null=True, max_length=255

    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.slug and self.name:

            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1

            while Catalog.objects.filter(slug=slug).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name

class Category(models.Model):

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='Catalogo',
    )

    name = models.CharField(
        verbose_name="Nome",
        max_length=255,
        unique=True,
    )

    slug = models.SlugField(
        verbose_name="Slug",
        max_length=255,
        unique=True,
        blank=True,
    )

    is_active = models.BooleanField(
        verbose_name="Ativa",
        default=True,
        help_text="Define se a categoria está visível no sistema.",
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True,
    )

    class Meta:

        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ["name"]
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["is_active"]),
        ]

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name