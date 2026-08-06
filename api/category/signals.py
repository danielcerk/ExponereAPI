
from api.catalog.models import Catalog

from django.dispatch import receiver
from django.db.models.signals import post_save

from .tasks import generate_categories

@receiver(post_save, sender=Catalog)
def generate_categories_after_business_category_config(
    sender,
    instance,
    created,
    **kwargs,
):
    
    if instance.business_category:

        generate_categories.delay(instance.id)