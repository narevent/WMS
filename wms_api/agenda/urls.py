# agenda/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, EventViewSet, VakantieViewSet

router = DefaultRouter()
router.register(r"posts", PostViewSet)
router.register(r"events", EventViewSet)
router.register(r"vakanties", VakantieViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
