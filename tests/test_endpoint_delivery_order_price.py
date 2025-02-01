from source.dopc import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_delivery_order_price():
    response = client.get("/api/v1/delivery-order-price")
    assert response.status_code == 200
