# wms_frontend/settings/development.py
from .base import *

SECRET_KEY = "django-insecure-change-me-frontend"
DEBUG = True
ALLOWED_HOSTS = ['*']

API_BASE_URL = "http://localhost:8000/api/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'