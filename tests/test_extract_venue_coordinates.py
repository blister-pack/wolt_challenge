from fastapi import HTTPException
from source.dopc import extract_venue_coordinates
import pytest


@pytest.mark.parametrize(
    "coordinate_list, expected_return, raises_exception",
    [
        ([12.123532, 56.156323], (12.123532, 56.156323), False),
        ([12.123456, 45.123456, 78.123456], None, True),
        ([12.123456], None, True),
        ([], None, True),
    ],
)
def test_multiple_coordinate_lists(
    coordinate_list, expected_return, raises_exception
):
    if raises_exception:
        with pytest.raises(HTTPException) as exception_info:
            extract_venue_coordinates(coordinate_list)
        assert exception_info.value.status_code == 400
        assert exception_info.value.detail == "Can only take in 2 arguments for coordinates -> [latitude, longitude]"  # fmt:skip
    else:
        assert extract_venue_coordinates(coordinate_list) == expected_return
