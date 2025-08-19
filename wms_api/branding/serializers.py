# branding/serializers.py

from rest_framework import serializers
from .models import BrandingAsset, DesignPattern

class BrandingAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrandingAsset
        fields = [
            "id",
            "logo",
            "icon",
            "font_file",
        ]

class DesignPatternSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignPattern
        fields = [
            "id",
            "primary_color",
            "secondary_color",
            "accent_color",
            "font_family",
        ]