from fastapi import FastAPI, HTTPException
import requests
import math
from delivery_price_logic import (
    get_delivery_fee,
    extract_venue_coordinates,
    get_distance,
    get_small_order_surcharge,
    get_total_price,
)
from venue_client import get_venue_data

app = FastAPI()


@app.get("/api/v1/delivery-order-price")
def delivery_order_price(*, venue_slug: str, cart_value: int, user_lat: float, user_lon: float):  # fmt:skip

    venue_data = get_venue_data(venue_slug)

    venue_coordinates = extract_venue_coordinates(venue_data["venue_coordinates"])

    distance = get_distance(
        venue_coordinates,
        (user_lat, user_lon),
    )

    delivery_fee = get_delivery_fee(
        venue_data["base_price_for_delivery"],
        distance,
        venue_data["distance_ranges_for_delivery"],
    )

    small_order_surcharge = get_small_order_surcharge(
        venue_data["order_minimum_no_surcharge"],
        cart_value,
    )

    total_price = get_total_price(cart_value, delivery_fee, small_order_surcharge)

    return {
        "total_price": total_price,
        "small_order_surcharge": small_order_surcharge,
        "cart_value": cart_value,
        "delivery": {
            "fee": delivery_fee,
            "distance": distance,
        },
    }
