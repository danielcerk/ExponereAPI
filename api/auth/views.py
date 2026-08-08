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
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    TokenError,
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.decorators import api_view, permission_classes, action

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
from django.conf import settings
from django.contrib.auth import get_user_model

from django_otp.plugins.otp_totp.models import TOTPDevice

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client

from google_auth_oauthlib.flow import Flow
from google.oauth2 import id_token
from google.auth.transport import requests

from dj_rest_auth.registration.views import SocialLoginView

import traceback
import requests as http_requests
import os

from .models import PasswordReset 
from .utils import get_client_ip, get_user_agent, generate_unique_username
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

class LogoutAPIView(
    APIView
):

    permission_classes = (
        IsAuthenticated,
    )

    def post(
        self,
        request
    ):

        refresh_token = (
            request.data.get(
                "refresh_token"
            )
        )

        if not refresh_token:

            return Response(
                {
                    "detail":
                    "Refresh token é obrigatório."
                },
                status=(
                    status
                    .HTTP_400_BAD_REQUEST
                ),
            )

        try:

            token = RefreshToken(
                refresh_token
            )

            token.blacklist()

            return Response(
                {
                    "detail":
                    "Logout realizado com sucesso."
                },
                status=(
                    status
                    .HTTP_205_RESET_CONTENT
                ),
            )

        except TokenError:

            return Response(
                {
                    "detail":
                    "Refresh token inválido."
                },
                status=(
                    status
                    .HTTP_400_BAD_REQUEST
                ),
            )

class GoogleLogin(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        code = request.data.get("code")

        if not code:
            return Response({"error": "Código não enviado"}, status=400)

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
                    "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
            ],
            redirect_uri="postmessage",
        )

        try:

            flow.fetch_token(code=code)

        except Exception as e:

            traceback.print_exc()

            return Response({"error": str(e)}, status=400)

        credentials = flow.credentials

        idinfo = id_token.verify_oauth2_token(
            credentials.id_token,
            requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID,
        )

        email = idinfo["email"]
        name = idinfo.get("name") or email.split("@")[0]

        username = User.generate_unique_username(name)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                "username": username,
                "first_name": idinfo.get("given_name", ""),
                "last_name": idinfo.get("family_name", ""),
            },
        )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": {
                "email": user.email,
                "username": user.username,
            },
        })

class FacebookLogin(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        access_token = request.data.get("access_token")

        if not access_token:
            return Response(
                {"error": "Token não enviado"},
                status=400,
            )

        try:

            app_access_token = (
                f"{settings.FACEBOOK_APP_ID}|"
                f"{settings.FACEBOOK_APP_SECRET}"
            )

            debug_response = http_requests.get(
                "https://graph.facebook.com/debug_token",
                params={
                    "input_token": access_token,
                    "access_token": app_access_token,
                },
                timeout=10,
            )

            if debug_response.status_code != 200:
                return Response(
                    {"error": "Não foi possível validar o token do Facebook"},
                    status=400,
                )

            debug_data = debug_response.json()

            if "data" not in debug_data:
                return Response(
                    {"error": "Resposta inválida do Facebook"},
                    status=400,
                )

            token_data = debug_data["data"]

            if not token_data.get("is_valid"):
                return Response(
                    {"error": "Token do Facebook inválido"},
                    status=400,
                )

            if str(token_data.get("app_id")) != str(
                settings.FACEBOOK_APP_ID
            ):
                return Response(
                    {"error": "Token não pertence a esta aplicação"},
                    status=400,
                )

            facebook_id = token_data.get("user_id")

            if not facebook_id:
                return Response(
                    {"error": "ID do usuário não encontrado"},
                    status=400,
                )

            user_response = http_requests.get(
                "https://graph.facebook.com/me",
                params={
                    "fields": "id,email,name,first_name,last_name",
                    "access_token": access_token,
                },
                timeout=10,
            )

            if user_response.status_code != 200:
                return Response(
                    {"error": "Não foi possível obter os dados do Facebook"},
                    status=400,
                )

            facebook_data = user_response.json()

            if str(facebook_data.get("id")) != str(facebook_id):
                return Response(
                    {"error": "Usuário do token não corresponde ao usuário retornado"},
                    status=400,
                )

            email = facebook_data.get("email")

            if not email:
                return Response(
                    {
                        "error": (
                            "O Facebook não forneceu um endereço de e-mail. "
                            "Verifique se a permissão de e-mail foi concedida."
                        )
                    },
                    status=400,
                )

            name = facebook_data.get("name") or email.split("@")[0]

            first_name = facebook_data.get("first_name", "")
            last_name = facebook_data.get("last_name", "")

            username = User.generate_unique_username(name)

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": username,
                    "first_name": first_name,
                    "last_name": last_name,
                },
            )

            refresh = RefreshToken.for_user(user)

            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "email": user.email,
                    "username": user.username,
                },
            })

        except requests.RequestException as e:

            return Response(
                {
                    "error": "Erro ao comunicar com o Facebook",
                    "detail": str(e),
                },
                status=400,
            )

        except Exception as e:

            return Response(
                {
                    "error": "Erro ao autenticar com o Facebook",
                    "detail": str(e),
                },
                status=400,
            )

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

                reset_url = f"https://app.exponere.com.br/recuperar-senha/{token}/resetar-senha"

            else:

                reset_url = f"http://localhost:3000/recuperar-senha/{token}/resetar-senha"

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