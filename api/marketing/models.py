from django.db import models
from django.core.validators import RegexValidator

from api.models import Plugin

'''

    Módulo de Marketing:

    Responsável por centralizar e automatizar as ações de marketing da plataforma.
    Permitirá o agendamento de posts em redes sociais, organização de conteúdos,
    e, futuramente, a criação e gestão de campanhas completas.

    O módulo deve contemplar:

    - Agendamento e publicação de posts (Instagram, Facebook, etc.)
    - Criação e gerenciamento de campanhas de marketing
    - Integração com APIs de redes sociais
    - Gestão de mídia (imagens, vídeos, copies)
    - Segmentação de público-alvo
    - Disparo de campanhas (ex: e-mail, WhatsApp, anúncios)
    - Integração com ferramentas como Meta Ads, Google Ads, Tag Manager e GA4
    - Métricas e análises de desempenho (alcance, cliques, conversões)
    - A/B testing para campanhas
    - Automações (ex: sequência de posts ou fluxos de marketing)

    Objetivo:

    Fornecer ao lojista uma ferramenta completa para atrair, engajar e converter clientes,
    centralizando todas as estratégias de marketing em um único lugar.

'''

class TagManager(Plugin):

    container_id = models.CharField(
        max_length=20,
        verbose_name="Container ID",
        help_text="Ex: GTM-ABC1234",
        validators=[
            RegexValidator(
                regex=r"^GTM-[A-Z0-9]+$",
                message="Informe um Container ID válido. Ex: GTM-ABC1234",
            )
        ],
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = "Google Tag Manager"
        verbose_name_plural = "Google Tag Managers"

    def __str__(self):

        return f"{self.catalog} - {self.container_id}"


class MetaPixel(Plugin):

    pixel_id = models.CharField(
        max_length=20,
        verbose_name="Pixel ID",
        help_text="Ex: 123456789012345",
        validators=[
            RegexValidator(
                regex=r"^\d{10,20}$",
                message="Informe um Pixel ID válido contendo apenas números.",
            )
        ],
        null=True,
        blank=True
    )

    class Meta:

        verbose_name = "Meta Pixel"
        verbose_name_plural = "Meta Pixels"

    def __str__(self):

        return f"{self.catalog} - {self.pixel_id}"


class GA4(Plugin):

    measurement_id = models.CharField(
        max_length=20,
        verbose_name="Measurement ID",
        help_text="Ex: G-ABC123XYZ9",
        validators=[
            RegexValidator(
                regex=r"^G-[A-Z0-9]{8,12}$",
                message="Informe um Measurement ID válido. Ex: G-ABC123XYZ9",
            )
        ],
        null=True,
        blank=True
    )

    property_id = models.CharField(
        max_length=20,
        verbose_name="Property ID",
        blank=True,
        null=True,
        help_text="Ex: 123456789",
        validators=[
            RegexValidator(
                regex=r"^\d+$",
                message="Property ID deve conter apenas números.",
            )
        ],
    )

    class Meta:

        verbose_name = "Google Analytics 4"
        verbose_name_plural = "Google Analytics 4"

    def __str__(self):

        return f"{self.catalog} - {self.measurement_id}"