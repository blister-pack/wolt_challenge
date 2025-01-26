import pytest
from source.dopc import get_total_price


@pytest.mark.parametrize(
    "cart_value, small_order_surcharge, delivery_fee, expected_price, raises_exception",  # fmt:skip
    [
        (100, 100, 100, 300, False),
        (100, 0, 0, 100, False),
        (50, 100, 0, 150, False),
        (0, 50, 50, 100, False),
        (-100, 0, 0, None, True),
        (0, -100, 0, None, True),
        (0, 0, -100, None, True),
        (-100, -100, -100, None, True),
        (-100, -100, 0, None, True),
        (-100, 0, -100, None, True),
        (0, -100, -100, None, True),
    ],
)


def test_multiple_prices(cart_value, small_order_surcharge, delivery_fee, expected_price, raises_exception):  # fmt:skip
    if raises_exception:
        pass
    else:
        assert (
            get_total_price(cart_value, small_order_surcharge, delivery_fee)
            == expected_price
        )
