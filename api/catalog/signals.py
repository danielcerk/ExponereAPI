from django.dispatch import receiver
from django.db.models.signals import post_save

from api.auth.models import UserProfile
from api.catalog.models import Catalog

@receiver(post_save, sender=UserProfile)
def create_catalog_user(sender, instance, created, **kwargs):

    if not created:

        return

    if instance.owner is None and not instance.is_affiliate and not instance.catalog:

        catalog = Catalog.objects.create(user=instance)

        instance.catalog = catalog
        instance.owner = instance

        # evita loop desnecessário
        UserProfile.objects.filter(pk=instance.pk).update(
            catalog=catalog,
            owner=instance
        )