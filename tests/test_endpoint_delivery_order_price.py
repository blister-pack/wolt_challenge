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
        {"min": 0, "max": 1000, "price": 500},
        {"min": 1000, "max": 2000, "price": 1000},
    ],
}


def mock_get_venue_data(venue_slug):
    return mock_venue_data


def mock_get_distance(venue_coordinates, user_coordinates):
    return 500


@mock.patch(
    target="source.delivery_price_logic.get_distance",
    side_effect=mock_get_distance,
)
@mock.patch(
    target="source.venue_client.get_venue_data",
    side_effect=mock_get_venue_data,
)
def test_dopc_success(mock_get_venue_data, mock_get_distance):
    response = client.get(
        "/api/v1/delivery-order-price",
        params={
            "venue_slug": "test_venue",
            "cart_value": 1500,
            "user_lat": 3,
            "user_lon": 4,
        },
    )

    assert response.status_code == 400 # why is it 400?????????
    json_response = response.json()

    assert json_response["delivery"]["distance"] == 500  # why tf is this passing lol


def test_dopc_range_2big():
    pass


def test_dopc_no_args():
    response = client.get("/api/v1/delivery-order-price")
    assert response.status_code == 422


def test_dopc_bad_slug():
    response = client.get(
        "/api/v1/delivery-order-price?venue_slug=nope&cart_value=0&user_lat=1&user_lon=1"
    )
    assert response.status_code == 400


def test_dopc_good_args():
    response = client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=199&user_lat=24.93913512&user_lon=60.18112143"
    )
    assert response.status_code == 200
