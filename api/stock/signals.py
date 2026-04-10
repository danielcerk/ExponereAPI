from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Stock, AlertProductStock
from .tasks import send_reminder_product_stock_available

@receiver(pre_save, sender=Stock)
def store_old_quantity(sender, instance, **kwargs):

    if instance.pk:

        try:

            old = Stock.objects.get(pk=instance.pk)
            instance._old_quantity = old.quantity

        except Stock.DoesNotExist:

            instance._old_quantity = 0

    else:

        instance._old_quantity = 0


@receiver(post_save, sender=Stock)
def notify_stock_available(sender, instance, **kwargs):

    old_quantity = getattr(instance, "_old_quantity", 0)

    if old_quantity == 0 and instance.quantity > 0:

        alerts = AlertProductStock.objects.filter(
            product=instance.product,
            is_active=True
        )

        for alert in alerts:

            send_reminder_product_stock_available.delay(
                email=alert.email,
                store=instance.product.catalog.name,
                product=instance.product
            )

        alerts.update(is_active=False)