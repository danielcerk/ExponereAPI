from django.shortcuts import get_object_or_404

from rest_framework.views import APIView

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS,
    IsAuthenticated,
    AllowAny

)
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import *

from .utils import get_coupon_by_code

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
    
class CouponIsValidView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request):
        catalog_id = request.query_params.get("catalog")
        coupon_code = request.query_params.get("coupon_code")

        if not catalog_id or not coupon_code:
            return Response(
                {
                    "valid": False,
                    "message": "catalog e coupon_code são obrigatórios."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            catalog = Catalog.objects.get(id=catalog_id)
        except Catalog.DoesNotExist:
            return Response(
                {
                    "valid": False,
                    "message": "Catálogo não encontrado."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        coupon = get_coupon_by_code(catalog, coupon_code)

        if not coupon:
            return Response(
                {
                    "valid": False,
                    "message": "Cupom não encontrado."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if not coupon.is_valid():
            return Response(
                {
                    "valid": False,
                    "message": "Cupom inválido ou expirado."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "valid": True,
                "message": "Cupom válido.",
                "coupon": {
                    "id": coupon.id,
                    "code": coupon.code,
                    "discount_type": coupon.discount_type,
                    "discount_value": coupon.discount_value,
                }
            },
            status=status.HTTP_200_OK
        )