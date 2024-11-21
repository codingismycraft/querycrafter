"""Defines the service wide constants."""

import os

LISTENING_PORT = 15959

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def load_secrets():
    """Load the secret environment variables."""
    fullpath = os.path.join(_CURRENT_DIR, "..", ".env")
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
    fullpath = os.path.join(_CURRENT_DIR, "..", ".env")
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
