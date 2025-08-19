# branding/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BrandingAssetsViewSet, DesignPatternsViewSet

router = DefaultRouter()
router.register(r'assets', BrandingAssetsViewSet, basename='branding-assets')
router.register(r'design', DesignPatternsViewSet, basename='design-patterns')

urlpatterns = [
    path('', include(router.urls)),
]
