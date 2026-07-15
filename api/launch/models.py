from django.db import models

from django.core.validators import RegexValidator

class Launch(models.Model):

    name = models.CharField(max_length=255, unique=True)

    email = models.EmailField(max_length=255, unique=True)
    whatsapp = models.CharField(
        verbose_name='WhatsApp',
        max_length=20,
        null=False,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Email de Launch'
        verbose_name_plural = 'Emails da Launch'

    def __str__(self):

        return self.email