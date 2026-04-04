from django.db import models

from django.utils.text import slugify

class Carrier(models.Model):

    '''

        Models para que o lojista defina todos as transportadoras com
        que ele vai trabalhar , por exemplo, J&F, Jadlog, etc. Models para criação
        apenas de superusuários

    
    '''

    name = models.CharField(max_length=255, unique=True)

    slug = models.SlugField(

        unique=True, max_length=100,
        null=True, blank=True

    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True
        
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True
    )

    def save(self, *args, **kwargs):

        base_slug = slugify(self.name)
        slug = base_slug
        counter = 1

        while Carrier.objects.exclude(pk=self.pk).filter(slug=slug).exists():

            slug = f'{base_slug}-{counter}'
            counter += 1

        self.slug = slug

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = "Transportadora"
        verbose_name_plural = "Transportadoras"

        ordering = ["-updated_at"]

class ShippingStatus(models.Model):

    '''

        Vamos puxar os dados de uma API

        Esse models servirá para armazenar os dados e atualizações da entrega como
        order, código, status ( Está indo pra SP, por ex, vai variar da API de busca ), etc

    
    '''

    class StatusChoices(models.TextChoices):
        
        PENDING = "pending", "Pendente"
        IN_TRANSIT = "in_transit", "Em trânsito"
        OUT_FOR_DELIVERY = "out_for_delivery", "Saiu para entrega"
        DELIVERED = "delivered", "Entregue"
        FAILED = "failed", "Falha na entrega"
        RETURNED = "returned", "Devolvido"

    order = models.ForeignKey(
        "order.Order", 
        on_delete=models.CASCADE,
        related_name="shipping_statuses",
        verbose_name="Pedido"
    )

    tracking_code = models.CharField(
        max_length=255,
        verbose_name="Código de rastreio",
        db_index=True
    )

    status = models.CharField(
        max_length=50,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
        verbose_name="Status"
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição do status"
    )

    location = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Localização (ex: São Paulo - SP)"
    )

    raw_response = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Resposta bruta da API"
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True
    )

    class Meta:

        verbose_name = "Status de entrega"
        verbose_name_plural = "Status de entregas"

        ordering = ["-updated_at"]

    def __str__(self):

        return f"{self.order} - {self.get_status_display()} ({self.tracking_code})"
