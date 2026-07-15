from rest_framework import generics, permissions
from .models import Launch
from .serializers import LaunchSerializer


class LaunchCreateView(generics.CreateAPIView):

    queryset = Launch.objects.all()
    serializer_class = LaunchSerializer
    permission_classes = [permissions.AllowAny]


class LaunchListView(generics.ListAPIView):

    queryset = Launch.objects.all()
    serializer_class = LaunchSerializer
    permission_classes = [permissions.IsAdminUser]