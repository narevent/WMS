# stichting/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OvereenkomstViewSet,
    SponsorViewSet,
    AnbiViewSet,
    DocumentViewSet,
)

router = DefaultRouter()
router.register(r"overeenkomsten", OvereenkomstViewSet)
router.register(r"sponsors", SponsorViewSet)
router.register(r"anbi", AnbiViewSet)
router.register(r"documents", DocumentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
