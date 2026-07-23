from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import authenticate
from django.conf import settings

from .models import Profile

from api.address.serializers import AddressSerializer

User = get_user_model()

DEBUG = settings.DEBUG

class ResetPasswordRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$',
        write_only=True,
        error_messages={
            "invalid": "Password must be at least 8 characters long with at least one capital letter and one symbol."
        }
    )

    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:

            raise serializers.ValidationError({

                "confirm_password": "Passwords do not match."

            })
        
        return attrs

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    otp = serializers.CharField(required=False, write_only=True)

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["email"] = user.email
        token["username"] = user.username

        return token

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")
        otp = attrs.get("otp")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password
        )

        if not user:
            raise serializers.ValidationError("Credenciais inválidas")

        device = TOTPDevice.objects.filter(user=user, confirmed=True).first()

        if device:

            if not otp:

                raise serializers.ValidationError("OTP obrigatório")

            if not device.verify_token(otp):

                raise serializers.ValidationError("OTP inválido")

        attrs["user"] = user

        return super().validate(attrs)


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    if not DEBUG:

        password = serializers.RegexField(
            regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z0-9]).{8,}$',
            write_only=True,
            error_messages={
                "invalid": "Password must be at least 8 characters long with at least one capital letter and one symbol."
            }
        )

    else:

        password = serializers.CharField(write_only=True, required=True)

    role = serializers.ChoiceField(
        choices=User.ROLE_CHOICES,
        default="reader",
        required=False
    )

    class Meta:
        
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'terms_of_use_is_ready',
            'is_affiliate',
            'role',
        )

        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def create(self, validated_data):

        request = self.context.get("request")
        current_user = request.user if request else None

        role = validated_data.pop("role", "reader")

        if current_user and current_user.is_authenticated:

            if current_user.role != "admin":

                raise serializers.ValidationError("Sem permissão para criar usuários.")

            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                password=validated_data['password'],
                terms_of_use_is_ready=validated_data.get('terms_of_use_is_ready', False),
                is_affiliate=validated_data.get('is_affiliate', False),
                owner=current_user.owner or current_user,
                role=role,
                catalog=current_user.catalog,
            )

        else:

            user = User.objects.create_user(
                username=validated_data['username'],
                email=validated_data['email'],
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                password=validated_data['password'],
                terms_of_use_is_ready=validated_data.get('terms_of_use_is_ready', False),
                is_affiliate=validated_data.get('is_affiliate', False),

                role="admin",
            )

        return user
    
class ProfileSerializer(serializers.ModelSerializer):

    cpf_cnpj = serializers.CharField(
        required=False,
        allow_null=True,
        allow_blank=True
    )

    address = AddressSerializer(required=False)

    class Meta:
        
        model = Profile
        fields = '__all__'

    def run_validation(self, data=serializers.empty):

        if self.parent and getattr(self.parent, "instance", None):
            self.instance = self.parent.instance.profile

        return super().run_validation(data)

    def validate_cpf_cnpj(self, value):

        if not value:
            return value

        queryset = Profile.objects.filter(cpf_cnpj=value)

        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)

        if queryset.exists():

            raise serializers.ValidationError(
                "Perfil com este CPF ou CNPJ já existe."
            )

        return value

    def update(self, instance, validated_data):

        address_data = validated_data.pop('address', None)

        instance = super().update(instance, validated_data)

        if address_data:

            if instance.address:

                addr_serializer = AddressSerializer(
                    instance.address,
                    data=address_data,
                    partial=True
                )

                addr_serializer.is_valid(raise_exception=True)
                addr_serializer.save()

            else:

                addr_serializer = AddressSerializer(data=address_data)
                addr_serializer.is_valid(raise_exception=True)
                addr_instance = addr_serializer.save()
                
                instance.address = addr_instance
                instance.save(update_fields=['address'])

        return instance
    
class AccountSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer(required=False)

    password = serializers.CharField(
        write_only=True,
        required=False
    )

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'full_name',
            'email',
            'password',
            'profile',
            'role',
            'catalog'
        )

        read_only_fields = (
            'id', 'is_active', 'is_staff', 'is_superuser',
            'created_at', 'updated_at'
        )

        extra_kwargs = {
            'username': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'email': {'required': False},
            'password': {'required': False},
        }

    def update(self, instance, validated_data):

        password = validated_data.pop("password", None)
        profile_data = validated_data.pop("profile", None)


        if password:

            instance.password = make_password(password)

        for attr in ('username', 'first_name', 'last_name', 'email'):

            if attr in validated_data:

                setattr(instance, attr, validated_data[attr])

        instance.save()

        if profile_data:

            profile_serializer = ProfileSerializer(
                instance.profile,
                data=profile_data,
                partial=True,
                context=self.context
            )

            profile_serializer.is_valid(raise_exception=True)
            profile_serializer.save()

        return instance
