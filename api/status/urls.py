from django.urls import path
from .views import StatusAnalyticView

urlpatterns = [
    path("", StatusAnalyticView.as_view(), name="analytics-status"),
]