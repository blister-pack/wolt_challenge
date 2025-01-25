from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import math

app = FastAPI()


@app.get("/api/v1/delivery-order-price")
def delivery_order_price(*, venue_slug: str, cart_value: int, user_lat: float, user_lon: float):  # fmt:skip

    venue_data = get_venue_data(venue_slug)

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


def get_distance(user_coordinates: list, venue_coordinates: list) -> int:
    """
    The function uses the Haversine formula to calculate the distance between
    two points using their coordinates (latitude and longitude).
    https://en.wikipedia.org/wiki/Haversine_formula
    Returns:
        int: The distance between the two points in meters.
    """

    user_lat, user_lon = user_coordinates
    venue_lat, venue_lon = venue_coordinates

    EARTH_RADIUS = 6372.8 * (10**3)  # earth radius in meters

    delta_lat = math.radians(venue_lat - user_lat)
    delta_lon = math.radians(venue_lon - user_lon)
    user_lat = math.radians(user_lat)
    venue_lat = math.radians(venue_lat)

    aux = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(user_lat) * math.cos(venue_lat) * math.sin(delta_lon / 2) ** 2
    )

    return round(EARTH_RADIUS * 2 * math.asin(math.sqrt(aux)))


def get_venue_data(venue_slug: str) -> dict:
    """
    Fetches and returns venue data from the Wolt API.
    Args:
        venue_slug (str): The unique identifier for the venue.
    Returns:
        dict: A dictionary containing the venue's coordinates, order minimum
        to avoid surcharge, base price for delivery, and distance ranges for delivery.
    Raises:
        HTTPException: If there is an issue with the HTTP request.
        KeyError: If the expected keys are not found in the API response.
    """
    # TODO make function raise error if response != 200
    static_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static"
    dynamic_url = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic"

    errors = {}

    static_response = requests.get(static_url)
    dynamic_response = requests.get(dynamic_url)

    if static_response.status_code != 200:
        errors["static_data_error"] = (
            f"Static data request failed with status code {static_response.status_code}"
        )
    else:
        static_data = static_response.json()

    if dynamic_response.status_code != 200:
        errors["dynamic_data_error"] = (
            f"Dynamic data request failed with status code {dynamic_response.status_code}"
        )
    else:
        dynamic_data = dynamic_response.json()

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    try:
        venue_coordinates = static_data["venue_raw"]["location"]["coordinates"]  # fmt:skip
        dynamic_data_delivery_specs = dynamic_data["venue_raw"]["delivery_specs"]
        order_minimum_no_surcharge = dynamic_data_delivery_specs["order_minimum_no_surcharge"]  # fmt:skip
        base_price_for_delivery = dynamic_data_delivery_specs["delivery_pricing"]["base_price"]  # fmt:skip
        distance_ranges_for_delivery = dynamic_data_delivery_specs["delivery_pricing"]["distance_ranges"]  # fmt:skip
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing key in API response {e}")

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
    Raises:
        HTTPException: If the distance exceeds the maximum permissible distance.
    """
    for distance_range in distance_ranges:
        if distance <= distance_range["max"]:
            venue_a = distance_range["a"]
            venue_b = distance_range["b"]
            break
        elif distance_range["max"] == 0:
            raise HTTPException(
                status_code=400, detail="Distance exceeds maximum permissible limit."
            )
    fee = base_price + venue_a + round(venue_b * distance / 10)
    return fee


def get_small_order_surcharge(order_minimum_no_surcharge: int, cart_value: int):
    small_order_surcharge = order_minimum_no_surcharge - cart_value
    return max(small_order_surcharge, 0)


def get_total_price(cart_value: int, small_order_surcharge: int, delivery_fee: int):
    errors = {}

    if cart_value < 0:
        errors["cart_value_error"] = "cart value can't be negative"

    if small_order_surcharge < 0:
        errors["small_order_surcharge_error"] = (
            "small order surcharge can't be negative"
        )

    if delivery_fee < 0:
        errors["delivery_fee"] = "delivery fee can't be negative"

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    return cart_value + small_order_surcharge + delivery_fee


# TODO change get_delivery_fee tests to accommodate possible error raising
# TODO make logic functions throw errors if results don't make sense
# TODO before any request check that the response is 200
# TODO get Fonseca to proof check my math
# TODO correct Haversine
# TODO test get_venue_data (with mocking)
# TODO test endpoint
# TODO instructions on how to install and run
# TODO complete functions with expected output and type hints
# TODO implement clean architecture design
# DONE endpoint should return error 400 if something is not possible (is there a technicality here?)
# DONE document get_venue_data
# DONE get_fee should take ranges into consideration
# DONE remember small order surcharge can never be negative
# DONE enable Github for version control (not public)
# DONE one of the coordinates isn't supposed to be processed as a list (in endpoint)
# DONE correct endpoint Path
# DONE document tests (explain what each test is testing like for which range)
