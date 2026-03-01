from django.db import models

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from datetime import date

from api.address.models import Address

class UserManager(BaseUserManager):

	def create_user(self, username, email=None, first_name=None, last_name=None, password=None):

		if not email:

			raise ValueError('O usuário deve ter um endereço de email.')

		email = self.normalize_email(email)
		user = self.model(username=username, email=email,
			first_name=first_name, last_name=last_name,)

		if password:

			user.set_password(password)

		user.full_clean()
		user.save(using=self._db)

		return user

	def create_superuser(self, username, email, password, first_name=None, last_name=None):

		user = self.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )
		user.is_superuser = True
		user.is_staff = True

		user.save(using=self._db)

		return user

class UserProfile(AbstractBaseUser, PermissionsMixin):
    
    username = models.CharField(
		max_length=255, 
		verbose_name='Nome de usuário',
		unique=True
	)
    email = models.EmailField(
		max_length=255, 
		unique=True, 
		verbose_name='Email'
	)
    first_name = models.CharField(
		max_length=30, 
		blank=True, null=True, 
		verbose_name='Primeiro nome'
	)
    last_name = models.CharField(
		max_length=150, 
		blank=True, null=True, 
		verbose_name='Último nome'
	)
    
    full_name = models.CharField(
		max_length=255, 
		blank=True, null=True, 
		verbose_name='Nome completo'
	)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    is_active = models.BooleanField(default=True, verbose_name="Está ativo")
    is_staff = models.BooleanField(default=False, verbose_name='É moderador')
    is_superuser = models.BooleanField(default=False, verbose_name='É superusuário')
    
    def __str__(self):
        
        return f'Usuário {self.username} - {self.id}'
    
    def save(self, *args, **kwargs):

        self.full_name = f'{self.first_name} {self.last_name}'
        
        if self.pk is None or not UserProfile.objects.filter(pk=self.pk).exists():

            if self.password and not self.password.startswith('pbkdf2_'):

                self.set_password(self.password)
        else:
    
            old = UserProfile.objects.get(pk=self.pk)

            if self.password != old.password and not self.password.startswith('pbkdf2_'):
                
                self.set_password(self.password)

        super().save(*args, **kwargs)   
        
    class Meta:
         
        verbose_name = 'Usuário'
        verbose_name_plural ='Usuários'


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