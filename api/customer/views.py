from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS,

)

from .models import Customer
from .serializers import CustomerSerializer

from api.catalog.models import Catalog

from rest_framework.filters import SearchFilter, OrderingFilter

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:

            return True

        if not request.user or not request.user.is_authenticated:
            
            return False

        catalog_id = view.kwargs.get("catalog_pk")

        return Catalog.objects.filter(
            id=catalog_id,
            user=request.user
        ).exists()

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            
            return True

        return obj.catalog.user == request.user

class CustomerViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = [SearchFilter, OrderingFilter]

    search_fields = [
        "full_name",
        "email",
        "whatsapp",
        "cpf_cnpj",
    ]

    ordering_fields = [
        "full_name",
        "email",
        "whatsapp",
        "cpf_cnpj",
        "created_at",
        "is_active",
        "is_integration",
    ]

    ordering = ["full_name"]

    def get_queryset(self):

        return Customer.objects.filter(

            catalog__id=self.kwargs["catalog_pk"]

        )