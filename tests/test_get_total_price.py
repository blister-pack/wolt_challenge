from fastapi import HTTPException
import pytest
from source.delivery_price_logic import get_total_price


def generate_error_dict(*error_keys):
    """
    Generates a dictionary of errors based on the provided keys.
    Each key corresponds to an error description.
    """
    error_descriptions = {
        "cart_value_error": "cart value can't be negative",
        "small_order_surcharge_error": "small order surcharge can't be negative",
        "delivery_fee_error": "delivery fee can't be negative",
    }
    return {key: error_descriptions[key] for key in error_keys}


# fmt: off
@pytest.mark.parametrize(
    "cart_value, small_order_surcharge, delivery_fee, expected_price, raises_exception, expected_errors",  # fmt:skip
    [
        (100, 100, 100, 300, False, None),
        (100, 0, 0, 100, False, None),
        (50, 100, 0, 150, False, None),
        (0, 50, 50, 100, False, None),
        (-100, 0, 0, None, True, generate_error_dict("cart_value_error")),
        (0, -100, 0, None, True, generate_error_dict("small_order_surcharge_error")),
        (0, 0, -100, None, True, generate_error_dict("delivery_fee_error")),
        (-100, -100, -100, None, True, generate_error_dict("cart_value_error", "small_order_surcharge_error", "delivery_fee_error")),
        (-100, -100, 0, None, True, generate_error_dict("cart_value_error", "small_order_surcharge_error")),
        (-100, 0, -100, None, True, generate_error_dict("cart_value_error","delivery_fee_error")),
        (0, -100, -100, None, True, generate_error_dict("small_order_surcharge_error", "delivery_fee_error")),
    ],
)
# fmt: on

def test_multiple_prices(cart_value, small_order_surcharge, delivery_fee, expected_price, raises_exception, expected_errors):  # fmt:skip
    if raises_exception:
        with pytest.raises(HTTPException) as exception_info:
            get_total_price(cart_value, small_order_surcharge, delivery_fee)
            assert exception_info.value.status_code == 400
            assert exception_info.value.detail == expected_errors
    else:
        assert (
            get_total_price(cart_value, small_order_surcharge, delivery_fee)
            == expected_price
        )
