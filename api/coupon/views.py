from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

from .models import *
from .serializers import *

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

        return request.catalog.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.catalog.user == request.user
    
class BaseCouponViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.queryset.filter(catalog__user=self.request.user)

    def perform_create(self, serializer):
        serializer.save()

class CouponProgressiveViewSet(BaseCouponViewSet):
    
    permission_classes = [IsOwnerOrReadOnly]

    queryset = CouponProgressive.objects.all()
    serializer_class = CouponProgressiveSerializer

class CouponFixedValueViewSet(BaseCouponViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = CouponFixedValue.objects.all()
    serializer_class = CouponFixedValueSerializer

class CouponPercentValueViewSet(BaseCouponViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    
    queryset = CouponPercentValue.objects.all()
    serializer_class = CouponPercentValueSerializer

class CouponFirstBuyViewSet(BaseCouponViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = CouponFirstBuy.objects.all()
    serializer_class = CouponFirstBuySerializer

class CouponUsageViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = CouponUsage.objects.all()
    serializer_class = CouponUsageSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):

        return self.queryset.filter(

            coupon__catalog__user=self.request.user

        )