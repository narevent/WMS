# muziekschool/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    OverViewSet,
    VacatureViewSet,
    ContactViewSet,
    contact_info,
    HeaderViewSet,
    BannerViewSet,
)

router = DefaultRouter()
router.register(r"over", OverViewSet)
router.register(r"contact", ContactViewSet)
router.register(r"vacatures", VacatureViewSet)
router.register(r"headers", HeaderViewSet)
router.register(r"banners", BannerViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("contact_info", contact_info, name='contact_info'),
]
