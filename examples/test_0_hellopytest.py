#!/usr/bin/env python3
"""Hello pytest"""

def test_pass():
    assert (1, 2, 3) == (1, 2, 3)

def test_fail():
    assert (1, 2, 3) == (3, 2, 1)
