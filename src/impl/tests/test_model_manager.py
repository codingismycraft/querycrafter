"""Tests the model_manager module."""

import pytest

import querycrafter.src.impl.model_manager as model_manager

ModelManager = model_manager.ModelManager


def test_get_provider():
    """Tests geting provider."""
    retrieved = ModelManager.get_provider()
    assert retrieved == ModelManager.DEFAULT_PROVIDER


def test_get_model_name():
    """Tests geting the model name."""
    retrieved = ModelManager.get_model_name()
    assert retrieved == ModelManager.DEFAULT_MODEL_NAME


def test_setting_active_model():
    """Tests setting the active model."""
    ModelManager.set_active_model("llama3:8b")

    retrieved = ModelManager.get_provider()
    assert retrieved == "ollama"

    retrieved = ModelManager.get_model_name()
    assert retrieved == "llama3:8b"

    ModelManager.set_active_model(ModelManager.DEFAULT_MODEL_NAME)


def test_setting_unsupported_active_model():
    """Tests setting unsupported active model."""
    with pytest.raises(ValueError):
        ModelManager.set_active_model("junk")
