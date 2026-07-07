from django.dispatch import receiver
from django.db.models.signals import post_save

from api.auth.models import UserProfile

from .models import NewsletterEmail


@receiver(post_save, sender=UserProfile)
def register_email_user_newsletter(sender, instance, created, **kwargs):
    
    if created and not NewsletterEmail.objects.filter(email=instance.email).exists():
        
        NewsletterEmail.objects.create(

            email=instance.email

        )