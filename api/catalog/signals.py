from django.dispatch import receiver
from django.db.models.signals import post_save

from api.auth.models import UserProfile

from .models import Catalog

@receiver(post_save, sender=UserProfile)
def create_catalog_user(sender, instance, created, **kwargs):
    
    if created:

        Catalog.objects.create(
            user=instance,
        )