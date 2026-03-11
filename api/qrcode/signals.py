# signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver

from api.catalog.models import Catalog
from .models import QRCode


def generate_qrcode_url(store_name: str) -> str:

    store_slug = store_name.replace(" ", "_").lower()
    store_url = f"https://exponere.com.br/store/{store_slug}"

    qr_api = "https://api.qrserver.com/v1/create-qr-code/"

    return f"{qr_api}?size=300x300&data={store_url}"


@receiver(post_save, sender=Catalog)
def create_catalog_qrcode(sender, instance, created, **kwargs):

    if not created:
        
        return

    qr_url = generate_qrcode_url(instance.name)

    QRCode.objects.create(
        catalog=instance,
        img=qr_url
    )