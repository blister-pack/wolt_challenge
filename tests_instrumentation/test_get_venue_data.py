import pytest
from source.venue_client import get_venue_data
from fastapi import HTTPException


@pytest.mark.parametrize(
    "venue_slug, expected_data_dict",
    [
        (
            "home-assignment-venue-helsinki",
            {
                "venue_coordinates": [24.92813512, 60.17012143],
                "order_minimum_no_surcharge": 1000,
                "base_price_for_delivery": 190,
                "distance_ranges_for_delivery": [
                    {"min": 0, "max": 500, "a": 0, "b": 0, "flag": None},
                    {"min": 500, "max": 1000, "a": 100, "b": 0, "flag": None},
                    {"min": 1000, "max": 1500, "a": 200, "b": 0, "flag": None},
                    {"min": 1500, "max": 2000, "a": 200, "b": 1, "flag": None},
                    {"min": 2000, "max": 0, "a": 0, "b": 0, "flag": None},
                ],
            },
        ),
        (
            "home-assignment-venue-stockholm",
            {
                "venue_coordinates": [18.0314984, 59.3466978],
                "order_minimum_no_surcharge": 10000,
                "base_price_for_delivery": 900,
                "distance_ranges_for_delivery": [
                    {"min": 0, "max": 500, "a": 0, "b": 0, "flag": None},
                    {"min": 500, "max": 1000, "a": 1000, "b": 0, "flag": None},
                    {"min": 1000, "max": 1500, "a": 2000, "b": 0, "flag": None},
                    {"min": 1500, "max": 2000, "a": 2000, "b": 10, "flag": None},
                    {"min": 2000, "max": 0, "a": 0, "b": 0, "flag": None},
                ],
            },
        ),
        (
            "home-assignment-venue-berlin",
            {
                "venue_coordinates": [13.4536149, 52.5003197],
                "order_minimum_no_surcharge": 1000,
                "base_price_for_delivery": 190,
                "distance_ranges_for_delivery": [
                    {"min": 0, "max": 500, "a": 0, "b": 0, "flag": None},
                    {"min": 500, "max": 1000, "a": 100, "b": 0, "flag": None},
                    {"min": 1000, "max": 1500, "a": 200, "b": 0, "flag": None},
                    {"min": 1500, "max": 2000, "a": 200, "b": 1, "flag": None},
                    {"min": 2000, "max": 0, "a": 0, "b": 0, "flag": None},
                ],
            },
        ),
        (
            "home-assignment-venue-tokyo",
            {
                "venue_coordinates": [139.7115264, 35.6459122],
                "order_minimum_no_surcharge": 700,
                "base_price_for_delivery": 49,
                "distance_ranges_for_delivery": [
                    {"min": 0, "max": 500, "a": 0, "b": 0, "flag": None},
                    {"min": 500, "max": 1000, "a": 30, "b": 0, "flag": None},
                    {"min": 1000, "max": 1500, "a": 50, "b": 0, "flag": None},
                    {"min": 1500, "max": 2000, "a": 50, "b": 1, "flag": None},
                    {"min": 2000, "max": 0, "a": 0, "b": 0, "flag": None},
                ],
            },
        ),
    ],
)
def test_multiple_venue_slugs(venue_slug, expected_data_dict):
    assert get_venue_data(venue_slug) == expected_data_dict
