"""Defines the service wide constants."""

import enum
import os

DEFAULT_LISTENING_PORT = 15959

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def load_secrets():
    """Load the secret environment variables."""
    fullpath = os.path.join(_CURRENT_DIR, "..", "..", ".env")
    if not os.path.isfile(fullpath):
        return
    with open(fullpath) as fin:
        for line in fin.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, value = line.split("=")
            os.environ[name] = value


def clear_secrets():
    """Removes the secrets environ values."""
    fullpath = os.path.join(_CURRENT_DIR, "..", "..", ".env")
    if not os.path.isfile(fullpath):
        return
    with open(fullpath) as fin:
        for line in fin.readlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            name, _ = line.split("=")
            if name in os.environ:
                del os.environ[name]


class DocType(enum.Enum):
    """Defines the supported docstring types."""

    FUNCTION = "FUNCTION"
    CLASS = "CLASS"
    GENERIC = "GENERIC"


def get_doc_type(txt):
    """Tries to guess the doc type of the passed in txt:

    :return: The doctype enumerator.
    :rtype: DocType

    :raises: ValueError
    """
    for line in txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("def"):
            return DocType.FUNCTION
        elif line.startswith("class"):
            return DocType.CLASS
        else:
            return DocType.GENERIC
        raise ValueError


def get_prefix_spaces(txt):
    """Gets the number of prefix spaces needed for the doc str.

    In the case that the passed in text is python code then in the
    case of a function, method or a class we need to know how many spaces
    consist the prefix of each line. This applies to cases where the function
    of the class is not defined starting from the first character of the line
    but instead it is indended (as happens in the case of a class method ).

    :param str txt: The text that can contain a fuction, method or class.

    :returns: The number of prefic spaces.
    :rtype: int
    """
    for line in txt.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("def"):
            return line.find("def")
        elif stripped.startswith("class"):
            return line.find("class")
        else:
            return 0
        raise ValueError
