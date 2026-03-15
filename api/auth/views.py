from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (

    AllowAny,
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS

)
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    AccountSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer
)

from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser

from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.decorators import api_view, permission_classes

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.conf import settings

import requests

from django.contrib.auth.tokens import PasswordResetTokenGenerator 
from .models import PasswordReset 
import os 

from api.notification.utils import (
    send_password_reset_email,
    send_password_changed_email
)

User = get_user_model()

class IsOwnerOrReadOnly(BasePermission):
    
    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.pk == request.user.pk

class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)

        return Response(
            {
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'refresh': str(refresh),
                'access': access,
            },
            status=status.HTTP_201_CREATED,
        )

class AccountViewSet(ModelViewSet):

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = AccountSerializer
    permission_classes = [IsOwnerOrReadOnly, AllowAny]

    def get_queryset(self):

        return User.objects.all().order_by('-created_at')

class LogoutAPIView(APIView):

    permission_classes = (AllowAny,)

    def post(self, request):

        try:

            refresh_token = request.data['refresh_token']

            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:

            return Response(status=status.HTTP_400_BAD_REQUEST)
        
class GoogleLogin(SocialLoginView):

    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.GOOGLE_OAUTH_CALLBACK_URL
    client_class = OAuth2Client

class GoogleLoginCallback(APIView):

    def get(self, request, *args, **kwargs):

        code = request.GET.get("code")

        if code is None:

            return Response({"error": "Código de autenticação não encontrado"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "redirect_uri": settings.GOOGLE_OAUTH_CALLBACK_URL,
            "grant_type": "authorization_code",
        }

        response = requests.post(token_url, data=data)

        if response.status_code != 200:

            return Response({"error": "Erro ao obter o token", "content": response.text}, status=status.HTTP_400_BAD_REQUEST)

        token_data = response.json()
        access_token = token_data.get("access_token")

        user_info_url = "https://www.googleapis.com/oauth2/v2/userinfo"
        headers = {"Authorization": f"Bearer {access_token}"}
        user_info_response = requests.get(user_info_url, headers=headers)

        if user_info_response.status_code != 200:

            return Response({"error": "Erro ao obter informações do usuário"}, status=status.HTTP_400_BAD_REQUEST)

        user_data = user_info_response.json()

        email = user_data.get("email")
        name = user_data.get("name")

        # Criar ou autenticar o usuário no banco de dados
        user, created = User.objects.get_or_create(email=email, defaults={"name": name})

        # Gerar tokens JWT para autenticação
        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "name": user.name,
            }
        })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def setup_2fa(request):

    device = TOTPDevice.objects.create(
        user=request.user,
        confirmed=False
    )

    return Response({
        "config_url": f'https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={device.config_url}'
    })

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def confirm_2fa(request):
    code = request.data.get("code")

    device = TOTPDevice.objects.filter(user=request.user, confirmed=False).first()

    if not device:

        return Response({"error": "Dispositivo não encontrado"}, status=404)

    if device.verify_token(code):
        device.confirmed = True
        device.save()
        return Response({"status": "2FA ativado"})

    return Response({"error": "Código inválido"}, status=400)

class RequestPasswordReset(generics.GenericAPIView):

    permission_classes = [AllowAny]
    serializer_class = ResetPasswordRequestSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email__iexact=email).first()

        if user:

            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)

            reset = PasswordReset(email=email, token=token)
            reset.save()

            if settings.DEBUG:

                reset_url = f"https://exponere.com.br/{token}"

            else:

                reset_url = f"http://127.0.0.1:8000/{token}"

            send_password_reset_email(user, reset_url)

            return Response(
                {"success": "We have sent you a link to reset your password"},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": "User with credentials not found"},
            status=status.HTTP_404_NOT_FOUND
        )


class ResetPassword(generics.GenericAPIView):

    serializer_class = ResetPasswordSerializer
    permission_classes = []

    def post(self, request, token):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        new_password = data["new_password"]
        confirm_password = data["confirm_password"]

        if new_password != confirm_password:
            return Response({"error": "Passwords do not match"}, status=400)

        reset_obj = PasswordReset.objects.filter(token=token).first()

        if not reset_obj:
            return Response({"error": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if not user:
            return Response({"error": "No user found"}, status=404)

        user.set_password(new_password)
        user.save()

        reset_obj.delete()

        send_password_changed_email(user)

        return Response({"success": "Password updated"}, status=200)