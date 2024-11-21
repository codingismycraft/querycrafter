"""Tests the _OpenAIChatBot."""

import os
import unittest

import ollama
import openai


import querycrafter.src.impl.chatbot as chatbot
import querycrafter.src.impl.common as common

# pylint: disable=protected-access
_OpenAIChatBot = chatbot._OpenAIChatBot
_OllamaChatBot = chatbot._OllamaChatBot


_QUERY = "What is the capital of France?"


class Test_OpenAIChatBot(unittest.TestCase):
    """Tests the _OpenAIChatBot class."""

    _MODEL_NAME = "gpt-4-turbo"

    def setUp(self):
        """Prepares an individual test to run."""
        common.clear_secrets()

    def test_invalid_model_name(self):
        """Tests using non supporting model name."""
        common.load_secrets()
        bot = _OpenAIChatBot("junk-model")
        with self.assertRaises(openai.NotFoundError):
            bot.run_query(_QUERY)

    def test_invalid_openai_key(self):
        """Tests invalid openai key."""
        os.environ["OPENAI_API_KEY"] = "junk"
        bot = _OpenAIChatBot(self._MODEL_NAME)
        with self.assertRaises(openai.AuthenticationError):
            bot.run_query(_QUERY)

    def test_successull_query(self):
        """Tests executing a query successfully."""
        common.load_secrets()
        bot = _OpenAIChatBot(self._MODEL_NAME)
        response = bot.run_query(_QUERY)
        self.assertIn("paris", response.lower())


class TestOllamaChatBot(unittest.TestCase):
    """Tests the  _OllamaChatBot class."""

    _MODEL_NAME = "llama3.2"

    def setUp(self):
        """Prepares an individual test to run."""
        common.clear_secrets()

    def test_invalid_model_name(self):
        """Tests using non supporting model name."""
        common.load_secrets()
        bot = _OllamaChatBot("junk-model")
        with self.assertRaises(ollama._types.ResponseError):
            bot.run_query(_QUERY)

    def test_successull_query(self):
        """Tests executing a query successfully."""
        common.load_secrets()
        bot = _OllamaChatBot(self._MODEL_NAME)
        response = bot.run_query(_QUERY)
        self.assertIn("paris", response.lower())
