from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet

from api.catalog.models import Catalog

from api.cloudinary_utils import delete_from_cloudinary_img

from .serializers import ProductSerializer
from .models import Product

from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS,

)

class IsCatalogOwnerOrRead(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

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

        catalog_id = self.kwargs.get("catalog_pk")

        if not catalog_id:

            return Product.objects.none()

        return Product.objects.filter(
            catalog_id=catalog_id,
            catalog__user=self.request.user
        )
    
    def perform_destroy(self, instance):

        images = instance.images.all()

        for image in images:

            if image.image:

                delete_from_cloudinary_img(image.image)

        instance.delete()