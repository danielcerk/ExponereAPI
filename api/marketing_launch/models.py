from django.db import models

from django.core.validators import RegexValidator
from django.utils.text import slugify


class CampaignMarketingLaunch(models.Model):

    name = models.CharField(
        verbose_name="Nome",
        max_length=255,
        unique=True
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        blank=True
    )

    description = models.TextField(
        verbose_name="Descrição",
        blank=True
    )

    file_url = models.URLField(
        verbose_name="URL do material",
        max_length=1000
    )

    is_active = models.BooleanField(
        verbose_name="Ativa",
        default=True
    )

    starts_at = models.DateTimeField(
        verbose_name="Início da campanha",
        null=True,
        blank=True
    )

    ends_at = models.DateTimeField(
        verbose_name="Fim da campanha",
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = "Campanha de Marketing"
        verbose_name_plural = "Campanhas de Marketing"
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):

        if not self.slug:

            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):

        return self.name

class MarketingLaunch(models.Model):

    class RevenueChoices(models.TextChoices):
        
        UP_TO_5K = "UP_TO_5K", "Até R$ 5 mil/mês"
        FROM_5K_TO_10K = "FROM_5K_TO_10K", "De R$ 5 mil a R$ 10 mil/mês"
        FROM_10K_TO_30K = "FROM_10K_TO_30K", "De R$ 10 mil a R$ 30 mil/mês"
        FROM_30K_TO_50K = "FROM_30K_TO_50K", "De R$ 30 mil a R$ 50 mil/mês"
        FROM_50K_TO_100K = "FROM_50K_TO_100K", "De R$ 50 mil a R$ 100 mil/mês"
        FROM_100K_TO_300K = "FROM_100K_TO_300K", "De R$ 100 mil a R$ 300 mil/mês"
        ABOVE_300K = "ABOVE_300K", "Acima de R$ 300 mil/mês"

    name = models.CharField(max_length=255)

    email = models.EmailField(max_length=255)

    whatsapp = models.CharField(
        verbose_name="WhatsApp",
        max_length=20,
        blank=False,
        null=False
    )

    monthly_revenue = models.CharField(
        verbose_name="Faturamento mensal",
        max_length=30,
        choices=RevenueChoices.choices,
        blank=False,
        null=False
    )

    campaign_marketing = models.ForeignKey(
        CampaignMarketingLaunch,
        on_delete=models.CASCADE,
        related_name="leads",
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        
        verbose_name = "Lead de Marketing"
        verbose_name_plural = "Leads de Marketing"

    def __str__(self):

        return self.email
    

