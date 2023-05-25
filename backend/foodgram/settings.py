import os
import socket
import string
from datetime import timedelta
from os import getenv
from pathlib import Path
from re import compile

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', default='django-insecure-1j#czt3k8&uc!i29flx$xfm0ee7vh@ovhqigz2fb&3u16#nvi+')

if socket.gethostname() in ('localhost','127.0.0.1', 'MaximuZ-Notebook'):
    DEBUG = True
else:
    DEBUG = False

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS', default='*')]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'djoser',
    'colorfield',
    'api.apps.ApiConfig',
    'recipes.apps.RecipesConfig',
    'users.apps.UsersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'foodgram.urls'

TEMPLATES_DIR = BASE_DIR / 'templates'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'foodgram.wsgi.application'

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv('DB_ENGINE',
                                default='django.db.backends.postgresql'),
            'NAME': os.getenv('DB_NAME', default='postgres'),
            'USER': os.getenv('POSTGRES_USER', default='postgres'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD', default='postgres'),
            'HOST': os.getenv('DB_HOST', default='db'),
            'PORT': os.getenv('DB_PORT', '5432')
        }
    }

AUTH_USER_MODEL = 'users.User'

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

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 6,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
}

DJOSER = {
    'SERIALIZERS': {
        'user_create': 'users.serializers.CustomUserCreateSerializer',
        'user': 'users.serializers.CustomUserSerializer',
        'current_user': 'users.serializers.CustomUserSerializer',
    },
    'LOGIN_FIELD': 'email',
    'SEND_ACTIVATION_EMAIL': False,
    'HIDE_USERS': False,
    'PERMISSIONS': {
        'user': ('djoser.permissions.CurrentUserOrAdminOrReadOnly',),
        'user_list': ('rest_framework.permissions.AllowAny',),
    },
}


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STRING_LENGTH = 150
STRING_MAX_LENGTH = 200
EMAIL_MAX_LENGTH = 254
HEX_COLOR_LENGTH = 7
MIN_COOKING_TIME = 1
MIN_AMOUNT_VALUE = 1
COOKING_TIME_ERROR_MESSAGE = f'Время приготовления должно быть не менее {MIN_COOKING_TIME}'
AMOUNT_VALUE_ERROR_MESSAGE = f'Количество ингредиента не может быть меньше {MIN_AMOUNT_VALUE}'
ROLE_ADMIN = 'admin'
ROLE_USER = 'user'
RESERVED_USERNAMES = ('me', )
USERNAME_INVALID_PATTERN = compile(r'[^\w.@+-]+')
SELF_SUBSCRIPTION_ERROR = 'Нельзя подписаться на самого себя!'
SAME_SUBSCRIPTION_ERROR = 'Нельзя повторно подписаться автора!'
ALREADY_IN_FAVORITES_ERROR = 'Этот рецепт уже в избранном!'
SAME_INGREDIENTS_ERROR = 'Ингредиенты не должны повторятся!'
NO_TAGS_ERROR = 'У рецепта должен быть хотябы один тег!'
SAME_TAGS_ERROR = 'Не должно быть одинаковых тегов!'
RECIPE_IN_CART_ERROR = 'Этот рецепт уже в списке покупок!'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
