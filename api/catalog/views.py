from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

from .models import Catalog, Link
from .serializers import CatalogSerializer, LinkSerializer

from rest_framework.parsers import ( 
    MultiPartParser, FormParser,
    JSONParser
)

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True
        
        if hasattr(obj, "user"):

            return obj.user == request.user

        if hasattr(obj, "catalog"):

            return obj.catalog.user == request.user

        return False
    
class CatalogViewSet(ModelViewSet):

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer
    
class LinkViewSet(ModelViewSet):
    
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsOwnerOrReadOnly]

    serializer_class = LinkSerializer

    def get_queryset(self):

        catalog_id = self.kwargs.get('catalog_pk')
            
        return Link.objects.filter(catalog__pk=catalog_id)
        