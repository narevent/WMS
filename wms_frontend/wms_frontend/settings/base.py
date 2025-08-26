# wms_frontend/settings/__init__.py (REQUIRED - makes settings a Python package)
# This file can be empty, but it MUST exist

# wms_frontend/settings/base.py (shared settings)
from pathlib import Path
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # Go up 3 levels from settings/base.py

# Shared settings between development and production
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'activiteiten',
    'agenda',
    'api_client',
    'main',
    'muziekles',
    'stichting',
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

ROOT_URLCONF = 'wms_frontend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.branding_context',
                'main.context_processors.contact_info',
            ],
        },
    },
]

WSGI_APPLICATION = 'wms_frontend.wsgi.application'

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = 'nl-nl'
TIME_ZONE = 'Europe/Amsterdam'

DATETIME_FORMAT = "d-m-Y H:i"
DATE_FORMAT = "d-m-Y"
TIME_FORMAT = "H:i"
USE_L10N = False

DATETIME_INPUT_FORMATS = ["%d-%m-%Y %H:%M"]
DATE_INPUT_FORMATS = ["%d-%m-%Y"]

USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

DJANGO_USERNAME = config("DJANGO_USERNAME")
DJANGO_PASSWORD = config("DJANGO_PASSWORD")