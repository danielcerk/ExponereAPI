# Editar env gh actions
# Criar imagem docker ( "docker image build -t exponere_api:1.0 ." , )
# Criar docker compose

# Adicionar models para horário de funcionamento ( Catalogo ) *
# Adicionar recuperação de senha *
# Adicionar Product ( Adicionar novos serializers e incorporar o stock, category serializer em product, views e urls, tests )
# Adicionar Estoque ( Completar Serializer e Signals, tests )
# Adicionar Order ( models, admin, signals, views, urls, tests )
# Adicionar sistema de cupom ( Signals, Views, Urls, testes )
# Adicionar sistema de frete ( API MelhorEnvio, models, admin, signals, views, urls, testes )
# Adicionar sistema de SEO ( Signals - para criar automaticamente keywords ) *

# Adicionar Plugin ( GA4, tag manager e Pixel Facebook, Pagseguro com django-pagseguro para pagamentos dos lojistas, Gestão de estoque, Sacolinha do Instagram )
# Adicionar Analytics ( Com dados de orders e de plugins dos analytics )
# Adicionar ( Serviço para plano PRO ) de dominio personalizado, ou seja, ao invés de /loja, loja.exponere.com.br

# Fazer testes unitários e de integração
# Adicionar consultas com elastic search

import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

from dotenv import load_dotenv

from urllib.parse import urlparse, parse_qsl
from datetime import timedelta

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = [

    '127.0.0.1',
    'localhost',
    'exponere.com.br'

]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_hotp',
    'django_otp.plugins.otp_static',

    'api',
    'api.analytic',
    'api.auth',
    'api.catalog',
    'api.category',
    'api.order',
    'api.plugin',
    'api.product',
    'api.wishlist',
    'api.SEO',
    'api.shipping',
    'api.stock',
    'api.subscription',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'corsheaders',
    'cities_light',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    'allauth.socialaccount.providers.google',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django_otp.middleware.OTPMiddleware',
    'core.middleware.APIKeyMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

AUTH_USER_MODEL = 'api_custom_auth.UserProfile'
WSGI_APPLICATION = 'core.wsgi.application'

if DEBUG:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:

    tmpPostgres = urlparse(os.getenv("DATABASE_URL"))

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': tmpPostgres.path.replace('/', ''),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': 5432,
            'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

CORS_ALLOWED_ORIGINS = [

    'http://localhost:3000',

]

CSRF_TRUSTED_ORIGINS =  [

    'http://localhost:3000',

]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True
USE_L10N = True
USE_THOUSAND_SEPARATOR = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

API_KEY = os.getenv('API_KEY')

SPECTACULAR_SETTINGS = {
    'TITLE': 'Exponere API',
    'DESCRIPTION': 'Exponere API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    },
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=180),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=50),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',

    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

CITIES_LIGHT_INCLUDE_COUNTRIES = ['BR']

if DEBUG:

    DOMAIN = os.getenv('STRIPE_LOCAL_DOMAIN_WEBHOOK')

    STRIPE_SECRET_KEY = os.getenv('STRIPE_TEST_SECRET_KEY')
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_TEST_PUBLIC_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_TEST_WEBHOOK_SECRET')

    STRIPE_LOCAL_PLAN_PREMIUM = os.getenv('STRIPE_LOCAL_PLAN_PREMIUM')
    STRIPE_LOCAL_PLAN_PREMIUM_2 = os.getenv('STRIPE_LOCAL_PLAN_PREMIUM_2')

else:

    DOMAIN = os.getenv('STRIPE_PROD_DOMAIN_WEHBOOK')

    STRIPE_SECRET_KEY = os.getenv('STRIPE_PROD_SECRET_KEY')
    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PROD_PUBLIC_KEY')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_PROD_WEBHOOK_SECRET')

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'suporteconstsoft@gmail.com'
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',
)

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_LOGIN_METHODS = {'email'}
ACCOUNT_USERNAME_REQUIRED = False 
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True

GOOGLE_OAUTH_CLIENT_ID = os.getenv('GOOGLE_OAUTH_CLIENT_ID') 
GOOGLE_OAUTH_CLIENT_SECRET = os.getenv('GOOGLE_OAUTH_CLIENT_SECRET')

if DEBUG:

    GOOGLE_OAUTH_CALLBACK_URL = 'http://localhost:3000/api/v1/auth/google/callback/'

else:

    GOOGLE_OAUTH_CALLBACK_URL = os.getenv('GOOGLE_OAUTH_CALLBACK_URL')

SOCIALACCOUNT_EMAIL_AUTHENTICATION = True

SOCIALACCOUNT_EMAIL_AUTHENTICATION_AUTO_CONNECT = True
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APPS": [
            {
                "client_id": GOOGLE_OAUTH_CLIENT_ID,
                "secret": GOOGLE_OAUTH_CLIENT_SECRET,
                "key": "",
            },
        ],
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {
            "access_type": "online",
        },
    }
}