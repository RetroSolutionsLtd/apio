"""
Tests of scons_util.py
"""

import os
import pytest
from apio.utils.util import plurality, list_plurality, is_debug, nameof

# pylint: disable=fixme
# TODO: Add more tests.


def test_pluraliry():
    """Tests the plurality() function."""
    # -- Test for ints 1, 2, 3
    assert plurality(1, "file") == "1 file"
    assert plurality(2, "file") == "2 files"
    assert plurality(3, "file") == "3 files"

    # -- Test for lengths 1, 2, 3.
    assert plurality(["aa"], "file") == "1 file"
    assert plurality(["aa", "bb"], "file") == "2 files"
    assert plurality(["aa", "bb", "cc"], "file") == "3 files"


def test_list_pluraliry():
    """Tests the list_plurality() function."""

    # -- Test for lengths 1, 2, and 3.
    assert list_plurality(["aa"], "or") == "aa"
    assert list_plurality(["aa", "bb"], "and") == "aa and bb"
    assert list_plurality(["aa", "bb", "cc"], "or") == "aa, bb, or cc"

    # -- An empty list should trhow an assert exception.
    with pytest.raises(AssertionError):
        list_plurality([], "or")


def test_is_debug():
    """Tests the is_debug() function."""

    # -- Assuming APIO_DEBUG is not defined.
    assert not is_debug()

    # -- Enter debug mode.
    os.environ["APIO_DEBUG"] = ""
    assert is_debug()

    # -- Exit debug mode
    os.environ.pop("APIO_DEBUG")
    assert not is_debug()


def test_nameof():
    """Tests the nameof() function."""

    def nameof_tester(a, _b, _c):
        """Returns the names of a and _c."""
        return nameof(a, _c)

    # -- Calling foor should return the names of its a and _c args.
    assert nameof_tester(1, 2, 3) == ["a", "_c"]
