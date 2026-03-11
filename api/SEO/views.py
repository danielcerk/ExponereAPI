from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

from api.catalog.models import Catalog

from .models import Keyword
from .serializers import KeywordSerializer

from rest_framework.parsers import MultiPartParser, FormParser

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
    
class KeyWordSEOViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = KeywordSerializer

    def get_queryset(self):

        catalog_id = self.kwargs.get("catalog_id")
        user = self.request.user

        if user.is_authenticated:

            return Keyword.objects.filter(
                catalog__user=user,
                catalog__id=catalog_id
            )

        return Keyword.objects.none()