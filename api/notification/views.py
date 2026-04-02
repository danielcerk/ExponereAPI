from django.shortcuts import get_object_or_404

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from api.catalog.models import Catalog

from .serializers import NotificationSerializer
from .models import Notification

from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

class IsCatalogOwner(BasePermission):

    def has_object_permission(self, request, view, obj):

        return obj.catalog.user == request.user

    def has_permission(self, request, view):

        catalog_id = view.kwargs.get("catalog_pk")

        if not catalog_id:

            return False

        catalog = get_object_or_404(Catalog, pk=catalog_id)

        return catalog.user == request.user
    
class NotificationViewSet(
    mixins.RetrieveModelMixin,
    GenericViewSet
    ):

    serializer_class = NotificationSerializer
    permission_classes = [IsCatalogOwner]

    def get_queryset(self):

        catalog_id = self.kwargs.get("catalog_pk")

        if not catalog_id:

            return Notification.objects.none()

        return Notification.objects.filter(
            catalog_id=catalog_id,
            catalog__user=self.request.user
        )