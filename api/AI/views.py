from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from django.shortcuts import get_object_or_404

from api.catalog.models import Catalog
from api.product.models import Product
from .models import CopyProduct

from .serializers import GenerateCopySerializer, CopyProductSerializer

class IsCatalogOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.catalog.user == request.user

    def has_permission(self, request, view):

        catalog_id = view.kwargs.get("catalog_pk")

        if not catalog_id:

            return False

        catalog = get_object_or_404(Catalog, pk=catalog_id)

        return catalog.user == request.user

class GenerateCopyView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, catalog_pk=None, product_pk=None):

        catalog = get_object_or_404(Catalog, pk=catalog_pk, user=request.user)
        product = get_object_or_404(Product, pk=product_pk, catalog=catalog)

        copy = f'{product.title} , {product.description} '

        serializer = GenerateCopySerializer(
            data={},
            context={"copy": copy}
        )

        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class CopyProductViewSet(viewsets.ModelViewSet):

    serializer_class = CopyProductSerializer
    permission_classes = [permissions.IsAuthenticated, IsCatalogOwner]

    def get_queryset(self):

        catalog_id = self.kwargs.get("catalog_pk")
        product_id = self.kwargs.get("product_pk")

        return CopyProduct.objects.filter(
            catalog_id=catalog_id,
            product_id=product_id,
            catalog__user=self.request.user
        )

    def perform_create(self, serializer):

        catalog_id = self.kwargs.get("catalog_pk")
        product_id = self.kwargs.get("product_pk")

        catalog = get_object_or_404(
            Catalog,
            pk=catalog_id,
            user=self.request.user
        )

        product = get_object_or_404(
            Product,
            pk=product_id,
            catalog=catalog
        )

        serializer.save(
            catalog=catalog,
            product=product
        )