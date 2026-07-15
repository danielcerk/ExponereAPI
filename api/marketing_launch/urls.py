from django.urls import path
from .views import (
    MarketingLaunchCreateView,
    MarketingLaunchListView
)

urlpatterns = [
    path("", MarketingLaunchCreateView.as_view(), name="newsletter-create"),
    path("list/", MarketingLaunchListView.as_view(), name="newsletter-list"),
]