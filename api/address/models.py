from django.db import models

from cities_light.models import SubRegion, Region

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .utils import verify_cep, validate_no_repeated_digits

class Address(models.Model):

    street = models.CharField(
        null=True, blank=True,
        verbose_name='Rua',
        max_length=255
    )

    neighborhood = models.CharField(
        null=True, blank=True,
        verbose_name='Bairro',
        max_length=255
    )

    cep = models.CharField(
        max_length=8,
        verbose_name='CEP',
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                regex=r'^\d{8}$',
                message='O CEP deve conter exatamente 8 números (sem hífen ou letras).'
            ),
            validate_no_repeated_digits
        ]
    )

    complement = models.TextField(
        null=True, blank=True,
        verbose_name='Complemento'
    )

    city = models.ForeignKey(
        SubRegion,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Cidade'
    )

    state = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        verbose_name='Estado'
    )

    full_address = models.CharField(
        verbose_name='Endereço completo',
        null=True, blank=True,
        max_length=255
    )

    def clean(self):

        if self.cep:
            cleaned = ''.join(filter(str.isdigit, self.cep))

            if not cleaned:
                raise ValidationError({'cep': 'CEP inválido'})

            self.cep = cleaned

    def save(self, *args, **kwargs):

        self.full_clean()

        if self.cep:

            address = verify_cep(self.cep)

            if address:

                self.street = address['logradouro']
                self.neighborhood = address['bairro']

                region = Region.objects.filter(name=address['estado']).first()

                if region:

                    city_obj = SubRegion.objects.filter(
                        name=address['localidade'],
                        region=region
                    ).first()
                    
                else:
                    
                    city_obj = SubRegion.objects.filter(
                        name=address['localidade']
                    ).first()

                self.city = city_obj
                self.state = region

        parts = [
            self.street,
            self.neighborhood,
            self.complement,
            str(self.city) if self.city else None,
            str(self.state) if self.state else None,
            self.cep
        ]

        self.full_address = ', '.join(filter(None, parts))

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):

        return f'Endereço completo: {self.full_address}'
