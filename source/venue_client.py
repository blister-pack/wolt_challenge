from fastapi import HTTPException
import requests


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
