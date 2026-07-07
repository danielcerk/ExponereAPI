from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import (

    AllowAny,
    IsAuthenticated,
    BasePermission,
    SAFE_METHODS

)
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, action

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

from django_otp.plugins.otp_totp.models import TOTPDevice

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from dj_rest_auth.registration.views import SocialLoginView

import requests
import os

from google.oauth2 import id_token
from google.auth.transport import requests

from .models import PasswordReset 
from .utils import get_client_ip, get_user_agent
from .serializers import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    AccountSerializer,
    ResetPasswordRequestSerializer,
    ResetPasswordSerializer
)


from datetime import timedelta

from api.notification.tasks import (
    send_password_reset_email_task,
    send_password_changed_email_task
)

User = get_user_model()

class IsOwner(BasePermission):

    def has_permission(self, request, view):

        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:

            return True

        return obj.pk == request.user.pk

class MyTokenObtainPairView(TokenObtainPairView):

    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

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
    permission_classes = [IsOwner]

    def get_queryset(self):

        return User.objects.filter(id=self.request.user.pk)
    
    @action(detail=False, methods=['get', 'put', 'patch', 'delete'])
    def me(self, request):
        user = request.user

        if request.method == 'GET':
            return Response(self.get_serializer(user).data)

        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=(request.method == 'PATCH')
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)

        if request.method == 'DELETE':
            user.delete()
            return Response(status=204)

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
        
'''class GoogleLogin(SocialLoginView):

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

        user, created = User.objects.get_or_create(email=email, defaults={"name": name})

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "name": user.name,
            }
        })'''

class GoogleLogin(APIView):

    def post(self, request):

        token = request.data.get("token")
        token = token.replace(" ", "").replace("\n", "")


        if not token:

            return Response({"error": "Token não enviado"}, status=400)

        try:

            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                settings.GOOGLE_OAUTH_CLIENT_ID
            )

        except ValueError:
            
            return Response({"error": "Token inválido"}, status=400)

        email = idinfo.get("email")
        username = idinfo.get("name")

        user, _ = User.objects.get_or_create(
            email=email,
            defaults={"username": username}
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "username": user.username,
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

            reset = PasswordReset(
                user=user,
                email=email,
                token=token,
                expires_at=timezone.now() + timedelta(hours=1),
                ip_address=get_client_ip(request),
                user_agent=get_user_agent(request)
            )
            reset.save()

            if not settings.DEBUG:

                reset_url = f"https://exponere.com.br/auth/reset/password/update/{token}/"

            else:

                reset_url = f"http://127.0.0.1:8000/api/v1/auth/reset/password/update/{token}/"

            send_password_reset_email_task(user, reset_url)

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

        reset_obj = PasswordReset.objects.filter(
            token=token,
            is_used=False
        ).first()

        if not reset_obj:

            return Response({"error": "Invalid token"}, status=400)

        user = User.objects.filter(email=reset_obj.email).first()

        if not user:

            return Response({"error": "No user found"}, status=404)

        user.set_password(new_password)
        user.save()

        reset_obj.is_used = True
        reset_obj.used_at = timezone.now()

        reset_obj.save()

        send_password_changed_email_task(user)

        return Response({"success": "Senha atualizada"}, status=200)