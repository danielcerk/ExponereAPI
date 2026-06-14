from django.shortcuts import get_object_or_404

from rest_framework import mixins, status
from rest_framework.viewsets import GenericViewSet

from api.catalog.models import Catalog

from .serializers import NotificationSerializer
from .models import Notification

from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone

from rest_framework.permissions import (

    BasePermission,
    SAFE_METHODS

)

class IsCatalogOwner(BasePermission):

    def has_permission(self, request, view):

        if not request.user or not request.user.is_authenticated:
            
            return False

        catalog = Catalog.objects.filter(user=request.user).first()

        if not catalog:

            return False

        return catalog.user == request.user

    def has_object_permission(self, request, view, obj):

        return obj.catalog.user == request.user
    
class NotificationViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    serializer_class = NotificationSerializer
    permission_classes = [IsCatalogOwner]

    def get_queryset(self):

        return Notification.objects.filter(
            catalog__user=self.request.user
        )

    @action(detail=True, methods=["patch"], url_path="mark-as-read")
    def mark_as_read(self, request, pk=None):
        
        notification = self.get_object()

        notification.is_read = True
        notification.read_at = timezone.now()
        notification.save(update_fields=["is_read", "read_at", "updated_at"])

        return Response(
            {
                "message": "Notificação marcada como lida.",
                "is_read": notification.is_read,
                "read_at": notification.read_at
            },
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=["patch"], url_path="mark-all-as-read")
    def mark_all_as_read(self, request):

        updated = self.get_queryset().filter(is_read=False).update(
            is_read=True,
            read_at=timezone.now()
        )

        return Response({
            "message": f"{updated} notificações marcadas como lidas."
        })