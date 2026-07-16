from django.db import models

from django.contrib.auth import get_user_model

User = get_user_model()

class Feedback(models.Model):

    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        null=True
    )

    email = models.EmailField(max_length=255)

    message = models.TextField(

        verbose_name='Feedback',
        null=False, blank=False

    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Email de Feedback'
        verbose_name_plural = 'Emails da Feedback'

    def __str__(self):

        return self.email