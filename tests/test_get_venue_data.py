import pytest
from source.venue_client import get_venue_data
from fastapi import HTTPException
import unittest.mock as mock

"""
this is similar to the tests in instrumentation, but in this case we seek out to
test the functionality of the function without having it depend on an external API.
"""

static_success_response = {"venue_raw": {"location": {"coordinates": [1, 2]}}}

dynamic_success_response = {
    "venue_raw": {
        "delivery_specs": {
            "order_minimum_no_surcharge": 1000,
            "delivery_pricing": {
                "base_price": 190,
                "distance_ranges": [
                    {"min": 0, "max": 500, "a": 0, "b": 0, "flag": None},
                    {"min": 500, "max": 1000, "a": 100, "b": 0, "flag": None},
                    {"min": 1000, "max": 1500, "a": 200, "b": 0, "flag": None},
                    {"min": 1500, "max": 2000, "a": 200, "b": 1, "flag": None},
                    {"min": 2000, "max": 0, "a": 0, "b": 0, "flag": None},
                ],
            },
        }
    }
}


@mock.patch("requests.get")
def test_gvd_static_fail(mock_get):
    mock_static_fail = mock.Mock()
    mock_static_fail.status_code = 402

    mock_dynamic = mock.Mock()
    mock_dynamic.status_code = 200
    mock_dynamic.json.return_value = dynamic_success_response

    mock_get.side_effect = [mock_static_fail, mock_dynamic]

    with pytest.raises(HTTPException) as exc:
        get_venue_data("test_venue")
    assert exc.value.status_code == 400
    assert exc.value.detail == {
        "static_data_error": "Static data request failed with status code 402"
    }


@mock.patch("requests.get")
def test_gvd_dynamic_fail(mock_get):
    mock_static = mock.Mock()
    mock_static.status_code = 200
    mock_static.json.return_value = static_success_response

    mock_dynamic_fail = mock.Mock()
    mock_dynamic_fail.status_code = 402

    mock_get.side_effect = [mock_static, mock_dynamic_fail]

    with pytest.raises(HTTPException) as exc:
        get_venue_data("test_venue")
    assert exc.value.status_code == 400
    assert exc.value.detail == {
        "dynamic_data_error": "Dynamic data request failed with status code 402"
    }


@mock.patch("requests.get")
def test_gvd_static_and_dynamic_fail(mock_get):
    mock_static_fail = mock.Mock()
    mock_static_fail.status_code = 402

    mock_dynamic_fail = mock.Mock()
    mock_dynamic_fail.status_code = 402

    mock_get.side_effect = [mock_static_fail, mock_dynamic_fail]

    with pytest.raises(HTTPException) as exc:
        get_venue_data("test_venue")
    assert exc.value.status_code == 400
    assert exc.value.detail == {
        "static_data_error": "Static data request failed with status code 402",
        "dynamic_data_error": "Dynamic data request failed with status code 402",
    }


@mock.patch("requests.get")
def test_gvd_KeyError(mock_get):
    mock_static = mock.Mock()
    mock_static.status_code = 200
    mock_static.json.return_value = {"venue_raw": {}}

    mock_dynamic = mock.Mock()
    mock_dynamic.status_code = 200
    mock_dynamic.json.return_value = dynamic_success_response

    mock_get.side_effect = [mock_static, mock_dynamic]

    with pytest.raises(HTTPException) as exc:
        get_venue_data("test_venue")

    assert exc.value.status_code == 400
    assert "Missing key" in exc.value.detail
    assert exc.value.detail == "Missing key in API response 'location'"


@mock.patch("requests.get")
def test_gvd_success(mock_get):
    mock_static = mock.Mock()
    mock_static.status_code = 200
    mock_static.json.return_value = static_success_response

    mock_dynamic = mock.Mock()
    mock_dynamic.status_code = 200
    mock_dynamic.json.return_value = dynamic_success_response

    mock_get.side_effect = [mock_static, mock_dynamic]

    venue_data = get_venue_data("test_venue")

    assert venue_data["venue_coordinates"] == [1, 2]
    assert venue_data["base_price_for_delivery"] == 190
    assert venue_data["order_minimum_no_surcharge"] == 1000
