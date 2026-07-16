from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)
from rest_framework.parsers import ( 
    MultiPartParser, FormParser,
    JSONParser
)

from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Catalog, Link
from .serializers import CatalogSerializer, LinkSerializer

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

    serializer_class = CatalogSerializer

    def get_queryset(self):

        return Catalog.objects.all()
    
    def perform_create(self, serializer):

        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def my(self, request):

        catalog = get_object_or_404(Catalog, user=self.request.user)

        if request.method == 'GET':

            return Response(self.get_serializer(catalog).data)

        if request.method in ['PUT', 'PATCH']:

            serializer = self.get_serializer(
                catalog,
                data=request.data,
                partial=(request.method == 'PATCH')
            )

            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data)

        if request.method == 'DELETE':

            catalog.delete()

            return Response(status=204)
    
class LinkViewSet(ModelViewSet):
    
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    permission_classes = [IsOwnerOrReadOnly]

    serializer_class = LinkSerializer

    def get_queryset(self):

        catalog_id = self.kwargs.get('catalog_pk')
            
        return Link.objects.filter(catalog__pk=catalog_id)
        