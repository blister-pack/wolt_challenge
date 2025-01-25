import pytest
from source.dopc import get_small_order_surcharge


@pytest.fixture
def minimum_order_no_surcharge_value():
    return 1000


@pytest.mark.parametrize(
    "cart_value, expected_surcharge",
    [
        (200, 800),
        (400, 600),
        (800, 200),
        (1000, 0),
        (1200, 0),
    ],
)
def test_multiple_surcharge_values(minimum_order_no_surcharge_value, cart_value, expected_surcharge):  # fmt:skip
    assert (
        get_small_order_surcharge(minimum_order_no_surcharge_value, cart_value)
        == expected_surcharge
    )
