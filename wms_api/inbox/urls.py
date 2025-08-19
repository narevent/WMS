# inbox/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    BerichtViewSet,
    ProeflesViewSet,
    BetalingsplichtigenViewSet,
    InschrijvingViewSet,
)

router = DefaultRouter()
router.register(r"berichten", BerichtViewSet)
router.register(r"proeflessen", ProeflesViewSet)
router.register(r"betalingsplichtigen", BetalingsplichtigenViewSet)
router.register(r"inschrijvingen", InschrijvingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
