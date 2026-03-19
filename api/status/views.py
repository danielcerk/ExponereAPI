from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .serializers import StatusAnalyticSerializer


class StatusAnalyticView(APIView):
    
    permission_classes = [AllowAny]

    def get(self, request):

        serializer = StatusAnalyticSerializer(instance={})

        return Response(serializer.data)