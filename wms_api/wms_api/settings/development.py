# settings/development.py
from .base import *

SECRET_KEY = "django-insecure-change-me"
DEBUG = True
ALLOWED_HOSTS = ['*']

API_BASE_URL = "http://localhost:8000/api/"

DATABASES = {
    "default": {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True