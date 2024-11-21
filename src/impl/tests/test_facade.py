"""Tests the facade module."""

import querycrafter.src.impl.common as common
import querycrafter.src.impl.facade as facade

DocType = common.DocType


def test_make_docstring_for_function():
    """Tests the make docstring for a function."""
    common.load_secrets()
    txt = """
    def add_numbers(i, j):
        return i + j
    """
    retrieved = facade.make_docstring(DocType.FUNCTION, txt)
    print(retrieved)
    common.clear_secrets()


def test_make_docstring_for_method():
    """Tests the make docstring for a class method."""
    common.load_secrets()
    txt = """
    def add_numbers(self, i, j):
        if i is None:
            raise ValueError
        return i + j
    """
    retrieved = facade.make_docstring(DocType.FUNCTION, txt)
    print(retrieved)
    common.clear_secrets()


def test_make_docstring_for_static_method():
    """Tests the make docstring for a static class method."""
    common.load_secrets()
    txt = """
    @classmethod
    def add_numbers(cls, i, j):
        if i is None:
            raise StaticValueError
        return i + j
    """
    retrieved = facade.make_docstring(DocType.FUNCTION, txt)
    print(retrieved)
    common.clear_secrets()


def test_make_docstring_for_class():
    """Tests the make docstring for a class."""
    common.load_secrets()
    txt = """
    class Person:
        name: None
        TITLES = ['mr.', 'mrs.']
        COUNTRY = "Where??"

        def __init__(self, name, age):
            self.name = name
            self.age = age
    """
    retrieved = facade.make_docstring(DocType.CLASS, txt)
    print(retrieved)
    common.clear_secrets()

