from rest_framework.test import APIClient

from tests.app.serializers import QuoteSerializer
from tests.utils import decode_content


def test_list_response_unfiltered():
    response = APIClient().get("/quotes/")
    expected = [
        {
            "character": "Michael Scott",
            "line": "I… Declare…. Bankruptcy!",
            "episode": "3x10",
        },
        {
            "character": "Dwight Schrute",
            "line": "Always the Padawan, never the Jedi.",
            "episode": "5x04",
        },
    ]
    content = decode_content(response)
    assert content == expected


def test_detail_response_unfiltered():
    response = APIClient().get("/quotes/parrot/")
    expected = {
        "character": "Stanley Hudson",
        "line": "Did I stutter?",
        "episode": "4x07",
    }
    content = decode_content(response)
    assert content == expected


def test_list_response_filtered_includes():
    response = APIClient().get("/quotes/?fields=character,line")
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


def test_detail_response_filtered_includes():
    response = APIClient().get("/quotes/parrot/?fields=character,line")
    expected = {
        "character": "Stanley Hudson",
        "line": "Did I stutter?",
    }
    content = decode_content(response)
    assert content == expected


def test_list_response_filtered_excludes():
    response = APIClient().get("/quotes/?fields!=character")
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


def test_detail_response_filtered_excludes():
    response = APIClient().get("/quotes/parrot/?fields!=character")
    expected = {
        "line": "Did I stutter?",
        "episode": "4x07",
    }
    content = decode_content(response)
    assert content == expected


def test_response_filtered_with_some_bogus_fields():
    response = APIClient().get("/quotes/parrot/?fields=episode,spam,eggs")
    expected = {
        "episode": "4x07",
    }
    content = decode_content(response)
    assert content == expected


def test_response_filtered_with_only_bogus_fields():
    response = APIClient().get("/quotes/parrot/?fields=blah")
    expected = {}
    content = decode_content(response)
    assert content == expected


def test_response_filtered_with_multiple_fields_in_separate_query_args():
    response = APIClient().get("/quotes/parrot/?fields=character&fields=episode")
    expected = {
        "character": "Stanley Hudson",
        "episode": "4x07",
    }
    content = decode_content(response)
    assert content == expected


def test_response_filtered_with_include_and_exclude():
    response = APIClient().get(
        "/quotes/parrot/?fields=character&fields=episode&fields!=line"
    )
    expected = {
        "character": "Stanley Hudson",
        "episode": "4x07",
    }
    content = decode_content(response)
    assert content == expected


def test_exclude_wins_for_ambiguous_filtering():
    response = APIClient().get("/quotes/parrot/?fields=line,episode&fields!=line")
    expected = {
        "episode": "4x07",
    }
    content = decode_content(response)
    assert content == expected


def test_post_ignores_queryfields():
    # Ensures that fields aren't dropped for other types of request
    response = APIClient().post("/quotes/?fields=line,episode")
    expected = {
        "request_method": "POST",
        "serializer_instance_fields": ["character", "line", "episode"],
        "request_query": {"fields": "line,episode"},
    }
    content = decode_content(response)
    assert content == expected


def test_instantiate_without_request_context():
    # just test that it doesn't crash or b0rk the serializer to omit request context
    data = {
        "character": "the character",
        "episode": "the episode",
        "line": "the line",
    }
    serializer = QuoteSerializer(data=data)
    assert serializer.is_valid()
    assert sorted(serializer.get_fields()) == ["character", "episode", "line"]
