# stichting/serializers.py
from rest_framework import serializers
from .models import (
    Overeenkomst,
    Sponsor,
    Anbi,
    Document,
)


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer for models inheriting from BaseModel.
    Sets read_only_fields for created_at and updated_at.
    """

    class Meta:
        abstract = True
        read_only_fields = (
            "created_at",
            "updated_at",
        )

class OvereenkomstSerializer(BaseModelSerializer):
    """Serializer for the Overeenkomst model."""

    class Meta(BaseModelSerializer.Meta):
        model = Overeenkomst
        fields = "__all__"

class SponsorSerializer(BaseModelSerializer):
    """Serializer for the Sponsor model."""

    class Meta(BaseModelSerializer.Meta):
        model = Sponsor
        fields = "__all__"


class AnbiSerializer(BaseModelSerializer):
    """Serializer for the Anbi model."""

    class Meta(BaseModelSerializer.Meta):
        model = Anbi
        fields = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = "__all__"