from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

from .models import QRCode
from .serializers import QRCodeSerializer

from api.catalog.models import Catalog

class IsOwnerOrReadOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        catalog_id = view.kwargs.get("catalog_id")

        return Catalog.objects.filter(
            id=catalog_id,
            user=request.user
        ).exists()

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
    
class QRCodeViewSet(ModelViewSet):

    permission_classes = [IsOwnerOrReadOnly]

    queryset = QRCode.objects.all()
    serializer_class = QRCodeSerializer

    def get_queryset(self):

        return QRCode.objects.filter(

            catalog__id=self.kwargs["catalog_pk"]

        )
