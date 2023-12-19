from rest_framework import serializers

from drf_nestedqueryfields import NestedQueryFieldsMixin
from tests.app.fields import BoomField
from tests.app.models import Snippet


class QuoteSerializer(NestedQueryFieldsMixin, serializers.Serializer):
    character = serializers.CharField()
    line = serializers.CharField()
    episode = serializers.CharField()


class SnippetSerializer(NestedQueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Snippet
        exclude = ()


class ExplosiveSerializer(NestedQueryFieldsMixin, serializers.Serializer):
    safe = serializers.CharField()
    boom = BoomField()
