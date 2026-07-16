from django.urls import path

from .views import (
    MarketingLaunchCreateView,
    MarketingLaunchListView,
)

urlpatterns = [
    path(
        "<slug:slug>/",
        MarketingLaunchCreateView.as_view(),
        name="marketing-launch-create",
    ),
    path(
        "list/",
        MarketingLaunchListView.as_view(),
        name="marketing-launch-list",
    ),
]