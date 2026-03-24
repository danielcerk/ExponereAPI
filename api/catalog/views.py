from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

from .models import Catalog
from .serializers import CatalogSerializer

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
    
class CatalogViewSet(ModelViewSet):

    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsOwnerOrReadOnly]

    serializer_class = CatalogSerializer

    def get_queryset(self):

        user = self.request.user

        if user.is_authenticated:
            
            return Catalog.objects.filter(user=user)

        return Catalog.objects.none()
        