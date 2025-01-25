import pytest
from source.dopc import get_delivery_fee


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
        (2200, {"Error 400": "Distance exceeds maximum allowed"}),
    ],
    ids=[
        "Test for first delivery range",
        "Test for 2nd delivery range",
        "Test for 3rd delivery range",
        "Test for 4th delivery range",
        "Test for out of bounds delivery (error expected)",
    ],
)
def test_multiple_distance_ranges(base_price, distance_ranges, distance, expected_fee):  # fmt:skip
    assert get_delivery_fee(base_price, distance, distance_ranges) == expected_fee
