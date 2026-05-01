from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import (

    BasePermission,

)

from .serializers import AnalyticSerializer

from .utils import get_catalog

class IsOwner(BasePermission):

    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        return obj.user == request.user

class AnalyticView(APIView):
    
    permission_classes = [IsOwner]

    def get(self, request):

        catalog = get_catalog(self.request.user.pk)

        self.check_object_permissions(request, catalog)

        serializer = AnalyticSerializer(
            catalog,
            context={
                'days': request.query_params.get('days'),
                'start_date': request.query_params.get('start_date'),
                'end_date': request.query_params.get('end_date'),
            }
        )

        return Response(serializer.data)