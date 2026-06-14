from rest_framework import generics, permissions
from .models import NewsletterEmail
from .serializers import NewsletterEmailSerializer


class NewsletterEmailCreateView(generics.CreateAPIView):

    queryset = NewsletterEmail.objects.all()
    serializer_class = NewsletterEmailSerializer
    permission_classes = [permissions.AllowAny]


class NewsletterEmailListView(generics.ListAPIView):

    queryset = NewsletterEmail.objects.all()
    serializer_class = NewsletterEmailSerializer
    permission_classes = [permissions.IsAdminUser]