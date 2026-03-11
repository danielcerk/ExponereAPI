from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

from .models import Category
from .serializers import CategorySerializer

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user

class CategoryViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):

        return Category.objects.filter(

            catalog__id=self.kwargs["catalog_pk"]

        )