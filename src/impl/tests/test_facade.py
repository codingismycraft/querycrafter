"""Tests the facade module."""

import querycrafter.src.impl.common as common
import querycrafter.src.impl.facade as facade

DocType = common.DocType


def inject_doc_str(source_code, docstr, linenum):
    """Injects the docstr to the source after the linenum.

    :param str source_code: The souce code to inject the docstr.
    :param str docstr: The docstr to inject.
    :param int linenum: The linenum where to inject the docstr.

    :returns: The source_code containing the docstr.
    :rtype: str
    """
    txt1 = ""
    new_line_count = 0
    for index, c in enumerate(source_code):
        if c == '\n':
            new_line_count += 1
        txt1 += c
        if new_line_count == linenum:
            txt1 += docstr
            txt1 += source_code[index:]
            break
    return txt1


def test_make_docstring_for_function():
    """Tests the make docstring for a function."""
    common.load_secrets()
    txt = """
    def add_numbers(i, j):
        return i + j
    """
    retrieved = facade.make_docstring(DocType.FUNCTION, txt)
    print(retrieved)
    txt1 = inject_doc_str(txt, retrieved, 2)
    print(txt1)
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
    txt1 = inject_doc_str(txt, retrieved, 3)
    print(txt1)
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
    txt1 = inject_doc_str(txt, retrieved, 2)
    print(txt1)
    common.clear_secrets()


def test_generic_query():
    """Tests a generic query."""
    common.load_secrets()
    txt = """What is the capital of France?"""
    retrieved = facade.make_docstring(DocType.GENERIC, txt)
    assert "paris" in retrieved.lower()
    common.clear_secrets()
