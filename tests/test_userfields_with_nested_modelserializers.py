from rest_framework.test import APIClient

from tests.utils import decode_content


def test_model_list_response_unfiltered():
    response = APIClient().get("/cities/")
    expected = [
        {
            "id": 1,
            "name": "Ronda",
            "code": "RO",
            "province": {
                "id": 1,
                "name": "Málaga",
                "code": "MA",
                "region": {
                    "id": 1,
                    "name": "Andalucía",
                    "code": "AN",
                    "country": {
                        "id": 1,
                        "name": "Spain",
                        "code": "ES",
                        "continent": {
                            "id": 1,
                            "name": "Europe",
                            "code": "EU",
                        },
                    },
                },
            },
        },
        {
            "id": 2,
            "name": "La Plata",
            "code": "LP",
            "province": {
                "id": 2,
                "name": "Buenos Aires",
                "code": "BA",
                "region": {
                    "id": 2,
                    "name": "Pampa",
                    "code": "PA",
                    "country": {
                        "id": 2,
                        "name": "Argentina",
                        "code": "AR",
                        "continent": {
                            "id": 2,
                            "name": "America",
                            "code": "AM",
                        },
                    },
                },
            },
        },
        {
            "id": 3,
            "name": "Medellín",
            "code": "ME",
            "province": {
                "id": 3,
                "name": "Antioquía",
                "code": "AN",
                "region": {
                    "id": 3,
                    "name": "Andina",
                    "code": "AN",
                    "country": {
                        "id": 3,
                        "name": "Colombia",
                        "code": "CO",
                        "continent": {
                            "id": 2,
                            "name": "America",
                            "code": "AM",
                        },
                    },
                },
            },
        },
    ]
    content = decode_content(response)
    assert content == expected


def test_model_detail_response_unfiltered():
    response = APIClient().get("/cities/1/")
    expected = (
        {
            "id": 1,
            "name": "Ronda",
            "code": "RO",
            "province": {
                "id": 1,
                "name": "Málaga",
                "code": "MA",
                "region": {
                    "id": 1,
                    "name": "Andalucía",
                    "code": "AN",
                    "country": {
                        "id": 1,
                        "name": "Spain",
                        "code": "ES",
                        "continent": {
                            "id": 1,
                            "name": "Europe",
                            "code": "EU",
                        },
                    },
                },
            },
        },
    )
    content = decode_content(response)
    assert content == expected[0]


def test_model_list_response_filtered_first_level_includes():
    response = APIClient().get("/cities/?fields=name,province.name,province.code")
    expected = [
        {
            "name": "Ronda",
            "province": {
                "name": "Málaga",
                "code": "MA",
            },
        },
        {
            "name": "La Plata",
            "province": {
                "name": "Buenos Aires",
                "code": "BA",
            },
        },
        {
            "name": "Medellín",
            "province": {
                "name": "Antioquía",
                "code": "AN",
            },
        },
    ]
    content = decode_content(response)
    assert content == expected


def test_model_detail_response_filtered_first_level_includes():
    response = APIClient().get("/cities/1/?fields=name,province.name")
    expected = {
        "name": "Ronda",
        "province": {
            "name": "Málaga",
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_list_response_filtered_first_level_excludes():
    response = APIClient().get("/cities/?fields!=id,province.region,province.id")
    expected = [
        {
            "name": "Ronda",
            "code": "RO",
            "province": {
                "name": "Málaga",
                "code": "MA",
            },
        },
        {
            "name": "La Plata",
            "code": "LP",
            "province": {
                "name": "Buenos Aires",
                "code": "BA",
            },
        },
        {
            "name": "Medellín",
            "code": "ME",
            "province": {
                "name": "Antioquía",
                "code": "AN",
            },
        },
    ]
    content = decode_content(response)
    assert content == expected


def test_model_detail_response_filtered_first_level_excludes():
    response = APIClient().get("/cities/1/?fields!=id,province.region,province.id")
    expected = (
        {
            "name": "Ronda",
            "code": "RO",
            "province": {
                "name": "Málaga",
                "code": "MA",
            },
        },
    )
    content = decode_content(response)
    assert content == expected[0]


def test_model_response_filtered_first_level_with_some_bogus_fields():
    response = APIClient().get(
        "/cities/1/?fields=name,province.name,canned.spam,boiled.egg"
    )
    expected = {
        "name": "Ronda",
        "province": {
            "name": "Málaga",
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_response_filtered_multiple_levels_with_only_bogus_fields():
    response = APIClient().get(
        "/cities/1/?fields=blahhh.blahhh,bla.blah.blahh,blah.blahhhh.blahh.blahhh.blahhhh"
    )
    expected = {}
    content = decode_content(response)
    assert content == expected


def test_model_response_filtered_first_level_with_multiple_fields_in_separate_query_args():
    response = APIClient().get(
        "/cities/1/?fields=province.name&fields=name,province.code"
    )
    expected = {
        "name": "Ronda",
        "province": {
            "name": "Málaga",
            "code": "MA",
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_response_filtered_first_level_with_include_and_exclude():
    response = APIClient().get(
        "/cities/1/?fields=province.name&fields!=province.region"
    )
    expected = {
        "province": {
            "name": "Málaga",
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_list_response_filtered_second_level_includes():
    response = APIClient().get(
        "/cities/?fields=province.region.name,province.region.code"
    )
    expected = [
        {
            "province": {
                "region": {
                    "name": "Andalucía",
                    "code": "AN",
                },
            },
        },
        {
            "province": {
                "region": {
                    "name": "Pampa",
                    "code": "PA",
                },
            },
        },
        {
            "province": {
                "region": {
                    "name": "Andina",
                    "code": "AN",
                },
            },
        },
    ]
    content = decode_content(response)
    assert content == expected


def test_model_detail_response_filtered_second_level_includes():
    response = APIClient().get(
        "/cities/1/?fields=province.region.id,province.region.code"
    )
    expected = {
        "province": {
            "region": {"id": 1, "code": "AN"},
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_list_response_filtered_second_level_excludes():
    response = APIClient().get(
        "/cities/?fields!=id,province.region.id,province.region.country"
    )
    expected = [
        {
            "name": "Ronda",
            "code": "RO",
            "province": {
                "id": 1,
                "name": "Málaga",
                "code": "MA",
                "region": {
                    "name": "Andalucía",
                    "code": "AN",
                },
            },
        },
        {
            "name": "La Plata",
            "code": "LP",
            "province": {
                "id": 2,
                "name": "Buenos Aires",
                "code": "BA",
                "region": {
                    "name": "Pampa",
                    "code": "PA",
                },
            },
        },
        {
            "name": "Medellín",
            "code": "ME",
            "province": {
                "id": 3,
                "name": "Antioquía",
                "code": "AN",
                "region": {
                    "name": "Andina",
                    "code": "AN",
                },
            },
        },
    ]
    content = decode_content(response)
    assert content == expected


def test_model_detail_response_filtered_second_level_excludes():
    response = APIClient().get(
        "/cities/1/?fields!=id,province.region.code,province.region.country"
    )
    expected = (
        {
            "name": "Ronda",
            "code": "RO",
            "province": {
                "id": 1,
                "name": "Málaga",
                "code": "MA",
                "region": {
                    "id": 1,
                    "name": "Andalucía",
                },
            },
        },
    )
    content = decode_content(response)
    assert content == expected[0]


def test_model_response_filtered_second_level_with_some_bogus_fields():
    response = APIClient().get(
        "/cities/1/?fields=name,province.region.name,canned.cold.spam,boiled.fried.egg"
    )
    expected = {
        "name": "Ronda",
        "province": {
            "region": {
                "name": "Andalucía",
            },
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_response_filtered_third_level_includes():
    """Test 3-level deep nesting"""
    response = APIClient().get(
        "/cities/1/?fields=province.region.country.name,province.region.country.code"
    )
    expected = {
        "province": {
            "region": {
                "country": {
                    "name": "Spain",
                    "code": "ES",
                },
            },
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_response_filtered_fourth_level_includes():
    """Test 4-level deep nesting"""
    response = APIClient().get(
        "/cities/1/?fields=province.region.country.continent.name"
    )
    expected = {
        "province": {
            "region": {
                "country": {
                    "continent": {
                        "name": "Europe",
                    },
                },
            },
        },
    }
    content = decode_content(response)
    assert content == expected


def test_model_response_filtered_deep_excludes():
    """Test deep exclusions"""
    response = APIClient().get(
        "/cities/1/?fields!=id,province.region.country.continent"
    )
    content = decode_content(response)

    # Should have all fields except id and the deeply nested continent
    assert "id" not in content
    assert "name" in content
    assert "code" in content
    assert "province" in content

    province = content["province"]
    assert "region" in province

    region = province["region"]
    assert "country" in region

    country = region["country"]
    assert "continent" not in country  # This should be excluded


def test_model_response_extreme_depth_with_bogus():
    """Test very deep nesting with bogus fields (stress test)"""
    response = APIClient().get(
        "/cities/1/?fields=name,province.region.country.continent.name,fake.very.deep.nested.field.that.goes.ten.levels.deep.and.does.not.exist"
    )
    expected = {
        "name": "Ronda",
        "province": {
            "region": {
                "country": {
                    "continent": {
                        "name": "Europe",
                    },
                },
            },
        },
    }
    content = decode_content(response)
    assert content == expected
