
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import (

    BasePermission

)

from .models import Order
from .serializers import OrderSerializer

class IsOwner(BasePermission):

    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.catalog.user == request.user

class OrderViewSet(ModelViewSet):

    permission_classes = [IsOwner]
    serializer_class = OrderSerializer

    def get_queryset(self):

        catalog_id = self.kwargs.get("catalog_id")

        session_key = self.request.session.session_key

        if session_key:

            orders =  Order.objects.filter(
                session_key=session_key,
                product__catalog__id=catalog_id
            )

        else:

            orders = Order.objects.all(

                product__catalog__id=catalog_id

            )

        return orders