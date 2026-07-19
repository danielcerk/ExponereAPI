from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.utils.text import slugify

from api.utils import validate_not_empty_url
from api.category.models import BusinessCategory

from urllib.parse import urlparse

import re

from decimal import Decimal

User = get_user_model()

class Catalog(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False, related_name="owned_catalogs")

    name = models.CharField(

        verbose_name='Nome da empresa', max_length=155,
        null=True, blank=True, default='catalogo'

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
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name="Valor mínimo por pedido"
    )

    minimum_order_value_free_shipping = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal("0.01"))],
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

            while Catalog.objects.filter(slug=slug).exclude(pk=self.pk).exists():

                slug = f"{base_slug}-{slugify(self.user.username)}"

            self.slug = slug

        super().save(*args, **kwargs)

    def __str__(self):

        return f'Catálogo de {self.user.username}'
    
class Link(models.Model):

    SOCIAL_CHOICES = (
        ("instagram", "Instagram"),
        ("facebook", "Facebook"),
        ("tiktok", "TikTok"),
        ("youtube", "YouTube"),
        ("linkedin", "LinkedIn"),
        ("x", "X/Twitter"),
        ("whatsapp", "WhatsApp"),
        ("site", "Site"),
        ("outro", "Outro"),
    )

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name='Catalogo',
        related_name='links'
    )

    url = models.URLField(
        "Link da rede social",
        default='https://exponere.com.br',
        null=False,
        blank=False,
        validators=[validate_not_empty_url]
    )

    social_name = models.CharField(
        max_length=20,
        choices=SOCIAL_CHOICES,
        blank=True,
        verbose_name='Rede social'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def detect_social_network(self):

        try:

            hostname = (urlparse(self.url).hostname or "").lower()

        except Exception:

            return "site"

        hostname = hostname.removeprefix("www.")

        domains = {
            "instagram": [
                "instagram.com",
            ],
            "facebook": [
                "facebook.com",
                "fb.com",
            ],
            "tiktok": [
                "tiktok.com",
            ],
            "youtube": [
                "youtube.com",
                "youtu.be",
            ],
            "linkedin": [
                "linkedin.com",
            ],
            "x": [
                "x.com",
                "twitter.com",
            ],
            "whatsapp": [
                "whatsapp.com",
                "wa.me",
            ],
        }

        for social, hosts in domains.items():
            if any(
                hostname == host or hostname.endswith(f".{host}")
                for host in hosts
            ):
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