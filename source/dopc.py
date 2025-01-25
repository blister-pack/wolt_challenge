from fastapi import FastAPI
from pydantic import BaseModel
import requests
import math

app = FastAPI()

venues = [
    "home-assignment-venue-helsinki",
    "home-assignment-venue-stockholm",
    "home-assignment-venue-berlin",
    "home-assignment-venue-tokyo",
]


@app.get("/api/v1/delivery-order-price")
def delivery_order_price(*, venue_slug: str, cart_value: int, user_lat: float, user_lon: float):  # fmt:skip
    match_found = False
    for venue_name in venues:
        if venue_slug == venue_name:
            venue_data = get_venue_data(venue_slug)
            match_found = True
    if not match_found:
        return {"Error": "No match for queried venue"}
    # TODO check if it works with an else instead of match_found

    distance = get_distance(
        venue_data["venue_coordinates"],
        [user_lat, user_lon],
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


def get_distance(user_coordinates: list, venue_coordinates: list):
    """
    The function uses the Haversine formula to calculate the distance between
    two points using their coordinates (latitude and longitude).
    Returns:
        float: The distance between the two points in meters.
    """

    user_lat, user_lon = user_coordinates
    venue_lat, venue_lon = venue_coordinates

    EARTH_RADIUS = 6371 * (10**3)  # earth radius in meters

    user_lat_radians = math.radians(user_lat)
    venue_lat_radians = math.radians(venue_lat)
    delta_lat = venue_lat_radians - user_lat_radians
    delta_lon = math.radians(venue_lon - user_lon)

    aux = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(user_lat) * math.cos(venue_lat) * math.sin(delta_lon / 2) ** 2
    )

    return EARTH_RADIUS * 2 * math.asin(math.sqrt(aux))


def get_venue_data(venue_slug: str):
    venue_slug = venue_slug.split("-")[-1]
    static_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-{venue_slug}/static"
    dynamic_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/home-assignment-venue-{venue_slug}/dynamic"

    venue_coordinates = requests.get(static_url).json()["venue_raw"]["location"]["coordinates"]  # fmt:skip
    dynamic_data = requests.get(dynamic_url).json()["venue_raw"]["delivery_specs"]
    order_minimum_no_surcharge = dynamic_data["order_minimum_no_surcharge"]  # fmt:skip
    base_price_for_delivery = dynamic_data["delivery_pricing"]["base_price"]  # fmt:skip
    distance_ranges_for_delivery = dynamic_data["delivery_pricing"]["distance_ranges"]  # fmt:skip

    return {
        "venue_coordinates": venue_coordinates,
        "order_minimum_no_surcharge": order_minimum_no_surcharge,
        "base_price_for_delivery": base_price_for_delivery,
        "distance_ranges_for_delivery": distance_ranges_for_delivery,
    }


def get_delivery_fee(base_price, distance, distance_ranges):
    """
    The function calculates the total fee for a delivery. It takes into
    consideration the different delivery ranges, which modify the calculation.
    Using the passed in distance, it determines which distance range should be
    used and extracts a and b variables.
    Returns:
        int: The total cost of the delivery in the lowest denomination of
        the local currency.
    """
    for distance_range in distance_ranges:
        if distance <= distance_range["max"]:
            venue_a = distance_range["a"]
            venue_b = distance_range["b"]
            break
        elif distance_range["max"] == 0:
            return {"Error 400": "Distance exceeds maximum allowed"}
    fee = base_price + venue_a + round(venue_b * distance / 10)
    return fee


def get_small_order_surcharge(order_minimum_no_surcharge: int, cart_value: int):
    small_order_surcharge = order_minimum_no_surcharge - cart_value
    if small_order_surcharge < 0:
        return 0
    return small_order_surcharge


def get_total_price(cart_value: int, small_order_surcharge: int, delivery_fee: int):
    return cart_value + small_order_surcharge + delivery_fee


# TODO make logic functions throw errors if results don't make sense
# TODO endpoint should return error 400 if something is not possible (is there a technicality here?)
# TODO before any request check that the response is 200
# TODO get Fonseca to proof check my math
# TODO correct Haversine
# TODO document get_venue_data
# TODO test endpoint
# TODO instructions on how to install and run
# TODO complete functions with expected output and type hints
# DONE get_fee should take ranges into consideration
# DONE remember small order surcharge can never be negative
# DONE enable Github for version control (not public)
# DONE one of the coordinates isn't supposed to be processed as a list (in endpoint)
# DONE correct endpoint Path
# DONE document tests (explain what each test is testing like for which range)
