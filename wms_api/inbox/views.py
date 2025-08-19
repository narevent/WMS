# inbox/views.py
from rest_framework import viewsets, filters, status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from typing import Dict
import requests
import json
from django.conf import settings
from .models import Bericht, Proefles, Betalingsplichtige, Inschrijving
from .serializers import (
    BerichtSerializer,
    ProeflesSerializer,
    BetalingsplichtigenSerializer,
    InschrijvingSerializer,
)

from knack.utility import END_POINTS, URL_POST
from knack.utility import get_header, get_token

class ExternalAPISyncMixin:
    """
    Mixin to add external API synchronization capabilities to ViewSets.
    """
    
    def get_sync_endpoint_config(self):
        """
        Override this method to return the endpoint configuration for the model.
        Should return (scene_id, view_id) tuple.
        """
        model_name = self.get_queryset().model.__name__
        if hasattr(self, 'sync_endpoint_key'):
            endpoint_key = self.sync_endpoint_key
        else:
            endpoint_key = model_name
            
        return END_POINTS.get(endpoint_key, {}).get("add")
    
    def get_sync_data(self, instance):
        """
        Override this method to customize the data sent to external API.
        By default, uses the serializer's data.
        """
        serializer = self.get_serializer(instance)
        return serializer.data
    
    def should_sync_to_external_api(self, instance, action='create'):
        """
        Override this method to add conditions for when to sync.
        Returns True by default.
        """
        return True
    
    def sync_to_external_api(self, instance, action='create'):
        """
        Sync the instance to external API.
        """
        if not self.should_sync_to_external_api(instance, action):
            return
            
        try:
            endpoint_config = self.get_sync_endpoint_config()
            if not endpoint_config:
                print(f"No endpoint configuration found for {instance.__class__.__name__}")
                return
                
            scene_id, view_id = endpoint_config
            token = get_token()
            headers = get_header(token)
            url = URL_POST % (scene_id, view_id)
            
            sync_data = self.get_sync_data(instance)
            
            response = requests.post(
                url,
                data=json.dumps(sync_data),
                headers=headers
            )
            
            if response.status_code in [200, 201]:
                print(f"Successfully synced {instance.__class__.__name__} {instance.id} to external API")
            else:
                print(f"Failed to sync {instance.__class__.__name__} {instance.id}: {response.text}")
                
        except Exception as e:
            print(f"Error syncing {instance.__class__.__name__} to external API: {str(e)}")
    
    def perform_create(self, serializer):
        instance = serializer.save()
        self.sync_to_external_api(instance, action='create')
        return instance
    
    def perform_update(self, serializer):
        instance = serializer.save()
        self.sync_to_external_api(instance, action='update')
        return instance

class ProeflesViewSet(ExternalAPISyncMixin, viewsets.ModelViewSet):
    queryset = Proefles.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = ProeflesSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "instrument"]
    search_fields = ["naam", "email", "telefoon"]
    ordering_fields = ["created_at", "naam"]
    ordering = ["-created_at"]
    
    def get_sync_data(self, instance):
        """Customize the data sent to external API for Proefles"""
        return {
            'naam': instance.naam,
            'email': instance.email,
            'telefoon': instance.telefoon,
            'status': instance.status,
            'instrument': instance.instrument.id,
        }
    
    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        proefles = self.get_object()
        new_status = request.data.get("status")
        if new_status in ["pending", "scheduled", "completed", "cancelled"]:
            proefles.status = new_status
            proefles.save()
            return Response({"status": f"updated to {new_status}"})
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

class BerichtViewSet(ExternalAPISyncMixin, viewsets.ModelViewSet):
    queryset = Bericht.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BerichtSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["is_read"]
    search_fields = ["naam", "email", "bericht"]
    ordering_fields = ["created_at", "naam"]
    ordering = ["-created_at"]
    
    def get_sync_data(self, instance):
        """Customize the data sent to external API for Bericht"""
        return {
            'naam': instance.naam,
            'email': instance.email,
            'bericht': instance.bericht,
            'is_read': instance.is_read,
        }
    
    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        bericht = self.get_object()
        bericht.is_read = True
        bericht.save()
        return Response({"status": "marked as read"})

class BetalingsplichtigenViewSet(ExternalAPISyncMixin, viewsets.ModelViewSet):
    queryset = Betalingsplichtige.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = BetalingsplichtigenSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["haarlempas", "akkoord"]
    search_fields = ["initialen", "achternaam", "adres", "plaats"]
    ordering_fields = ["created_at", "achternaam"]
    ordering = ["achternaam", "initialen"]
    
    sync_endpoint_key = "Betalingsplichtige"
    
    def get_sync_data(self, instance):
        """Customize the data sent to external API for Betalingsplichtige"""
        return {
            'initialen': instance.initialen,
            'achternaam': instance.achternaam,
            'adres': instance.adres,
            'plaats': instance.plaats,
            'haarlempas': instance.haarlempas,
            'akkoord': instance.akkoord,
        }

class InschrijvingViewSet(ExternalAPISyncMixin, viewsets.ModelViewSet):
    queryset = Inschrijving.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = InschrijvingSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["status", "instrument", "lestype", "huren"]
    search_fields = ["voornaam", "achternaam", "email", "telefoon"]
    ordering_fields = ["created_at", "achternaam", "geboortedatum"]
    ordering = ["-created_at"]
    
    def get_sync_data(self, instance):
        """Customize the data sent to external API for Inschrijving"""
        return {
            'voornaam': instance.voornaam,
            'achternaam': instance.achternaam,
            'email': instance.email,
            'telefoon': instance.telefoon,
            'geboortedatum': instance.geboortedatum.isoformat() if instance.geboortedatum else None,
            'status': instance.status,
            'instrument': instance.instrument.id if instance.instrument else None,
            'lestype': instance.lestype,
            'huren': instance.huren,
        }
    
    @action(detail=True, methods=["post"])
    def update_status(self, request, pk=None):
        inschrijving = self.get_object()
        new_status = request.data.get("status")
        if new_status in ["pending", "approved", "rejected", "active", "inactive"]:
            inschrijving.status = new_status
            inschrijving.save()
            return Response({"status": f"updated to {new_status}"})
        return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)