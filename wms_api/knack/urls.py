# knack/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    InstrumentViewSet,
    LesTypeViewSet,
    LesTariefViewSet,
    LocatieViewSet,
    DocentViewSet,
)

router = DefaultRouter()
router.register(r"instrumenten", InstrumentViewSet)
router.register(r"lestypes", LesTypeViewSet)
router.register(r"lestarieven", LesTariefViewSet)
router.register(r"locaties", LocatieViewSet)
router.register(r"docenten", DocentViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
