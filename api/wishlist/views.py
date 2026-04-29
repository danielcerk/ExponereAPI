from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin
)
from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Wishlist
from .serializers import WishlistSerializer


class IsOwner(BasePermission):

    def has_permission(self, request, view):

        if not request.session.session_key:

            request.session.save()

        return True

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        session_key = request.session.session_key

        return obj.session_key == session_key

class WishlistViewSet(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    permission_classes = [IsOwner]
    serializer_class = WishlistSerializer
    http_method_names = ["get", "post", "delete"]

    def get_queryset(self):

        catalog_id = self.kwargs.get("catalog_pk")

        session_key = self.request.session.session_key

        if not session_key:
            
            self.request.session.create()
            session_key = self.request.session.session_key

        return Wishlist.objects.filter(
            session_key=session_key,
            product__catalog__id=catalog_id
        )