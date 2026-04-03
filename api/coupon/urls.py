from django.urls import path

from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'coupon-progressive', CouponProgressiveViewSet)
router.register(r'coupon-fixed', CouponFixedValueViewSet)
router.register(r'coupon-percent', CouponPercentValueViewSet)
router.register(r'coupon-first-buy', CouponFirstBuyViewSet)
router.register(r'coupon-usage', CouponUsageViewSet)

urlpatterns = [
] + router.urls