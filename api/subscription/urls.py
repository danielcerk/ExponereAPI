from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CancelAPIView,
    SuccessAPIView,
    CreateCheckoutSessionAPIView,
    UpgradeDowngradeSessionAPIView,
    StripeWebhookAPIView,
    PlanModelViewSet,
    MySubscriptionAPIView
)

router = DefaultRouter()
router.register(r'plans', PlanModelViewSet, basename='plan')

urlpatterns = [
    path('my-subscription/', MySubscriptionAPIView.as_view(), name='my-subscription'),
    path('create-checkout/', CreateCheckoutSessionAPIView.as_view(), name='create-checkout'),
    path('upgrade-downgrade/', UpgradeDowngradeSessionAPIView.as_view(), name='upgrade-downgrade'),
    path('success/', SuccessAPIView.as_view(), name='success'),
    path('cancel/', CancelAPIView.as_view(), name='cancel'),
    path('webhook/', StripeWebhookAPIView.as_view(), name='webhook'),
    path('', include(router.urls)),
]
