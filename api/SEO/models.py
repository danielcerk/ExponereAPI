from django.db import models
from django.utils.text import slugify

from api.catalog.models import Catalog

class Keyword(models.Model):

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name="Catálogo",
        related_name="keywords"
    )

    keyword = models.CharField(
        verbose_name="Palavra-chave",
        max_length=50
    )

    slug = models.SlugField(
        verbose_name="Slug",
        max_length=60,
        blank=True
    )

    is_active = models.BooleanField(
        verbose_name="Ativo",
        default=True
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

        return self.keyword

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.keyword)

        self.keyword = self.keyword.lower().strip()

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = "Palavra-chave"
        verbose_name_plural = "Palavras-chave"
        ordering = ["keyword"]

        constraints = [
            models.UniqueConstraint(
                fields=["catalog", "keyword"],
                name="unique_keyword_per_catalog"
            )
        ]

        indexes = [
            models.Index(fields=["keyword"]),
            models.Index(fields=["slug"]),
        ]