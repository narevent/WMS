from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from .models import BrandingAsset, DesignPattern
from .serializers import BrandingAssetSerializer, DesignPatternSerializer

class BrandingAssetsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BrandingAsset.objects.all()
    serializer_class = BrandingAssetSerializer
    permission_classes = [AllowAny]

class DesignPatternsViewSet(viewsets.ModelViewSet):
    queryset = DesignPattern.objects.all()
    serializer_class = DesignPatternSerializer
    permission_classes = [AllowAny]