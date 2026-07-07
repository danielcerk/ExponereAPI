from django.dispatch import receiver
from django.db.models.signals import post_save

from api.catalog.models import Catalog
from api.marketing.models import (
    MetaPixel,
    GA4,
    TagManager
)
from api.models import AuthorPlugin


@receiver(post_save, sender=Catalog)
def create_plugin_instance(sender, instance, created, **kwargs):

    if not created:

        return

    meta_author, _ = AuthorPlugin.objects.get_or_create(
        name="Meta"
    )

    google_author, _ = AuthorPlugin.objects.get_or_create(
        name="Google"
    )

    MetaPixel.objects.get_or_create(
        catalog=instance,
        defaults={
            "name": "Meta Pixel",
            "author": meta_author,
            "pixel_id": "",
        }
    )

    GA4.objects.get_or_create(
        catalog=instance,
        defaults={
            "name": "Google Analytics",
            "author": google_author,
            "measurement_id": "",
            "property_id": "",
        }
    )

    TagManager.objects.get_or_create(
        catalog=instance,
        defaults={
            "name": "Google Tag Manager",
            "author": google_author,
            "container_id": "",
        }
    )