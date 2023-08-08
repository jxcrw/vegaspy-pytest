#!/usr/bin/env python3
"""Simple fixture demo"""

import pytest


@pytest.fixture()
def my_data():
    """Prep data for testing."""
    return 42


def test_init(my_data):
	"""Check that data was initialized."""
	assert my_data == 42


def test_addition(my_data):
    """Check that data can be used to do stuff."""
    my_data += 1
    assert my_data == 43
