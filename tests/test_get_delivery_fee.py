import pytest
from source.dopc import get_delivery_fee
from fastapi import HTTPException


@pytest.fixture
def base_price():
    return 190


@pytest.fixture
def distance_ranges():
    return [
        {"min": 0, "max": 500, "a": 0, "b": 0},
        {"min": 500, "max": 1000, "a": 100, "b": 0},
        {"min": 1000, "max": 1500, "a": 200, "b": 0},
        {"min": 1500, "max": 2000, "a": 200, "b": 1},
        {"min": 2000, "max": 0, "a": 0, "b": 0},
    ]


@pytest.mark.parametrize(
    "distance, expected_fee",
    [
        (200, 190),
        (700, 290),
        (1200, 390),
        (1700, 560),
    ],
    ids=[
        "Test for first delivery range",
        "Test for 2nd delivery range",
        "Test for 3rd delivery range",
        "Test for 4th delivery range",
    ],
)
def test_multiple_distance_ranges(base_price, distance_ranges, distance, expected_fee):  # fmt:skip
    assert get_delivery_fee(base_price, distance, distance_ranges) == expected_fee


@pytest.fixture
def out_of_bounds_distance():
    return 2200


def test_raises_exception(out_of_bounds_distance, distance_ranges, base_price):
    with pytest.raises(HTTPException) as exception_info:
        get_delivery_fee(base_price, out_of_bounds_distance, distance_ranges)
    assert exception_info.value.status_code == 400
    assert exception_info.value.detail == "Distance exceeds maximum permissible limit."
