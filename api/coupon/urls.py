from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(r'coupon-progressive', CouponProgressiveViewSet, basename='coupon-progressive')
router.register(r'coupon-fixed', CouponFixedValueViewSet, basename='coupon-fixed')
router.register(r'coupon-percent', CouponPercentValueViewSet, basename='coupon-percent')
router.register(r'coupon-first-buy', CouponFirstBuyViewSet, basename='coupon-first-buy')
router.register(r'coupon-usage', CouponUsageViewSet, basename='coupon-usage')

urlpatterns = [

    path('<int:catalog_pk>/', include(router.urls)),
    path("coupon/is-valid/", CouponIsValidView.as_view(), name="coupon-is-valid"),

]