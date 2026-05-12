from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Order

from .tasks import send_confirmation_order_customer

@receiver(post_save, sender=Order)
def create_order_confirmation(sender, instance, created, **kwargs):

    if instance.is_paid:

        send_confirmation_order_customer.delay(instance.id)