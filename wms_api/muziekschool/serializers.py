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
    Voorwaarde,
)
from knack.models import Instrument


class BaseModelSerializer(serializers.ModelSerializer):
    class Meta:
        abstract = True
        read_only_fields = (
            "created_at",
            "updated_at",
        )

class OverSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Over
        fields = "__all__"


class VacatureSerializer(BaseModelSerializer):
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
        super().__init__(*args, **kwargs)
        self.fields["instrumenten_ids"].queryset = Instrument.objects.all()


class ContactSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Contact
        fields = "__all__"


class HeaderSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Header
        fields = "__all__"

class BannerSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Banner
        fields = "__all__"

class VoorwaardeSerializer(BaseModelSerializer):
    class Meta(BaseModelSerializer.Meta):
        model = Voorwaarde
        fields = "__all__"