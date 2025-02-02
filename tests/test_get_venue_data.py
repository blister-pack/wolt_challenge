import pytest
from source.venue_client import get_venue_data
from fastapi import HTTPException
import unittest.mock as mock

"""
this is similar to the tests in instrumentation, but in this case we seek out to
test the functionality of the function without having it depend on an external API.
"""


def test_gvd_static_fail():
    pass


def test_gvd_dynamic_fail():
    pass


def test_gvd_static_and_dynamic_fail():
    pass


def test_gvd_success():
    pass
