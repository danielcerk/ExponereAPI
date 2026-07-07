from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS,

)

from .models import Category, BusinessCategory, SubCategory
from .serializers import CategorySerializer, BusinessCategorySerializer, SubCategorySerializer

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
        
        if hasattr(obj, "category"):

            return obj.category.catalog.user == request.user

        return False
    
class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

        return request.user and request.user.is_authenticated and request.user.is_staff

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True
        return request.user and request.user.is_authenticated and request.user.is_staff

class CategoryViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):

        return Category.objects.filter(

            catalog__id=self.kwargs["catalog_pk"]

        )
    
class SubCategoryViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer

    def get_queryset(self):

        return SubCategory.objects.filter(

            category__id=self.kwargs["category_pk"]

        )
    
class BusinessCategoryViewSet(ModelViewSet):

    permission_classes = [IsAdminOrReadOnly]

    queryset = BusinessCategory.objects.all()
    serializer_class = BusinessCategorySerializer