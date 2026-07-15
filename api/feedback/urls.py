from django.urls import path
from .views import (
    FeedbackCreateView,
    FeedbackListView
)

urlpatterns = [
    path("", FeedbackCreateView.as_view(), name="newsletter-create"),
    path("list/", FeedbackListView.as_view(), name="newsletter-list"),
]