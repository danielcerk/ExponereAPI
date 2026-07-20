from django.dispatch import receiver
from django.db.models.signals import post_save

from api.catalog.models import Catalog

from .models import AnalyticRoute

@receiver(post_save, sender=Catalog)
def create_analytic_catalog_user(sender, instance, created, **kwargs):

    if not created:

        AnalyticRoute.objects.update_or_create(
            catalog=instance,
            defaults={
                "slug": instance.slug,
            },
        )