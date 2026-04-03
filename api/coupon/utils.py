from .models import (
    CouponProgressive,
    CouponFixedValue,
    CouponPercentValue,
    CouponFirstBuy
)

def get_coupon_by_code(catalog, code):

    models = [
        CouponProgressive,
        CouponFixedValue,
        CouponPercentValue,
        CouponFirstBuy
    ]

    for model in models:
        coupon = model.objects.filter(
            catalog=catalog,
            code__iexact=code
        ).first()

        if coupon:
            return coupon

    return None