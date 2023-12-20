from rest_framework import serializers

from drf_nestedqueryfields import NestedQueryFieldsMixin
from tests.app.fields import BoomField
from tests.app.models import City
from tests.app.models import Continent
from tests.app.models import Country
from tests.app.models import Province
from tests.app.models import Region
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


class ContinentSerializer(NestedQueryFieldsMixin, serializers.ModelSerializer):
    class Meta:
        model = Continent
        exclude = ()


class CountrySerializer(NestedQueryFieldsMixin, serializers.ModelSerializer):
    continent = ContinentSerializer()

    class Meta:
        model = Country
        exclude = ()


class RegionSerializer(NestedQueryFieldsMixin, serializers.ModelSerializer):
    country = CountrySerializer()

    class Meta:
        model = Region
        exclude = ()


class ProvinceSerializer(NestedQueryFieldsMixin, serializers.ModelSerializer):
    region = RegionSerializer()

    class Meta:
        model = Province
        exclude = ()


class CitySerializer(NestedQueryFieldsMixin, serializers.ModelSerializer):
    province = ProvinceSerializer()

    class Meta:
        model = City
        exclude = ()
