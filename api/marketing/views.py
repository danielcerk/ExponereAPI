from django.shortcuts import get_object_or_404

from api.catalog.models import Catalog
from api.marketing.serializers import (
    TagManagerSerializer,
    MetaPixelSerializer,
    GA4Serializer
)
from api.marketing.models import (
    MetaPixel,
    GA4,
    TagManager
)

from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

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

class BasePluginViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):

    permission_classes = [IsCatalogOwnerOrRead]

    def get_catalog(self):

        return get_object_or_404(
            Catalog,
            pk=self.kwargs["catalog_pk"]
        )

    def get_object(self):

        return get_object_or_404(
            self.queryset,
            catalog=self.get_catalog()
        )

class MetaPixelViewSet(BasePluginViewSet):

    serializer_class = MetaPixelSerializer
    queryset = MetaPixel.objects.all()

class TagManagerViewSet(BasePluginViewSet):

    serializer_class = TagManagerSerializer
    queryset = TagManager.objects.all()

class GA4ViewSet(BasePluginViewSet):

    serializer_class = GA4Serializer
    queryset = GA4.objects.all()