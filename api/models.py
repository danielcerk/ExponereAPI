from django.db import models

from api.catalog.models import Catalog

class AuthorPlugin(models.Model):

    name = models.CharField(max_length=150, blank=True, null=True)

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True,
    )

    class Meta:

        verbose_name = "Autor do plugin"
        verbose_name_plural = "Autores dos plugins"
        ordering = ["name"]

class Plugin(models.Model):

    name = models.CharField(max_length=150, blank=True, null=True)

    author = models.ForeignKey(
        AuthorPlugin,
        on_delete=models.CASCADE,
        verbose_name="Autor",
    )

    is_active = models.BooleanField(

		default=False

	)

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name="Catalogo",
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

        verbose_name = "Plugin"
        verbose_name_plural = "Plugins"
        ordering = ["name"]