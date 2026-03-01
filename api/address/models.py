from django.db import models

from cities_light.models import SubRegion, Region

from .utils import verify_cep

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
        max_length=8, verbose_name='CEP',
        null=True, blank=True
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

    def save(self, *args, **kwargs):

        cep = self.cep
        address = verify_cep(cep)

        if cep and address:

            self.street = address['logradouro']
            self.neighborhood = address['bairro']

            region = Region.objects.filter(name=address['estado']).first()

            city_obj = None

            if region:

                city_obj = SubRegion.objects.filter(name=address['localidade'], region=region).first()

            else:

                city_obj = SubRegion.objects.filter(name=address['localidade']).first()

            self.city = city_obj
            self.state = region

        self.full_address = f'{self.street or ""}, {self.neighborhood or ""}, {self.complement or ""}, {self.city or ""}, {self.state or ""} - {cep or ""}'.strip(', -')

        super().save(*args, **kwargs)



    class Meta:

        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):

        return f'Endereço completo: {self.full_address}'
