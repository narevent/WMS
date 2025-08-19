# muziekschool/serializers.py
from rest_framework import serializers
from knack.serializers import (
    InstrumentSerializer,
)
from .models import (
    Over,
    Vacature,
    Contact,
    Header,
    Banner,
)
from knack.models import Instrument


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

class OverSerializer(BaseModelSerializer):
    """Serializer for the Over model."""

    class Meta(BaseModelSerializer.Meta):
        model = Over
        fields = "__all__"


class VacatureSerializer(BaseModelSerializer):
    """
    Serializer for the Vacature model.
    Includes read-only representation of instruments, write-only field for instrument IDs,
    and a read-only field for the is_open property.
    """

    instrumenten = InstrumentSerializer(many=True, read_only=True)
    instrumenten_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        write_only=True,
        source="instrumenten",
        queryset=Instrument.objects.none(),
    )
    is_open = serializers.ReadOnlyField()

    class Meta(BaseModelSerializer.Meta):
        model = Vacature
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        """
        Initializes the serializer and sets the queryset for instrumenten_ids.
        This is done dynamically to avoid circular imports.
        """
        super().__init__(*args, **kwargs)
        self.fields["instrumenten_ids"].queryset = Instrument.objects.all()


class ContactSerializer(BaseModelSerializer):
    """Serializer for the Contact model."""

    class Meta(BaseModelSerializer.Meta):
        model = Contact
        fields = "__all__"


class HeaderSerializer(BaseModelSerializer):
    """Serializer for the Header model."""

    class Meta(BaseModelSerializer.Meta):
        model = Header
        fields = "__all__"

class BannerSerializer(BaseModelSerializer):
    """Serializer for the Header model."""

    class Meta(BaseModelSerializer.Meta):
        model = Banner
        fields = "__all__"