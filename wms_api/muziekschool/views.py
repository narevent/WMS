# muziekschool/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Over,
    Vacature,
    Contact,
    Header,
    Banner,
    Voorwaarde,
)
from .serializers import (
    OverSerializer,
    VacatureSerializer,
    ContactSerializer,
    HeaderSerializer,
    BannerSerializer,
    VoorwaardeSerializer,
)

class OverViewSet(viewsets.ModelViewSet):
    queryset = Over.objects.all()
    serializer_class = OverSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["titel", "info"]
    ordering_fields = ["titel", "created_at"]
    ordering = ["titel"]

class VacatureViewSet(viewsets.ModelViewSet):
    queryset = Vacature.objects.all()
    serializer_class = VacatureSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "instrumenten"]
    search_fields = ["functie", "beschrijving"]
    ordering_fields = ["functie", "created_at"]
    ordering = ["functie"]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["organisatie", "adres", "plaats", "email"]
    ordering_fields = ["organisatie", "updated_at"]
    ordering = ["organisatie"]

@api_view(['GET'])
def contact_info(request):
    contact = Contact.objects.first()
    return Response({
        "address": contact.address,
        "phone": contact.phone,
        "email": contact.email,
    })

class HeaderViewSet(viewsets.ModelViewSet):
    queryset = Header.objects.all()
    serializer_class = HeaderSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["titel", "info"]
    ordering_fields = ["titel", "created_at"]
    ordering = ["titel"]

class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["titel", "info"]
    ordering_fields = ["titel", "created_at"]
    ordering = ["titel"]

class VoorwaardeViewSet(viewsets.ModelViewSet):
    queryset = Voorwaarde.objects.all()
    serializer_class = VoorwaardeSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "titel"]
    search_fields = ["titel"]
    ordering_fields = ["titel", "created_at"]
    ordering = ["titel"]

