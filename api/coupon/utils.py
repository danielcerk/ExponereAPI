from django.db.models import Q, F
from django.utils import timezone

from .models import (
    CouponProgressive,
    CouponFixedValue,
    CouponPercentValue,
    CouponFirstBuy
)


def get_coupon_by_code(catalog, code):

    now = timezone.now()

    coupon_models = [
        CouponProgressive,
        CouponFixedValue,
        CouponPercentValue,
        CouponFirstBuy
    ]

    for model in coupon_models:

        coupon = model.objects.filter(
            catalog=catalog,
            code__iexact=code,
            is_active=True
        ).filter(
            Q(start_date__isnull=True) | Q(start_date__lte=now),
            Q(end_date__isnull=True) | Q(end_date__gte=now),
            Q(usage_limit__isnull=True) | Q(usage_count__lt=F("usage_limit"))
        ).first()

        if coupon:

            return coupon

    return None