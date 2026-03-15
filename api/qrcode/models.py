from django.db import models

from api.catalog.models import Catalog

class QRCode(models.Model):

    catalog = models.OneToOneField(
        Catalog,
        on_delete=models.CASCADE,
        related_name="qr_code"
    )

    img = models.URLField(
        verbose_name='QR code',
        null=True, blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)

    def __str__(self):

        return f'QR Code {self.catalog.name}'