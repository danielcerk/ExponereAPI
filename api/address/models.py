from django.db import models

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .utils import ( 
    
    verify_cep, 
    validate_no_repeated_digits,
    get_cities,
    get_states

)

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

    city = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Cidade",
        choices=get_cities()
    )

    state = models.CharField(
        max_length=2,
        null=True,
        blank=True,
        verbose_name="UF",
        choices=get_states()
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

            try:

                address = verify_cep(self.cep)

                if not address or address.get("erro") == "true":

                    raise ValidationError({"cep": "CEP inválido ou não encontrado."})

                self.street = address.get("logradouro")
                self.neighborhood = address.get("bairro")

                city_obj = get_cities(name=address.get("localidade"))

                if city_obj:

                    self.city = city_obj["Nome"]

                state_obj = get_states(UF=address.get("uf"))

                if state_obj:

                    self.state = state_obj["Uf"]

            except Exception as e:
                
                raise ValidationError({
                    "cep": f"Erro ao validar CEP: {str(e)}"
                })

        parts = [
            self.street,
            self.neighborhood,
            self.complement,
            self.city,
            self.state,
            self.cep
        ]

        self.full_address = ", ".join(filter(None, parts))

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = 'Endereço'
        verbose_name_plural = 'Endereços'

    def __str__(self):

        return f'Endereço completo: {self.full_address}'
