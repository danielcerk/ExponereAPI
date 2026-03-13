from rest_framework import serializers

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator

from django.contrib.auth import get_user_model

from .models import Profile

from django.contrib.auth.hashers import make_password
from django_otp.plugins.otp_totp.models import TOTPDevice
from django.contrib.auth import authenticate

from api.address.serializers import AddressSerializer

User = get_user_model()

class ResetPasswordRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.RegexField(
        regex=r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$',
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
        required=True, validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    password = serializers.CharField(
        write_only=True, required=True, 
    )

    class Meta:

        model = User
        fields = ('username', 
            'first_name', 'last_name', 
            'email', 'password', 'terms_of_use_is_ready')
        
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            email=validated_data['email'],
            terms_of_use_is_ready=validated_data['terms_of_use_is_ready']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user
    
class ProfileSerializer(serializers.ModelSerializer):

    address = AddressSerializer(required=False)

    class Meta:
        
        model = Profile
        fields = '__all__'

        read_only_fields = [

            'id', 'user', 'created_at',
            'updated_at'

        ]

    def update(self, instance, validated_data):

        instance = super().update(instance, validated_data)

        return instance
    
class AccountSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        
        model = User
        fields = (
            'id', 'username', 
            'first_name', 'last_name',
            'email','password', 'profile'
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
