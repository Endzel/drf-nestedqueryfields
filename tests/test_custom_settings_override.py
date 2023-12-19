from django.test import override_settings
from rest_framework.test import APIClient

from tests.utils import decode_content


@override_settings(DRF_NESTEDQUERYFIELDS_INCLUDE_ARG_NAME="include")
def test_list_response_filtered_includes():
    response = APIClient().get("/quotes/?include=character,episode")
    expected = [
        {
            "character": "Michael Scott",
            "episode": "3x10",
        },
        {
            "character": "Dwight Schrute",
            "episode": "5x04",
        },
    ]
    content = decode_content(response)
    assert content == expected


@override_settings(DRF_NESTEDQUERYFIELDS_EXCLUDE_ARG_NAME="omit")
def test_list_response_filtered_excludes():
    response = APIClient().get("/quotes/?omit=episode")
    expected = [
        {
            "character": "Michael Scott",
            "line": "I… Declare…. Bankruptcy!",
        },
        {
            "character": "Dwight Schrute",
            "line": "Always the Padawan, never the Jedi.",
        },
    ]
    content = decode_content(response)
    assert content == expected


@override_settings(DRF_NESTEDQUERYFIELDS_DELIMITER="|")
def test_list_response_filtered_delimiter():
    response = APIClient().get("/quotes/?fields=line|episode")
    expected = [
        {
            "line": "I… Declare…. Bankruptcy!",
            "episode": "3x10",
        },
        {
            "line": "Always the Padawan, never the Jedi.",
            "episode": "5x04",
        },
    ]
    content = decode_content(response)
    assert content == expected
