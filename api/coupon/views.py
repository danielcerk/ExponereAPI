from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS,
    IsAuthenticated

)

from .models import *
from .serializers import *

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.catalog.user == request.user
    
class BaseCouponViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    def get_catalog(self):

        queryset = Catalog.objects.filter(

            pk=self.kwargs["catalog_pk"]

        )

        if self.request.method not in SAFE_METHODS:
            
            queryset = queryset.filter(user=self.request.user)

        return get_object_or_404(queryset)

    def get_queryset(self):

        return self.queryset.filter(

            catalog=self.get_catalog()

        )

    def perform_create(self, serializer):

        serializer.save(

            catalog=self.get_catalog()

        )


class CouponProgressiveViewSet(BaseCouponViewSet):

    queryset = CouponProgressive.objects.all()
    serializer_class = CouponProgressiveSerializer

class CouponFixedValueViewSet(BaseCouponViewSet):

    queryset = CouponFixedValue.objects.all()
    serializer_class = CouponFixedValueSerializer

class CouponPercentValueViewSet(BaseCouponViewSet):

    queryset = CouponPercentValue.objects.all()
    serializer_class = CouponPercentValueSerializer

class CouponFirstBuyViewSet(BaseCouponViewSet):

    queryset = CouponFirstBuy.objects.all()
    serializer_class = CouponFirstBuySerializer

class CouponUsageViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    queryset = CouponUsage.objects.all()
    serializer_class = CouponUsageSerializer

    def get_queryset(self):

        return self.queryset.filter(

            coupon__catalog__pk=self.kwargs["catalog_pk"],
            coupon__catalog__user=self.request.user

        )