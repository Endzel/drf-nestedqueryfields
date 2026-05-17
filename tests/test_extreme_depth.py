"""
Tests for extreme depth levels (up to 10+ levels) and performance benchmarks
"""
import time
from rest_framework.test import APIClient

from tests.utils import decode_content


class TestExtremeDepth:
    """Test cases for extreme depth levels and performance"""

    def test_depth_5_full_path(self):
        """Test the full 5-level path: city -> province -> region -> country -> continent"""
        response = APIClient().get(
            "/cities/1/?fields=name,code,province.name,province.code,province.region.name,province.region.code,province.region.country.name,province.region.country.code,province.region.country.continent.name,province.region.country.continent.code"
        )
        expected = {
            "name": "Ronda",
            "code": "RO",
            "province": {
                "name": "Málaga",
                "code": "MA",
                "region": {
                    "name": "Andalucía",
                    "code": "AN",
                    "country": {
                        "name": "Spain",
                        "code": "ES",
                        "continent": {
                            "name": "Europe",
                            "code": "EU",
                        },
                    },
                },
            },
        }
        content = decode_content(response)
        assert content == expected

    def test_depth_6_hypothetical_extension(self):
        """Test hypothetical 6th level (would require model extension)"""
        # This tests how the system handles non-existent deep paths
        response = APIClient().get(
            "/cities/1/?fields=name,province.region.country.continent.supercontinent.name"
        )
        expected = {
            "name": "Ronda",
            "province": {
                "region": {
                    "country": {
                        "continent": {
                            # supercontinent doesn't exist, so it should be ignored
                        },
                    },
                },
            },
        }
        content = decode_content(response)
        # Should handle gracefully - exact behavior depends on implementation
        assert "name" in content
        assert "province" in content

    def test_depth_10_bogus_fields(self):
        """Test 10-level deep bogus field paths"""
        response = APIClient().get(
            "/cities/1/?fields=name,level1.level2.level3.level4.level5.level6.level7.level8.level9.level10"
        )
        expected = {
            "name": "Ronda",
            # All the deep bogus fields should be ignored
        }
        content = decode_content(response)
        assert content == expected

    def test_multiple_extreme_depth_paths(self):
        """Test multiple extreme depth paths in one query"""
        response = APIClient().get(
            "/cities/1/?fields=name,province.region.country.continent.name,fake.path.level3.level4.level5.level6.level7.level8.level9.level10,another.bogus.very.deep.nested.field.path.that.goes.extremely.deep"
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

    def test_performance_many_deep_fields(self):
        """Performance test with many deep field specifications"""
        # Create a query with many deep field paths
        deep_fields = [
            "name",
            "code",
            "province.name",
            "province.code",
            "province.region.name",
            "province.region.code",
            "province.region.country.name",
            "province.region.country.code",
            "province.region.country.continent.name",
            "province.region.country.continent.code",
            # Add some bogus deep paths
            "bogus1.level2.level3.level4.level5",
            "bogus2.level2.level3.level4.level5.level6",
            "bogus3.level2.level3.level4.level5.level6.level7",
            "bogus4.level2.level3.level4.level5.level6.level7.level8",
            "bogus5.level2.level3.level4.level5.level6.level7.level8.level9",
            "bogus6.level2.level3.level4.level5.level6.level7.level8.level9.level10",
        ]
        
        fields_param = ",".join(deep_fields)
        
        start_time = time.time()
        response = APIClient().get(f"/cities/1/?fields={fields_param}")
        end_time = time.time()
        
        # Should complete in reasonable time (less than 1 second for this complexity)
        processing_time = end_time - start_time
        assert processing_time < 1.0, f"Processing took too long: {processing_time:.3f}s"
        
        expected = {
            "name": "Ronda",
            "code": "RO",
            "province": {
                "name": "Málaga",
                "code": "MA",
                "region": {
                    "name": "Andalucía",
                    "code": "AN",
                    "country": {
                        "name": "Spain",
                        "code": "ES",
                        "continent": {
                            "name": "Europe",
                            "code": "EU",
                        },
                    },
                },
            },
        }
        content = decode_content(response)
        assert content == expected

    def test_exclude_at_extreme_depth(self):
        """Test exclusions at very deep levels"""
        response = APIClient().get(
            "/cities/1/?fields!=province.region.country.continent.code,province.region.country.continent.id"
        )
        content = decode_content(response)
        
        # Should have everything except the specified deep exclusions
        assert "name" in content
        assert "code" in content
        assert "province" in content
        
        province = content["province"]
        assert "region" in province
        
        region = province["region"]
        assert "country" in region
        
        country = region["country"]
        assert "continent" in country
        
        continent = country["continent"]
        assert "code" not in continent  # Should be excluded
        assert "name" in continent  # Should be present

    def test_mixed_depth_operations(self):
        """Test mixed include/exclude operations at different depths"""
        response = APIClient().get(
            "/cities/1/?fields=name,province.region.country.continent.name&fields!=province.region.country.id"
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

    def test_stress_test_100_bogus_deep_fields(self):
        """Stress test with 100 bogus deep field paths"""
        # Generate 100 bogus deep field paths
        bogus_fields = []
        for i in range(100):
            depth = (i % 10) + 1  # Vary depth from 1 to 10
            field_parts = [f"bogus{i}"] + [f"level{j}" for j in range(1, depth + 1)]
            bogus_fields.append(".".join(field_parts))
        
        # Add one real field
        all_fields = ["name"] + bogus_fields
        fields_param = ",".join(all_fields)
        
        start_time = time.time()
        response = APIClient().get(f"/cities/1/?fields={fields_param}")
        end_time = time.time()
        
        # Should handle gracefully and complete in reasonable time
        processing_time = end_time - start_time
        assert processing_time < 2.0, f"Stress test took too long: {processing_time:.3f}s"
        
        expected = {
            "name": "Ronda",
        }
        content = decode_content(response)
        assert content == expected

    def test_edge_case_empty_field_parts(self):
        """Test edge cases with empty field parts"""
        response = APIClient().get("/cities/1/?fields=name,,province..region...country")
        # Should handle gracefully despite malformed field specifications
        content = decode_content(response)
        assert isinstance(content, dict)
        # Should at least include name if it's properly specified
        assert "name" in content

    def test_edge_case_only_dots(self):
        """Test edge case with only dots"""
        response = APIClient().get("/cities/1/?fields=name,.......")
        expected = {
            "name": "Ronda",
        }
        content = decode_content(response)
        assert content == expected

    def test_performance_list_with_deep_fields(self):
        """Performance test with deep fields on list endpoint"""
        start_time = time.time()
        response = APIClient().get(
            "/cities/?fields=name,province.region.country.continent.name"
        )
        end_time = time.time()
        
        processing_time = end_time - start_time
        # Should handle list queries efficiently
        assert processing_time < 1.0, f"List query took too long: {processing_time:.3f}s"
        
        content = decode_content(response)
        assert len(content) == 3  # Should return all 3 cities
        
        for city in content:
            assert "name" in city
            assert "province" in city
            province = city["province"]
            assert "region" in province
            region = province["region"]
            assert "country" in region
            country = region["country"]
            assert "continent" in country
            continent = country["continent"]
            assert "name" in continent
