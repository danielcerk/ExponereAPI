from django.db import models

class NewsletterEmail(models.Model):

    email = models.EmailField(max_length=255, unique=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = 'Email de Newsletter'
        verbose_name_plural = 'Emails da Newsletter'

    def __str__(self):

        return self.email