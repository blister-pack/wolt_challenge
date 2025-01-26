from source.dopc import extract_venue_coordinates
import pytest


@pytest.mark.parametrize(
    "coordinate_list, expected_return",
    [
        ([12.123532, 56.156323], (12.123532, 56.156323)),
        ([12.123456, 45.123456, 78.123456])
    ],
)
def test_multiple_coordinate_lists():
    pass
