from django.db import models

from django.utils.text import slugify

class AnalyticRoute(models.Model):

    catalog = models.ForeignKey(
        "catalog.Catalog",
        on_delete=models.CASCADE,
        verbose_name="Catalogo",
    )

    slug = models.SlugField(

        unique=True, blank=True,
        null=True, max_length=255

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

        verbose_name = 'Análise de view de Catálogo'
        verbose_name_plural = 'Análises de views de Catálogos'

    def __str__(self):

        return f"Análise de view - {self.catalog.name}"