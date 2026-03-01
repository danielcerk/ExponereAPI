from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

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
    
class WishlistViewSet(ModelViewSet):

    permission_classes = [IsOwner,]

    queryset = Wishlist.objects.all()
    serializer_class = WishlistSerializer