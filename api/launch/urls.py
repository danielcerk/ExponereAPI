from django.urls import path
from .views import (
    LaunchCreateView,
    LaunchListView
)

urlpatterns = [
    path("", LaunchCreateView.as_view(), name="newsletter-create"),
    path("list/", LaunchListView.as_view(), name="newsletter-list"),
]