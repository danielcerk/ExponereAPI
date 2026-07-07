from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django_otp.admin import OTPAdminSite
from django.conf import settings

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

if not settings.DEBUG:

    admin.site.__class__ = OTPAdminSite

urlpatterns = [

    path('admin/', admin.site.urls),

    path('api/v1/', include('api.urls')),

    path('api/v1/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/v1/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path(
        "robots.txt",
        TemplateView.as_view(
            template_name="robots.txt",
            content_type="text/plain"
        ),
    ),

]
