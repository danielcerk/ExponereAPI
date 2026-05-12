from django.shortcuts import get_object_or_404

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import BasePermission

from .models import Order
from .serializers import OrderSerializer
from api.nf.models import NF
from api.cloudinary_utils import delete_from_cloudinary_nf

class IsOrderOwner(BasePermission):

    def has_permission(self, request, view):

        if not request.session.session_key:

            request.session.save()

        return True

    def has_object_permission(self, request, view, obj):

        if request.user.is_authenticated:

            return obj.catalog.user == request.user

        return obj.customer.session_key == request.session.session_key


class OrderViewSet(ModelViewSet):

    permission_classes = [IsOrderOwner]
    serializer_class = OrderSerializer

    def get_queryset(self):

        catalog_id = self.kwargs.get("catalog_pk")

        queryset = Order.objects.filter(

            catalog__id=catalog_id

        )

        if self.request.user.is_authenticated:

            if queryset.filter(

                catalog__user=self.request.user

            ).exists():
                
                return queryset

        return queryset.filter(

            customer__session_key=self.request.session.session_key

        )
    
    def perform_destroy(self, instance):

        nf = get_object_or_404(NF, order=instance)

        delete_from_cloudinary_nf(nf.file_url)

        instance.delete()

