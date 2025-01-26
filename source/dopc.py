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


# TODO make dopc.py work by just running it - if __name__ == __main__
# TODO change get_delivery_fee tests to accommodate possible error raising
# TODO test get_venue_data (with mocking)
# TODO test endpoint
# TODO instructions on how to install and run
# TODO complete functions with expected output and type hints
# DONE implement clean architecture design
# DONE before any request check that the response is 200
# DONE get Fonseca to proof check my math
# DONE correct Haversine
# DONE make logic functions throw errors if results don't make sense
# DONE endpoint should return error 400 if something is not possible (is there a technicality here?)
# DONE document get_venue_data
# DONE get_fee should take ranges into consideration
# DONE remember small order surcharge can never be negative
# DONE enable Github for version control (not public)
# DONE one of the coordinates isn't supposed to be processed as a list (in endpoint)
# DONE correct endpoint Path
# DONE document tests (explain what each test is testing like for which range)
