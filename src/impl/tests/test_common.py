"""Tests the common module."""

import pytest

import querycrafter.src.impl.common as common


def test_getting_function():
    """Tests retrieving a function."""
    txt = """


    def foo(i, j):
        return i * j

    """

    retrieved = common.get_doc_type(txt)
    assert common.DocType.FUNCTION == retrieved


def test_getting_class():
    """Tests retrieving a class."""
    txt = """

    class Junk:
        pass


    """

    retrieved = common.get_doc_type(txt)
    assert common.DocType.CLASS == retrieved


def test_invalid_element():
    """Test a text that is not a class of a function."""
    txt = """


    x

    """

    with pytest.raises(ValueError):
        common.get_doc_type(txt)