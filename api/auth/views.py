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
)

from django.contrib.auth import get_user_model
from rest_framework.parsers import MultiPartParser, FormParser

from django_otp.plugins.otp_totp.models import TOTPDevice
from rest_framework.decorators import api_view, permission_classes

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