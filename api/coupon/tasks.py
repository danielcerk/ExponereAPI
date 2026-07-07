from celery import shared_task

from .models import (

    Coupon

)

from django.utils import timezone

@shared_task()
def disable_expired_coupons():

    now = timezone.now()

    updated_count = Coupon.objects.filter(
        is_active=True,
        end_date__isnull=False,
        end_date__lt=now
    ).update(is_active=False)

    return f"{updated_count} cupons desativados."