from django.urls import path, include

from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    MyTokenObtainPairView,
    RegisterView,
    LogoutAPIView,
    AccountViewSet,
    setup_2fa,
    confirm_2fa
)

router = DefaultRouter()

router.register('account', AccountViewSet, basename='account')

urlpatterns = [
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('', include(router.urls)),
    path('logout/', LogoutAPIView.as_view(), name ='logout'),

    path("2fa/setup/", setup_2fa),
    path("2fa/confirm/", confirm_2fa, name="confirm-2fa"),

]