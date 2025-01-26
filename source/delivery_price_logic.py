from fastapi import HTTPException
import math

def get_distance(venue_coordinates: tuple, user_coordinates: tuple) -> int:
    """
    The function uses the Haversine formula to calculate the distance between
    two points using their coordinates (latitude and longitude).
    https://en.wikipedia.org/wiki/Haversine_formula
    Returns:
        int: The distance between the two points in meters.
    """

    if len(venue_coordinates) != 2:
        raise HTTPException(
            status_code=400, detail="Venue must have only 2 coordinates"
        )

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


def get_total_price(cart_value: int, small_order_surcharge: int, delivery_fee: int) ->int:  # fmt:skip
    """
    Calculate the total price of an order including cart value, small order surcharge,
    and delivery fee.
    Args:
        cart_value (int): The value of the items in the cart. Must be non-negative.
        small_order_surcharge (int): The surcharge applied to small orders. Must be
        non-negative.
        delivery_fee (int): The fee for delivering the order. Must be non-negative.
    Returns:
        int: The total price of the order.
    Raises:
        HTTPException: If any of the input values are negative, an HTTPException
        is raised with a status code of 400 and details of the errors.
    """

    errors = {}

    if cart_value < 0:
        errors["cart_value_error"] = "cart value can't be negative"

    if small_order_surcharge < 0:
        errors["small_order_surcharge_error"] = (
            "small order surcharge can't be negative"
        )

    if delivery_fee < 0:
        errors["delivery_fee_error"] = "delivery fee can't be negative"

    if errors:
        raise HTTPException(status_code=400, detail=errors)

    return cart_value + small_order_surcharge + delivery_fee


def extract_venue_coordinates(venue_coordinates_list: list) -> tuple:
    """
    Extracts and returns the latitude and longitude from a list of venue coordinates.
    Args:
        venue_coordinates_list (list): A list containing exactly two elements - latitude and longitude.
    Returns:
        tuple: A tuple containing the latitude and longitude.
    Raises:
        HTTPException: If the input list does not contain exactly two elements.
    """
    if len(venue_coordinates_list) != 2:
        raise HTTPException(
            status_code=400,
            detail="Can only take in 2 arguments for coordinates -> [latitude, longitude]",
        )

    venue_lat, venue_lon = venue_coordinates_list
    return (venue_lat, venue_lon)
