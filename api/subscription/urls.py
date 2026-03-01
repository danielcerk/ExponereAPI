from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CancelAPIView,
    SuccessAPIView,
    CreateCheckoutSessionAPIView,
    UpgradeDowngradeSessionAPIView,
    StripeWebhookAPIView,
    PlanModelViewSet,
    RemoveAccess4CanceledPlan
)

router = DefaultRouter()
router.register(r'plans', PlanModelViewSet, basename='plan')

urlpatterns = [
    path('create-checkout/', CreateCheckoutSessionAPIView.as_view(), name='create-checkout'),
    path('upgrade-downgrade/', UpgradeDowngradeSessionAPIView.as_view(), name='upgrade-downgrade'),
    path('success/', SuccessAPIView.as_view(), name='success'),
    path('cancel/', CancelAPIView.as_view(), name='cancel'),
    path('webhook/', StripeWebhookAPIView.as_view(), name='webhook'),
    path('set-status-canceled-plan/', RemoveAccess4CanceledPlan.as_view(), name='remove'),
    path('', include(router.urls)),
]
