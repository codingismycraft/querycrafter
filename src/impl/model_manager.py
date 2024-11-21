"""Defines the mechanism to handle the selected LLM model."""


class ModelManager:
    """Manages the selected model.

    :cvar str model_name: The model name to use.
    :cvar str _provider: The LLM provider to use.

    :cvar list [dict] _SUPPORTED_MODELS: The supported models.

    :cvar str DEFAULT_PROVIDER: The defautl LLM provider to use.
    :cvar str DEFAULT_MODEL_NAME: The default model to use.
    """

    DEFAULT_PROVIDER = "openai"
    DEFAULT_MODEL_NAME = "gpt-4-turbo"

    _provider = DEFAULT_PROVIDER
    _model_name = DEFAULT_MODEL_NAME

    _SUPPORTED_MODELS = [
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
            "model_name": "gpt-4-turbo"
        },
    ]

    @classmethod
    def set_active_model(cls, model_name):
        """Sets the active model.

        :param str model_name: The model name to use.

        :raises ValueError
        """
        for model_info in cls._SUPPORTED_MODELS:
            if model_info["model_name"] == model_name:
                provider = model_info.get("provider")
                if not provider:
                    raise ValueError(f"Invalid provider for {model_name}")
                cls._model_name = model_name
                cls._provider = provider
                return
        raise ValueError(f"Unsupported model {model_name}")

    @classmethod
    def get_provider(cls):
        """Returns the active LLM provider.

        :returns: The active LLM provider.
        :rtype: str
        """
        return cls._provider

    @classmethod
    def get_model_name(cls):
        """Returns the active LLM model_name.

        :returns: The active LLM model_name.
        :rtype: str
        """
        return cls._model_name
