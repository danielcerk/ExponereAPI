from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import date

from api.address.models import Address

from django.utils import timezone
import uuid

from django.conf import settings

class UserManager(BaseUserManager):

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_user(
        self,
        username,
        email=None,
        first_name=None,
        last_name=None,
        password=None,
        terms_of_use_is_ready=False,
        is_affiliate=False,
        owner=None,
        role="reader",
        catalog=None,
    ):
        if not email:
            raise ValueError("O usuário deve ter um endereço de email.")

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            terms_of_use_is_ready=terms_of_use_is_ready,
            is_affiliate=is_affiliate,
            owner=owner,
            role=role,
            catalog=catalog if catalog else (owner.catalog if owner else None),
        )

        if password:
            user.set_password(password)

        user.full_clean()
        user.save(using=self._db)

        return user

    def create_superuser(
        self,
        email,
        username=None,
        password=None,
        first_name=None,
        last_name=None,
        **extra_fields
    ):
        user = self.create_user(
            username=username or email,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
            role="admin",
        )

        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.owner = user  # ele é o próprio dono

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = (
        ("admin", "Administrador"),
        ("reader", "Leitor"),
    )

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)

    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)

    owner = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="team_members",
        verbose_name="Dono do workspace"
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="reader"
    )

    catalog = models.ForeignKey(
        "catalog.Catalog",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users"
    )

    is_affiliate = models.BooleanField(default=False)
    terms_of_use_is_ready = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def save(self, *args, **kwargs):

        self.full_name = f"{self.first_name or ''} {self.last_name or ''}".strip()

        if not self.catalog and self.owner:

            self.catalog = self.owner.catalog

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.role})"

    class Meta:

        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'


class Profile(models.Model):

    user = models.OneToOneField(
         
        UserProfile, on_delete=models.CASCADE, 
        verbose_name='Usuário'

    )

    cpf_cnpj = models.CharField(
        verbose_name='CPF ou CNPJ',
        max_length=18,
        validators=[
            RegexValidator(
                regex=r'^(\d{3}\.\d{3}\.\d{3}-\d{2}|\d{2}\.\d{3}\.\d{3}/\d{4}-\d{2})$',
                message='Digite um CPF (XXX.XXX.XXX-XX) ou CNPJ (XX.XXX.XXX/XXXX-XX) válido'
            )
        ],
        unique=True,
        null=True,
        blank=True
    )

    slug = models.SlugField(

        unique=True, max_length=100,
        null=True, blank=True

    )
    whatsapp = models.CharField(
        verbose_name='WhatsApp',
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+?55\d{10,11}$',
                message='Digite um número válido com DDD (ex: +5511999999999)'
            )
        ],
        null=True,
        blank=True
    )

    address = models.ForeignKey(
         
        Address, on_delete=models.SET_NULL,
        verbose_name='Endereço', null=True

    )

    created_at = models.DateTimeField(
        verbose_name='Criado em',
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        verbose_name='Atualizado em',
        auto_now=True
    )

    def save(self, *args, **kwargs):

        base_slug = slugify(self.user.username)
        slug = base_slug
        counter = 1

        while Profile.objects.exclude(pk=self.pk).filter(slug=slug).exists():

            slug = f'{base_slug}-{counter}'
            counter += 1

        self.slug = slug

        super().save(*args, **kwargs)

    class Meta:

        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'

    def __str__(self):

        return f'Perfil de {self.user.username} - {self.user.id}'
    
class PasswordReset(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="password_resets"
    )

    email = models.EmailField()

    token = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False
    )

    is_used = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    expires_at = models.DateTimeField()

    used_at = models.DateTimeField(
        null=True,
        blank=True
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    class Meta:

        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["token"]),
        ]
        ordering = ["-created_at"]

    def is_expired(self):

        return timezone.now() > self.expires_at

    def mark_as_used(self):

        self.is_used = True
        self.used_at = timezone.now()

        self.save(update_fields=["is_used", "used_at"])

    def __str__(self):

        return f"Password reset for {self.email}"