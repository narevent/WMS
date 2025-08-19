# activiteiten/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CursusViewSet,
    WorkshopViewSet,
    ProjectViewSet,
    GroepViewSet,
)

router = DefaultRouter()
router.register(r"cursussen", CursusViewSet)
router.register(r"workshops", WorkshopViewSet)
router.register(r"projecten", ProjectViewSet)
router.register(r"groepen", GroepViewSet)
urlpatterns = [
    path("", include(router.urls)),
]
