from django.db import models

import re
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from django.utils.text import slugify

from api.category.models import BusinessCategory

User = get_user_model()

class Catalog(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)

    name = models.CharField(

        verbose_name='Nome da empresa', max_length=155,
        null=True, blank=True

    )

    slug = models.SlugField(

        unique=True, blank=True,
        null=True, max_length=255

    )

    photo_img = models.URLField(
        verbose_name='Logotipo da empresa',
        null=True, blank=True
    )

    banner_img = models.URLField(
        verbose_name='Foto do banner', null=True,
        blank=True
    )

    minimum_order_value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor mínimo por pedido"
    )

    minimum_order_value_free_shipping = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Valor mínimo por pedido para frete grátis"
    )

    business_category = models.ForeignKey(

        BusinessCategory,
        verbose_name='Categoria da Empresa',
        null=True, blank=True,
        on_delete=models.SET_NULL

    )

    about = models.TextField(default='Meu catálogo digital ; )')
    
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

        return f'Catálogo de {self.user.username}'
    
class OpeningHours(models.Model):

    WEEKDAY_CHOICES = (
        (0, "Segunda-feira"),
        (1, "Terça-feira"),
        (2, "Quarta-feira"),
        (3, "Quinta-feira"),
        (4, "Sexta-feira"),
        (5, "Sábado"),
        (6, "Domingo"),
    )

    catalog = models.ForeignKey(
        "Catalog",
        on_delete=models.CASCADE,
        related_name="opening_hours",
        verbose_name="Catálogo"
    )

    weekday = models.IntegerField(
        choices=WEEKDAY_CHOICES,
        verbose_name="Dia da semana"
    )

    open_time = models.TimeField(
        verbose_name="Abre às",
        null=True,
        blank=True
    )

    close_time = models.TimeField(
        verbose_name="Fecha às",
        null=True,
        blank=True
    )

    is_closed = models.BooleanField(
        default=False,
        verbose_name="Fechado neste dia"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = "Horário de funcionamento"
        verbose_name_plural = "Horários de funcionamento"

        ordering = ["weekday", "open_time"]
        
        unique_together = ("catalog", "weekday", "open_time")

    def __str__(self):

        return f"{self.catalog} - {self.get_weekday_display()}"
    
class Link(models.Model):

    SOCIAL_CHOICES = (
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("tiktok", "TikTok"),
        ("youtube", "YouTube"),
        ("linkedin", "LinkedIn"),
        ("x", "X/Twitter"),
        ("site", "Site"),
        ("outro", "Outro"),
    )

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='Catalogo',
        related_name='links'
    )

    url = models.URLField("Link da rede social", null=True, blank=True)

    social_name = models.CharField(
        max_length=20,
        choices=SOCIAL_CHOICES,
        blank=True,
        verbose_name='Rede social'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def detect_social_network(self):

        patterns = {

            "instagram": r"(https?:\/\/)?(www\.)?instagram\.com\/",
            "facebook": r"(https?:\/\/)?(www\.)?facebook\.com\/",
            "tiktok": r"(https?:\/\/)?(www\.)?tiktok\.com\/",
            "youtube": r"(https?:\/\/)?(www\.)?(youtube\.com|youtu\.be)\/",
            "linkedin": r"(https?:\/\/)?(www\.)?linkedin\.com\/",
            "x": r"(https?:\/\/)?(www\.)?(x\.com|twitter\.com)\/",

        }

        for social, pattern in patterns.items():

            if re.search(pattern, self.url):

                return social

        return "site"

    def clean(self):

        if not self.url:

            raise ValidationError("Informe uma URL válida")

    def save(self, *args, **kwargs):

        self.social_name = self.detect_social_network()

        super().save(*args, **kwargs)

    def __str__(self):

        return f"{self.get_social_name_display()} - {self.catalog}"