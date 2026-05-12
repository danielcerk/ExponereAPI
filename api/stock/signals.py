from django.db import transaction
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from .models import Stock, AlertProductStock, StockMovement
from .tasks import send_reminder_product_stock_available

from api.order.models import Order, ProductOrder

@receiver(pre_save, sender=Order)
def track_payment_status(sender, instance, **kwargs):

    if not instance.pk:

        instance._previous_is_paid = False
        
        return

    previous = Order.objects.get(pk=instance.pk)
    instance._previous_is_paid = previous.is_paid


@receiver(post_save, sender=Order)
def update_stock_quantity(sender, instance, created, **kwargs):

    just_paid = (
        instance.is_paid is True and
        getattr(instance, "_previous_is_paid", False) is False
    )

    if not just_paid:

        return

    with transaction.atomic():

        for item in instance.items.select_related(
            "wishlist_product__product"
        ):
            
            product = item.wishlist_product.product
            quantity = item.wishlist_product.quantity

            stock = product.stocks

            StockMovement.objects.create(
                stock=stock,
                type=StockMovement.OUT,
                quantity=quantity,
                purchase_price=instance.total,
                reference=f"Pedido #{instance.id}"
            )

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