"""Defines the service wide constants."""

import os

LISTENING_PORT = 15959

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

SUPPORTED_MODELS = [
    {
        "provider": "ollama",
        "model_name": "codellama:7b",
    },
    {
        "provider": "ollama",
        "model_name": "llama3:8b",
    },
    {
        "provider": "openai",
        "model_name": "gpt-3.5-turbo"
    },
    {
        "provider": "openai",
        "model_name": "gpt-4-turbo",
        "is_active": True
    },
]


def load_secrets():
    """Load the secret environment variables."""
    fullpath = os.path.join(_CURRENT_DIR, ".env")
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
    fullpath = os.path.join(_CURRENT_DIR, ".env")
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
