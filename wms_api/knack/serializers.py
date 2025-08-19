# knack/serializers.py
from rest_framework import serializers
from .models import Instrument, LesType, LesTarief, Locatie, Docent


class InstrumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Instrument
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class LesTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LesType
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class LesTariefSerializer(serializers.ModelSerializer):
    type_naam = serializers.CharField(source="type.soort", read_only=True)
    type_beschrijving = serializers.CharField(
        source="type.beschrijving", read_only=True
    )

    class Meta:
        model = LesTarief
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class LocatieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Locatie
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")


class DocentSerializer(serializers.ModelSerializer):
    instrumenten_namen = serializers.StringRelatedField(
        source="instrumenten", many=True, read_only=True
    )

    class Meta:
        model = Docent
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
