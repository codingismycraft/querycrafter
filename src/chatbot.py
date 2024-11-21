"""Exposes a chatbot capable to respond to a query."""

import ollama
import openai

import querycrafter.constants as constants


def run_query(query):
    """Executes the passed in query.

    :param str query: The query to execute.

    :returns: The response to the query.
    :rtype: str.

    :raises: ValueError
    :raises: openai.NotFoundError
    :raises: openai.AuthenticationError
    """
    return _ChatBotWrapper.run_query(query)


class _ChatBotWrapper:
    """Generic Chat Bot."""

    _chat_bot = None

    @classmethod
    def initialize(cls):
        """Initializes the chatbot.

        :raises: ValueError
        """
        provider = None
        model_name = None
        for mi in constants.SUPPORTED_MODELS:
            if mi.get("is_active"):
                if provider or model_name:
                    raise ValueError("Cannot define multiple active models.")
                provider = mi["provider"]
                model_name = mi["model_name"]
        if not model_name or not provider:
            raise ValueError("You must select an active model in constants.")

        if provider == "ollama""":
            cls._chat_bot = _OllamaChatBot(model_name)
        elif provider == "openai":
            cls._chat_bot = _OpenAIChatBot(model_name)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    @classmethod
    def run_query(cls, query):
        """Executes the passed in query.

        :param str query: The query to execute.

        :returns: The response to the query.
        :rtype: str.
        """
        if not cls._chat_bot:
            cls.initialize()
        assert cls._chat_bot, "ChatBot is not initialized."
        return cls._chat_bot.run_query(query)


class _OllamaChatBot:
    """Chatbot using the Ollama API to generate responses.

    :ivar ollama.Client _client: The ollama client object.
    :ivar str _model_name: The Ollama model to use..
    """
    _client = None
    _model_name = None

    def __init__(self, model_name):
        """Initializer.

        :param str model_name: The name of the model.
        """
        self._model_name = model_name
        self._client = ollama.Client()

    def run_query(self, query):
        """Executes the passed in query.

        :param str query: The query to execute.

        :returns: The response to the query.
        :rtype: str.
        """
        response = self._client.generate(
            model=self._model_name,
            prompt=query
        )
        return response['response']


class _OpenAIChatBot:
    """Manages the LLM session to get a RAG response.

    :ivar OpenAI _openai_client: The OpenAI client to use.
    :ivar str _model_name: The name of the model to use.
    """
    _DEFAULT_TEMPERATURE = 0.4
    _DEFAULT_MAX_TOKENS = 2000

    _openai_client = None
    _model_name = None

    def __init__(self, model_name):
        """Initializer.

        Assumes that the existence of the env variable OPENAI_API_KEY.

        :param str model_name: The name of the model.
        """
        self._model_name = model_name
        self._openai_client = openai.OpenAI()

    def run_query(self, query):
        """Executes a query getting a RAG response.

        :param str query: The query to execute.

        :returns: The response to the query.
        :rtype: str.

        :raises: openai.NotFoundError
        :raises: openai.AuthenticationError
        """
        temperature = self._DEFAULT_TEMPERATURE
        max_tokens = self._DEFAULT_MAX_TOKENS

        response = self._openai_client.chat.completions.create(
            model=self._model_name,
            messages=[
                {"role": "user", "content": query},
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        response = response.choices[0].message.content

        return response
