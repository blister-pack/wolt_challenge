import pytest
from source.dopc import get_total_price


@pytest.mark.parametrize(
    "cart_value, small_order_surcharge, delivery_fee, expected_price",
    [
        (100, 100, 100, 300),
        (100, 0, 0, 100),
        (50, 100, 0, 150),
        (0, 50, 50, 100),
    ],
)


def test_multiple_prices(cart_value, small_order_surcharge, delivery_fee, expected_price):  # fmt:skip
    assert (
        get_total_price(cart_value, small_order_surcharge, delivery_fee)
        == expected_price
    )
