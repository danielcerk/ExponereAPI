from django.db import models

from api.catalog.models import Catalog
from api.address.models import Address

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

from django.utils.text import slugify

class Customer(models.Model):

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        verbose_name="Catalogo",
    )

    session_key = models.CharField(
		max_length=40,
		null=True,
		blank=True,
		db_index=True
	)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    cpf_cnpj = models.CharField(
        verbose_name='CPF ou CNPJ',
        max_length=18,
        validators=[
            RegexValidator(
                regex=r'^(\d{3}\.\d{3}\.\d{3}-\d{2})$',
                message='Digite um CPF (XXX.XXX.XXX-XX)'
            )
        ],
        unique=True,
        null=True,
        blank=True
    )

    slug = models.SlugField(
        
        max_length=100,
        null=True, blank=True

    )
    whatsapp = models.CharField(
        verbose_name='WhatsApp',
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?55\d{10,11}$',
                message='Digite um número válido com DDD (ex: +5511999999999)'
            )
        ],
        null=True,
        blank=True
    )

    address = models.ForeignKey(
         
        Address, on_delete=models.SET_NULL,
        verbose_name='Endereço', null=True

    )

    is_integration = models.BooleanField(
        verbose_name="vem de uma integração?",
        default=True,
    )

    is_active = models.BooleanField(
        verbose_name="Cliente ativo",
        default=True,
    )

    created_at = models.DateTimeField(
        verbose_name="Criado em",
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        verbose_name="Atualizado em",
        auto_now=True,
    )

    def save(self, *args, **kwargs):

        self.slug = slugify(self.full_name)

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["full_name"]

    def __str__(self):

        return f'{self.catalog.name} - {self.full_name}'