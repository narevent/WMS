# agenda/views.py
from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Post, Event, Vakantie
from .serializers import PostSerializer, EventSerializer, VakantieSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["titel", "content"]
    ordering_fields = ["titel"]
    ordering = ["-updated_at"]


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["datum"]
    search_fields = ["titel", "beschrijving"]
    ordering_fields = ["datum", "titel"]
    ordering = ["datum", "aanvang"]


class VakantieViewSet(viewsets.ModelViewSet):
    queryset = Vakantie.objects.all()
    serializer_class = VakantieSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["start", "eind"]
    search_fields = ["naam"]
    ordering_fields = ["start", "eind", "naam"]
    ordering = ["start"]
