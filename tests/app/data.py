# coding: utf-8
from django.http import Http404
from mock_django.query import QuerySetMock

from tests.app.models import City
from tests.app.models import Continent
from tests.app.models import Country
from tests.app.models import Explosive
from tests.app.models import Province
from tests.app.models import Quote
from tests.app.models import Region
from tests.app.models import Snippet


def get_quote_list():
    """canned data for a list-view response"""
    quote1 = Quote(
        character="Michael Scott",
        line="I… Declare…. Bankruptcy!",
        episode="3x10",
    )
    quote2 = Quote(
        character="Dwight Schrute",
        line="Always the Padawan, never the Jedi.",
        episode="5x04",
    )
    return [quote1, quote2]


def get_quote_object(pk=None):
    """canned data far a detail-view response"""
    if pk != "parrot":
        raise Http404
    q = Quote(
        character="Stanley Hudson",
        line="Did I stutter?",
        episode="4x07",
    )
    return q


def get_snippet_queryset():
    s1 = Snippet(id=1, title="Fork bomb", code=":(){ :|: & };:", language="bash")
    s2 = Snippet(
        id=2,
        title="French flag",
        code="print((u'\x1b[3%s;1m\u2588'*78+u'\n')%((4,)*26+(7,)*26+(1,)*26)*30)",
    )
    snippets_qs = QuerySetMock(Snippet, s1, s2)
    return snippets_qs


def get_snippet_model_instance(pk=None):
    if int(pk) != 3:
        raise Http404
    code = '[ $[ $RANDOM % 6 ] == 0 ] && rm -rf / || echo "click"'
    snippet = Snippet(id=3, title="Russian roulette", code=code, language="bash")
    return snippet


def get_explosive_list():
    bomb1 = Explosive(safe="green wire", boom="red wire")
    bomb2 = Explosive(safe="helium", boom="hydrogen")
    return [bomb1, bomb2]


def get_explosive_object(pk=None):
    if pk != "bunger":
        raise Http404
    return Explosive(safe="tom thumb", boom="poha")


def get_cities_list():
    continent1 = Continent(
        id=1,
        name="Europe",
        code="EU",
    )
    continent2 = Continent(
        id=2,
        name="America",
        code="AM",
    )
    country1 = Country(
        id=1,
        name="Spain",
        code="ES",
        continent=continent1,
    )
    country2 = Country(
        id=2,
        name="Argentina",
        code="AR",
        continent=continent2,
    )
    country3 = Country(
        id=3,
        name="Colombia",
        code="CO",
        continent=continent2,
    )
    region1 = Region(
        id=1,
        name="Andalucía",
        code="AN",
        country=country1,
    )
    region2 = Region(
        id=2,
        name="Pampa",
        code="PA",
        country=country2,
    )
    region3 = Region(
        id=3,
        name="Andina",
        code="AN",
        country=country3,
    )
    province1 = Province(
        id=1,
        name="Málaga",
        code="MA",
        region=region1,
    )
    province2 = Province(
        id=2,
        name="Buenos Aires",
        code="BA",
        region=region2,
    )
    province3 = Province(
        id=3,
        name="Antioquía",
        code="AN",
        region=region3,
    )
    city1 = City(
        id=1,
        name="Ronda",
        code="RO",
        province=province1,
    )
    city2 = City(
        id=2,
        name="La Plata",
        code="LP",
        province=province2,
    )
    city3 = City(
        id=3,
        name="Medellín",
        code="ME",
        province=province3,
    )
    return [city1, city2, city3]


def get_city_object(pk=None):
    if int(pk) != 1:
        raise Http404
    continent = Continent(
        id=1,
        name="Europe",
        code="EU",
    )
    country = Country(
        id=1,
        name="Spain",
        code="ES",
        continent=continent,
    )
    region = Region(
        id=1,
        name="Andalucía",
        code="AN",
        country=country,
    )
    province = Province(
        id=1,
        name="Málaga",
        code="MA",
        region=region,
    )
    city = City(
        id=1,
        name="Ronda",
        code="RO",
        province=province,
    )
    return city
