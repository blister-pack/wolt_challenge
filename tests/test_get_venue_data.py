import pytest
from source.venue_client import get_venue_data
from fastapi import HTTPException

"""
this is similar to the tests in instrumentation, but in this case we seek out to
test the functionality of the function without having it depend on an external API.
"""
