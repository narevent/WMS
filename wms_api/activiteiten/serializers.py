# activiteiten/serializers.py
from rest_framework import serializers
from knack.serializers import (
    InstrumentSerializer,
)
from .models import (
    Cursus,
    Workshop,
    Project,
    Groep,
)

from knack.models import Instrument


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        read_only_fields = (
            "created_at",
            "updated_at",
        )

class CursusSerializer(BaseModelSerializer):
    """
    Serializer for the Cursus model.
    Includes read-only representation of instruments and write-only field for instrument IDs.
    """

    instrumenten = InstrumentSerializer(many=True, read_only=True)
    instrumenten_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="instrumenten",
        queryset=Instrument.objects.none(),
    )

    class Meta(BaseModelSerializer.Meta):
        model = Cursus
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer and sets the queryset for instrumenten_ids.
        This is done dynamically to avoid circular imports.
        """
        super().__init__(*args, **kwargs)
        # Set the correct queryset here
        self.fields["instrumenten_ids"].queryset = Instrument.objects.all()


class WorkshopSerializer(BaseModelSerializer):
    """
    Serializer for the Workshop model.
    Includes read-only representation of instruments and write-only field for instrument IDs.
    """

    instrumenten = InstrumentSerializer(many=True, read_only=True)
    instrumenten_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="instrumenten",
        queryset=Instrument.objects.none(),
    )

    class Meta(BaseModelSerializer.Meta):
        model = Workshop
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer and sets the queryset for instrumenten_ids.
        This is done dynamically to avoid circular imports.
        """
        super().__init__(*args, **kwargs)
        self.fields["instrumenten_ids"].queryset = Instrument.objects.all()


class ProjectSerializer(BaseModelSerializer):
    """
    Serializer for the Project model.
    Includes read-only representation of instruments, write-only field for instrument IDs,
    and read-only fields for is_upcoming and is_ongoing properties.
    """

    instrumenten = InstrumentSerializer(many=True, read_only=True)
    instrumenten_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="instrumenten",
        queryset=Instrument.objects.none(),
    )
    is_upcoming = serializers.ReadOnlyField()
    is_ongoing = serializers.ReadOnlyField()

    class Meta(BaseModelSerializer.Meta):
        model = Project
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer and sets the queryset for instrumenten_ids.
        This is done dynamically to avoid circular imports.
        """
        super().__init__(*args, **kwargs)
        self.fields["instrumenten_ids"].queryset = Instrument.objects.all()


class GroepSerializer(BaseModelSerializer):
    """Serializer for the Groep model."""

    class Meta(BaseModelSerializer.Meta):
        model = Groep
        fields = "__all__"

