from rest_framework import __version__
from rest_framework.routers import DefaultRouter

from tests.app.views import ExplosiveViewSet
from tests.app.views import QuoteViewSet
from tests.app.views import SnippetViewSet
from tests.app.views import CityViewSet

v = tuple([int(x) for x in __version__.split(".")])
basename = "basename" if v >= (3, 9) else "base_name"

router = DefaultRouter()
router.register(r"quotes", QuoteViewSet, **{basename: "api-quote"})
router.register(r"snippets", SnippetViewSet, **{basename: "api-snippet"})
router.register(r"explosives", ExplosiveViewSet, **{basename: "api-explosive"})
router.register(r"cities", CityViewSet, **{basename: "api-city"})
urlpatterns = router.urls
