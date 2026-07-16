from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions

from .models import MarketingLaunch, CampaignMarketingLaunch
from .serializers import MarketingLaunchSerializer

class MarketingLaunchCreateView(generics.CreateAPIView):

    queryset = MarketingLaunch.objects.all()
    serializer_class = MarketingLaunchSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        campaign = get_object_or_404(
            CampaignMarketingLaunch,
            slug=self.kwargs["slug"],
            is_active=True,
        )

        serializer.save(campaign_marketing=campaign)


class MarketingLaunchListView(generics.ListAPIView):

    queryset = MarketingLaunch.objects.all()
    serializer_class = MarketingLaunchSerializer
    permission_classes = [permissions.IsAdminUser]