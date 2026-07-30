from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from api.catalog.models import Catalog

from api.cloudinary_utils import delete_from_cloudinary_img

from .serializers import ProductSerializer
from .models import Product

from django.db.models import Q

from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS,

)

class IsCatalogOwnerOrRead(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

        if not request.user or not request.user.is_authenticated:

            return False

        catalog_id = view.kwargs.get("catalog_pk")

        if not catalog_id:

            return False

        catalog = get_object_or_404(Catalog, pk=catalog_id)

        return catalog.user == request.user

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.catalog.user == request.user
    
class ProductViewSet(ModelViewSet):
    
    permission_classes = [IsCatalogOwnerOrRead]
    serializer_class = ProductSerializer

    def get_queryset(self):

        product_id = self.kwargs.get("pk")
        catalog_id = self.kwargs.get("catalog_pk")

        if not catalog_id:
            return Product.objects.none()

        queryset = Product.objects.filter(
            catalog_id=catalog_id
        )

        if self.request.user.is_authenticated:
            queryset = queryset.filter(
                catalog__user=self.request.user
            )

        if product_id:
            queryset = queryset.filter(pk=product_id)

        search = self.request.query_params.get("search")
        category = self.request.query_params.get("category")
        subcategory = self.request.query_params.get("subcategory")
        ordering = self.request.query_params.get("ordering")

        if search:
            queryset = queryset.filter(
                title__icontains=search
            )

        if category:
            queryset = queryset.filter(
                category__id=category
            )

        if subcategory:
            queryset = queryset.filter(
                subcategory__id=subcategory
            )

        queryset = queryset.distinct()

        allowed_ordering = {
            "title",
            "-title",
            "price",
            "-price",
            "promotion_is_active",
            "-promotion_is_active",
            "is_active",
            "-is_active",
            "created_at",
            "-created_at",
            "updated_at",
            "-updated_at",
            "stocks__quantity",
            "-stocks__quantity",
        }

        if ordering in allowed_ordering:
            queryset = queryset.order_by(ordering)

        return queryset
    
    def perform_destroy(self, instance):

        images = instance.images.all()

        for image in images:

            if image.image:

                delete_from_cloudinary_img(image.image)

        instance.delete()