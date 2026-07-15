from rest_framework import generics, permissions
from .models import MarketingLaunch
from .serializers import MarketingLaunchSerializer


class MarketingLaunchCreateView(generics.CreateAPIView):

    queryset = MarketingLaunch.objects.all()
    serializer_class = MarketingLaunchSerializer
    permission_classes = [permissions.AllowAny]


class MarketingLaunchListView(generics.ListAPIView):

    queryset = MarketingLaunch.objects.all()
    serializer_class = MarketingLaunchSerializer
    permission_classes = [permissions.IsAdminUser]