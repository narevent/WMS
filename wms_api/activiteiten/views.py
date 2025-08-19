# activiteiten/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Cursus,
    Workshop,
    Project,
    Groep,
)
from .serializers import (
    CursusSerializer,
    WorkshopSerializer,
    ProjectSerializer,
    GroepSerializer,
)

class CursusViewSet(viewsets.ModelViewSet):
    queryset = Cursus.objects.all()
    serializer_class = CursusSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "instrumenten"]
    search_fields = ["naam", "beschrijving"]
    ordering_fields = ["naam", "prijs", "created_at"]
    ordering = ["naam"]


class WorkshopViewSet(viewsets.ModelViewSet):
    queryset = Workshop.objects.all()
    serializer_class = WorkshopSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active", "instrumenten"]
    search_fields = ["naam", "beschrijving"]
    ordering_fields = ["naam", "prijs", "created_at"]
    ordering = ["naam"]


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["instrumenten"]
    search_fields = ["naam", "beschrijving"]
    ordering_fields = ["naam", "start", "end", "prijs", "created_at"]
    ordering = ["start", "naam"]


class GroepViewSet(viewsets.ModelViewSet):
    queryset = Groep.objects.all()
    serializer_class = GroepSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_active"]
    search_fields = ["naam", "beschrijving"]
    ordering_fields = ["naam", "created_at"]
    ordering = ["naam"]