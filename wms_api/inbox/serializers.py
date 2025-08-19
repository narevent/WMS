# inbox/serializers.py
from rest_framework import serializers
from .models import Bericht, Proefles, Betalingsplichtige, Inschrijving


class BerichtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bericht
        fields = "__all__"
        read_only_fields = ("created_at",)


class ProeflesSerializer(serializers.ModelSerializer):
    instrument_naam = serializers.CharField(source="instrument.naam", read_only=True)

    class Meta:
        model = Proefles
        fields = "__all__"
        read_only_fields = ("created_at",)


class BetalingsplichtigenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Betalingsplichtige
        fields = "__all__"
        read_only_fields = ("created_at",)


class InschrijvingSerializer(serializers.ModelSerializer):
    instrument_naam = serializers.CharField(source="instrument.naam", read_only=True)
    lestype_beschrijving = serializers.CharField(
        source="lestype.beschrijving", read_only=True
    )
    betalingsplichtige_naam = serializers.SerializerMethodField()

    class Meta:
        model = Inschrijving
        fields = "__all__"
        read_only_fields = ("created_at",)

    def get_betalingsplichtige_naam(self, obj):
        return f"{obj.betalingsplichtige.initialen} {obj.betalingsplichtige.achternaam}"
