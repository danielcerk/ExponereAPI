from django.urls import path
from .views import (
    NewsletterEmailCreateView,
    NewsletterEmailListView
)

urlpatterns = [
    path("", NewsletterEmailCreateView.as_view(), name="newsletter-create"),
    path("list/", NewsletterEmailListView.as_view(), name="newsletter-list"),
]