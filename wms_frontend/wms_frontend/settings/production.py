# wms_frontend/settings/production.py
from .base import *
from pathlib import Path
from decouple import config

SECRET_KEY = config("SECRET_KEY", default="django-insecure-change-me")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default='localhost').split(',')

API_BASE_URL = config("API_BASE_URL", default="http://localhost:8000/api/")
DOMAIN_URL = config("DOMAIN_URL", default="http://localhost:8000/")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/app/data/db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/app/staticfiles/'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media/'

# Security settings for production
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True