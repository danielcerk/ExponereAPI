from django.dispatch import receiver
from django.db.models.signals import post_save

from api.order.models import Order
from .models import CouponUsage


@receiver(post_save, sender=Order)
def create_coupon_usage_per_user(sender, instance, created, **kwargs):

    if not instance.coupon:
        
        return

    if not instance.is_paid:

        return

    if CouponUsage.objects.filter(order=instance).exists():

        return

    CouponUsage.objects.create(
        coupon=instance.coupon,
        order=instance,
        customer=instance.customer
    )