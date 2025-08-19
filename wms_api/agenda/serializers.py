from rest_framework import serializers
from .models import Post, Event, Vakantie


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = "__all__"


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = "__all__"


class VakantieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vakantie
        fields = "__all__"
