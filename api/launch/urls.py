from django.urls import path
from .views import (
    LaunchCreateView,
    LaunchListView
)

urlpatterns = [
    path("", LaunchCreateView.as_view(), name="launch-create"),
    path("list/", LaunchListView.as_view(), name="launch-list"),
]