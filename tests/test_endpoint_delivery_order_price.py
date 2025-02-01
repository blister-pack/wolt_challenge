from source.dopc import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_dopc_no_args():
    response = client.get("/api/v1/delivery-order-price")
    assert response.status_code == 422


def test_dopc_bad_args():
    response = client.get(
        "/api/v1/delivery-order-price?venue_slug=nope&cart_value=0&user_lat=1&user_lon=1"
    )
    assert response.status_code == 400


def test_dopc_good_args():
    response = client.get(
        "/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=199&user_lat=24.93913512&user_lon=60.18112143"
    )
    assert response.status_code == 200
