from django.dispatch import receiver
from django.db.models.signals import post_save
from django.shortcuts import get_object_or_404

from api.order.models import Order
from .models import Coupon, CouponUsage

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

    get_coupon = get_object_or_404(Coupon, pk=instance.coupon.pk)

    get_coupon.usage_count += 1

    if get_coupon.usage_count == get_coupon.usage_limit:

        get_coupon.is_active = False

    get_coupon.save()

