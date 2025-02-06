from urllib import response
import pytest
from source.delivery_price_logic import get_delivery_fee
from source.dopc import app
from fastapi.testclient import TestClient
import unittest.mock as mock
from fastapi import HTTPException
from source.venue_client import get_venue_data
import contextlib

client = TestClient(app)

mock_venue_data = {
    "venue_coordinates": [1, 2],
    "order_minimum_no_surcharge": 100,
    "base_price_for_delivery": 299,
    "distance_ranges_for_delivery": [
        {"min": 0, "max": 1000},
        {"min": 1000, "max": 2000},
        {"min": 2000, "max": 0},
    ],
}


def mock_get_venue_data(venue_slug):
    return mock_venue_data


def mock_get_distance(venue_coords, user_coords):
    return 500


def mock_get_delivery_fee(base_price, distance, distance_ranges):
    return 200


def mock_extr_venue_coordinates(venue_coordinates_list):
    return (1, 2)


def mock_get_small_order_surcharge(order_minimum_no_surcharge, cart_value):
    return 300


def mock_get_total_price(cart_value, small_order_surcharge, delivery_fee):
    return 1000


@contextlib.contextmanager
def mock_dependencies(
    mock_total_price=True,
    mock_small_order_surcharge=True,
    mock_venue_coordinates=True,
    mock_delivery_fee=True,
    mock_distance=True,
    mock_venue_data=True,
):
    used_mocks = []

    if mock_get_total_price:
        used_mocks.append(
            mock.patch("source.dopc.get_total_price", side_effect=mock_get_total_price)
        )

    if mock_small_order_surcharge:
        used_mocks.append(
            mock.patch(
                "source.dopc.get_small_order_surcharge",
                side_effect=mock_get_small_order_surcharge,
            )
        )

    if mock_venue_coordinates:
        used_mocks.append(
            mock.patch(
                "source.dopc.extract_venue_coordinates",
                side_effect=mock_extr_venue_coordinates,
            )
        )

    if mock_delivery_fee:
        used_mocks.append(
            mock.patch(
                "source.dopc.get_delivery_fee", side_effect=mock_get_delivery_fee
            )
        )

    if mock_distance:
        used_mocks.append(
            mock.patch("source.dopc.get_distance", side_effect=mock_get_distance)
        )

    if mock_venue_data:
        used_mocks.append(
            mock.patch("source.dopc.get_venue_data", side_effect=mock_get_venue_data)
        )

    with contextlib.ExitStack() as stack:
        for m in used_mocks:
            stack.enter_context(m)
        yield used_mocks


def test_dopc_success_context():
    with mock_dependencies():
        response = client.get(
            "/api/v1/delivery-order-price",
            params={
                "venue_slug": "test_venue",
                "cart_value": 1500,
                "user_lat": 3,
                "user_lon": 4,
            },
        )
    assert response.status_code == 200
    assert response.json() == {
        "total_price": 1000,
        "small_order_surcharge": 300,
        "cart_value": 1500,
        "delivery": {
            "fee": 200,
            "distance": 500,
        },
    }

    # ----- SOME USEFUL COMMANDS -----
    # mock_get_venue_data.assert_called_once_with("test_venue")
    # print("Error detail: ", json_response.get("detail"))
    # print("Full JSON: ", json_response)
    # print("Mock venue data returned:", mock_get_venue_data("test_venue"))
    # ---------------------------------


@mock.patch("source.dopc.get_total_price", side_effect=mock_get_total_price)
@mock.patch(
    "source.dopc.get_small_order_surcharge", side_effect=mock_get_small_order_surcharge
)
@mock.patch(
    "source.dopc.extract_venue_coordinates", side_effect=mock_extr_venue_coordinates
)
@mock.patch("source.dopc.get_distance")
@mock.patch("source.dopc.get_venue_data", side_effect=mock_get_venue_data)
def test_dopc_range_2big(
    mock_get_venue_data,
    mock_get_distance,
    mock_extract_venue_coordinates,
    mock_get_small_order_surcharge,
    mock_get_total_price,
):
    mock_get_distance.return_value = 3000  # out of bounds

    response = client.get(
        "/api/v1/delivery-order-price",
        params={
            "venue_slug": "test_venue",
            "cart_value": 1500,
            "user_lat": 3,
            "user_lon": 4,
        },
    )

    assert response.status_code == 400
    json_response = response.json()
    assert "Distance exceeds maximum permissible limit." == json_response["detail"]


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
