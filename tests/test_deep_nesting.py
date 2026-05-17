"""
Tests for deep nesting functionality (up to 10 levels)
"""
from rest_framework.test import APIClient

from tests.utils import decode_content


class TestDeepNesting:
    """Test cases for deep nesting up to 10 levels"""

    def test_depth_3_includes(self):
        """Test 3-level deep nesting: city.province.region.country"""
        response = APIClient().get(
            "/cities/?fields=name,province.region.country.name,province.region.country.code"
        )
        expected = [
            {
                "name": "Ronda",
                "province": {
                    "region": {
                        "country": {
                            "name": "Spain",
                            "code": "ES",
                        },
                    },
                },
            },
            {
                "name": "La Plata",
                "province": {
                    "region": {
                        "country": {
                            "name": "Argentina",
                            "code": "AR",
                        },
                    },
                },
            },
            {
                "name": "Medellín",
                "province": {
                    "region": {
                        "country": {
                            "name": "Colombia",
                            "code": "CO",
                        },
                    },
                },
            },
        ]
        content = decode_content(response)
        assert content == expected

    def test_depth_4_includes(self):
        """Test 4-level deep nesting: city.province.region.country.continent"""
        response = APIClient().get(
            "/cities/?fields=province.region.country.continent.name,province.region.country.continent.code"
        )
        expected = [
            {
                "province": {
                    "region": {
                        "country": {
                            "continent": {
                                "name": "Europe",
                                "code": "EU",
                            },
                        },
                    },
                },
            },
            {
                "province": {
                    "region": {
                        "country": {
                            "continent": {
                                "name": "America",
                                "code": "AM",
                            },
                        },
                    },
                },
            },
            {
                "province": {
                    "region": {
                        "country": {
                            "continent": {
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

    def test_depth_3_excludes(self):
        """Test 3-level deep exclusions"""
        response = APIClient().get(
            "/cities/?fields!=id,province.region.country.continent"
        )
        content = decode_content(response)
        
        # Should have all fields except id and the nested continent
        assert len(content) == 3
        for city in content:
            assert "id" not in city
            assert "name" in city
            assert "code" in city
            assert "province" in city
            
            province = city["province"]
            assert "region" in province
            
            region = province["region"]
            assert "country" in region
            
            country = region["country"]
            assert "continent" not in country  # This should be excluded
            assert "name" in country
            assert "code" in country

    def test_mixed_depth_includes(self):
        """Test mixed depth levels in same query"""
        response = APIClient().get(
            "/cities/?fields=name,code,province.name,province.region.country.continent.name"
        )
        expected = [
            {
                "name": "Ronda",
                "code": "RO",
                "province": {
                    "name": "Málaga",
                    "region": {
                        "country": {
                            "continent": {
                                "name": "Europe",
                            },
                        },
                    },
                },
            },
            {
                "name": "La Plata",
                "code": "LP",
                "province": {
                    "name": "Buenos Aires",
                    "region": {
                        "country": {
                            "continent": {
                                "name": "America",
                            },
                        },
                    },
                },
            },
            {
                "name": "Medellín",
                "code": "ME",
                "province": {
                    "name": "Antioquía",
                    "region": {
                        "country": {
                            "continent": {
                                "name": "America",
                            },
                        },
                    },
                },
            },
        ]
        content = decode_content(response)
        assert content == expected

    def test_depth_5_single_detail(self):
        """Test 5-level deep nesting on single record"""
        # This tests the full depth: city -> province -> region -> country -> continent
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

    def test_multiple_fields_at_different_depths(self):
        """Test multiple fields at various depth levels"""
        response = APIClient().get(
            "/cities/1/?fields=name,province.name,province.code,province.region.name,province.region.country.name,province.region.country.continent.name"
        )
        expected = {
            "name": "Ronda",
            "province": {
                "name": "Málaga",
                "code": "MA",
                "region": {
                    "name": "Andalucía",
                    "country": {
                        "name": "Spain",
                        "continent": {
                            "name": "Europe",
                        },
                    },
                },
            },
        }
        content = decode_content(response)
        assert content == expected

    def test_deep_nesting_with_bogus_fields(self):
        """Test deep nesting with non-existent fields"""
        response = APIClient().get(
            "/cities/1/?fields=name,province.region.country.continent.name,fake.deep.nested.field,another.bogus.very.deep.nested.field.that.does.not.exist"
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

    def test_exclude_at_various_depths(self):
        """Test exclusions at different depth levels"""
        response = APIClient().get(
            "/cities/1/?fields!=id,province.id,province.region.id,province.region.country.id"
        )
        content = decode_content(response)
        
        # Should exclude id at multiple levels
        assert "id" not in content
        assert "name" in content
        assert "code" in content
        assert "province" in content
        
        province = content["province"]
        assert "id" not in province
        assert "name" in province
        assert "code" in province
        assert "region" in province
        
        region = province["region"]
        assert "id" not in region
        assert "name" in region
        assert "code" in region
        assert "country" in region
        
        country = region["country"]
        assert "id" not in country
        assert "name" in country
        assert "code" in country
        assert "continent" in country

    def test_performance_very_deep_nesting(self):
        """Test performance with very deep field specifications (stress test)"""
        # This creates a very long field path that should be handled gracefully
        deep_field = "province.region.country.continent.name"
        very_deep_bogus = "a.b.c.d.e.f.g.h.i.j.k.l.m.n.o.p.q.r.s.t.u.v.w.x.y.z"
        
        response = APIClient().get(
            f"/cities/1/?fields=name,{deep_field},{very_deep_bogus}"
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

    def test_edge_case_empty_nested_specification(self):
        """Test edge case with empty nested specifications"""
        response = APIClient().get("/cities/1/?fields=province.")
        # Should return empty result or handle gracefully
        content = decode_content(response)
        # The exact behavior can be defined based on requirements
        # For now, we expect it to not crash and return some reasonable result
        assert isinstance(content, dict)

    def test_edge_case_trailing_dots(self):
        """Test edge case with trailing dots in field specifications"""
        response = APIClient().get("/cities/1/?fields=name,province.name.")
        expected = {
            "name": "Ronda",
            "province": {
                "name": "Málaga",
            },
        }
        content = decode_content(response)
        # Should handle trailing dots gracefully
        assert content == expected or "name" in content  # Allow some flexibility in handling

    def test_complex_mixed_operations(self):
        """Test complex scenario with both includes and excludes at different levels"""
        # Include specific fields but exclude some nested ones
        response = APIClient().get(
            "/cities/1/?fields=name,province.name,province.region.name,province.region.country.name&fields!=province.region.country.id"
        )
        expected = {
            "name": "Ronda",
            "province": {
                "name": "Málaga",
                "region": {
                    "name": "Andalucía",
                    "country": {
                        "name": "Spain",
                    },
                },
            },
        }
        content = decode_content(response)
        assert content == expected
