from django.db import models
from django.contrib.auth import get_user_model

from api.catalog.models import Catalog

User = get_user_model()

class Notification(models.Model):

    class NotificationType(models.TextChoices):

        ORDER = "order", "Pedido"
        PAYMENT = "payment", "Pagamento"
        SYSTEM = "system", "Sistema"
        MARKETING = "marketing", "Marketing"
        ALERT = "alert", "Alerta"

    catalog = models.ForeignKey(
        Catalog,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Catálogo",
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Usuário",
        null=True,
        blank=True
    )

    type_notification = models.CharField(
        max_length=50,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM,
        verbose_name="Tipo de notificação",
    )

    title = models.CharField(
        max_length=150,
        verbose_name="Título"
    )

    message = models.TextField(
        verbose_name="Mensagem",
        blank=True,
        null=True
    )

    action_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="URL de ação"
    )

    payload = models.JSONField(
        blank=True,
        null=True,
        verbose_name="Dados adicionais"
    )

    is_read = models.BooleanField(
        default=False,
        verbose_name="Lida"
    )

    read_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Lida em"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Atualizado em"
    )

    class Meta:
        verbose_name = "Notificação"
        verbose_name_plural = "Notificações"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "is_read"]),
            models.Index(fields=["catalog"]),
            models.Index(fields=["type_notification"]),
        ]

    def __str__(self):

        return f"{self.title} - {self.user or 'Sistema'}"