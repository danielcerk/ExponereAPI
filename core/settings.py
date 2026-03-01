# Adicionar Product * ( Com multiplas imagens e multiplas categorias)
# Adicionar Wishlist * ( router vamos puxar Catalog e User )
# Adicionar Estoque ( Produto ) *
# Adicionar Order
# Adicionar sistema de cupom

# Fazer testes unitários e de integração
# Criar imagem docker

# Adicionar login com google
# Adicionar Plugin ( GA4, tag manager e Pixel Facebook, Pagseguro com django-pagseguro para pagamentos dos lojistas, e ERPs )
# Adicionar Analytics ( Com dados de orders e de plugins dos analytics )
# Ver se conseguimos integrar com sacolinha do Instagram e Catlaogo do Whatsapp

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
    'api.subscription',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'drf_spectacular',
    'corsheaders',
    'cities_light'
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