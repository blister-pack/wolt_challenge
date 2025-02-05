from source.delivery_price_logic import get_delivery_fee
from source.dopc import app
from fastapi.testclient import TestClient
import unittest.mock as mock
from fastapi import HTTPException
from source.venue_client import get_venue_data

client = TestClient(app)

mock_venue_data = {
    "venue_coordinates": [1, 2],
    "order_minimum_no_surcharge": 100,
    "base_price_for_delivery": 299,
    "distance_ranges_for_delivery": [
        {"min": 0, "max": 1000},
        {"min": 1000, "max": 2000},
    ],
}


def mock_get_venue_data(venue_slug):
    return mock_venue_data


@mock.patch("source.dopc.get_total_price")
@mock.patch("source.dopc.get_small_order_surcharge")
@mock.patch("source.dopc.extract_venue_coordinates")
@mock.patch("source.dopc.get_delivery_fee")
@mock.patch("source.dopc.get_distance")
@mock.patch(
    target="source.dopc.get_venue_data",
    side_effect=mock_get_venue_data,
)
def test_dopc_success(
    mock_get_venue_data,
    mock_get_distance,
    mock_get_delivery_fee,
    mock_extract_venue_coordinates,
    mock_get_small_order_surcharge,
    mock_get_total_price,
):
    mock_get_delivery_fee.return_value = 100
    mock_get_distance.return_value = 500
    mock_get_delivery_fee.return_value = 200
    mock_extract_venue_coordinates.return_value = (1, 2)
    mock_get_small_order_surcharge.return_value = 300
    mock_get_total_price.return_value = 1000

    response = client.get(
        "/api/v1/delivery-order-price",
        params={
            "venue_slug": "test_venue",
            "cart_value": 1500,
            "user_lat": 3,
            "user_lon": 4,
        },
    )
    mock_get_venue_data.assert_called_once_with("test_venue")
    assert response.status_code == 200
    json_response = response.json()
    print("Error detail: ", json_response.get("detail"))
    print("Full JSON: ", json_response)
    print("Mock venue data returned:", mock_get_venue_data("test_venue"))

    assert json_response["delivery"]["distance"] == 500


def test_dopc_range_2big():
    pass


# def test_dopc_no_args():
#     response = client.get("/api/v1/delivery-order-price")
#     assert response.status_code == 422


# def test_dopc_bad_slug():
#     response = client.get(
#         "/api/v1/delivery-order-price?venue_slug=nope&cart_value=0&user_lat=1&user_lon=1"
#     )
#     assert response.status_code == 400


# def test_dopc_good_args():
#     response = client.get(
#         "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=199&user_lat=24.93913512&user_lon=60.18112143"
#     )
#     assert response.status_code == 200
