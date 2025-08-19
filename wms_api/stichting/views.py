# stichting/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Overeenkomst,
    Sponsor,
    Anbi,
    Document,
)
from .serializers import (
    OvereenkomstSerializer,
    SponsorSerializer,
    AnbiSerializer,
    DocumentSerializer,
)

class OvereenkomstViewSet(viewsets.ModelViewSet):
    queryset = Overeenkomst.objects.all()
    serializer_class = OvereenkomstSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["naam", "beschrijving"]
    ordering_fields = ["naam", "created_at"]
    ordering = ["naam"]


class SponsorViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all().order_by('-priority')
    serializer_class = SponsorSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["naam", "beschrijving"]
    ordering_fields = ["priority"]
    ordering = ["-priority"]


class AnbiViewSet(viewsets.ModelViewSet):
    queryset = Anbi.objects.all()
    serializer_class = AnbiSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["beschrijving"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

class DocumentViewSet(viewsets.ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["title"]
    search_fields = ["title"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
