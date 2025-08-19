# knack/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Instrument, LesType, LesTarief, Locatie, Docent
from .serializers import (
    InstrumentSerializer,
    LesTypeSerializer,
    LesTariefSerializer,
    LocatieSerializer,
    DocentSerializer,
)


class InstrumentViewSet(viewsets.ModelViewSet):
    queryset = Instrument.objects.all()
    serializer_class = InstrumentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["naam", "beschrijving"]
    ordering_fields = ["naam", "created_at"]
    ordering = ["naam"]


class LesTypeViewSet(viewsets.ModelViewSet):
    queryset = LesType.objects.all()
    serializer_class = LesTypeSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "duur"]
    search_fields = ["soort", "beschrijving"]
    ordering_fields = ["soort", "duur", "created_at"]
    ordering = ["soort", "duur"]


class LesTariefViewSet(viewsets.ModelViewSet):
    queryset = LesTarief.objects.all()
    serializer_class = LesTariefSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "type"]
    search_fields = ["type__soort", "type__beschrijving"]
    ordering_fields = ["prijs_ex", "prijs_inc", "created_at"]
    ordering = ["type__soort", "prijs_ex"]


class LocatieViewSet(viewsets.ModelViewSet):
    queryset = Locatie.objects.all()
    serializer_class = LocatieSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["naam", "adres"]
    ordering_fields = ["naam", "created_at"]
    ordering = ["naam"]


class DocentViewSet(viewsets.ModelViewSet):
    queryset = Docent.objects.all()
    serializer_class = DocentSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "instrumenten"]
    search_fields = ["naam", "bio"]
    ordering_fields = ["naam", "created_at"]
    ordering = ["naam"]
