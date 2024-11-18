"""Tests the prompts and the generated responses."""

import json
import os

import querycrafter.chatbot as chatbot
import querycrafter.constants as constants
import querycrafter.prompts as prompts

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_doc_string_for_class():
    """Tests creating doc string for a class."""
    constants.load_secrets()
    txt = """
    class Person:
        name: None
        TITLES = ['mr.', 'mrs.']

        def __init__(self, name, age):
            self.name = name
            self.age = age
    """

    prompt = prompts.MAKE_DOC_STRING_FOR_CLASS + txt
    response = chatbot.run_query(prompt)
    retrieved = json.loads(response)
    assert isinstance(retrieved, dict)
    assert len(retrieved) == 4
    assert "summary" in retrieved
    assert "ivars" in retrieved
    assert "cvars" in retrieved


def test_doc_string_for_function():
    """Tests creating doc string for a function."""
    constants.load_secrets()

    txt = """
    def get_max_profit(prices):
        m = 0
        index = 0
        left = left_side_max_deltas(prices)
        right = right_side_max_deltas(prices)
        while index < len(prices):
            m = max(m, left[index] + right[index])
            index += 1
        return m
    """

    prompt = prompts.MAKE_DOC_STRING_FOR_FUNCTION + txt
    response = chatbot.run_query(prompt)
    print(response)
    retrieved = json.loads(response)

    assert isinstance(retrieved, dict)
    assert len(retrieved) == 4
    assert "summary" in retrieved
    assert "arguments" in retrieved
    assert "return" in retrieved

    return_value = retrieved.get("return")
    assert isinstance(return_value, dict)
    assert len(return_value) == 2
    assert "return_type" in return_value
    assert "desc" in return_value


def test_doc_string_for_method_1():
    """Tests creating doc string for a class method."""
    constants.load_secrets()
    txt = """
    def say_hello(self, crowd, time):
        if is_morning(time):
            print(crowd, "goodmorning")
        else:
            print(crowd, "hello")
    """
    prompt = prompts.MAKE_DOC_STRING_FOR_FUNCTION + txt
    response = chatbot.run_query(prompt)
    print(response)
    retrieved = json.loads(response)

    assert isinstance(retrieved, dict)
    assert len(retrieved) == 3
    assert "summary" in retrieved
    assert "arguments" in retrieved
    assert "prefixed_spaces" in retrieved

    args = retrieved.get("arguments")
    assert isinstance(args, list)
    assert len(args) == 2


def test_doc_string_for_method_2():
    """Tests creating doc string for a class method no args."""
    constants.load_secrets()
    txt = """
    def say_hello(self):
        return "OK"
    """
    prompt = prompts.MAKE_DOC_STRING_FOR_FUNCTION + txt
    response = chatbot.run_query(prompt)
    retrieved = json.loads(response)

    assert isinstance(retrieved, dict)
    assert len(retrieved) == 3
    assert "summary" in retrieved
    assert "return" in retrieved

    return_value = retrieved.get("return")
    assert isinstance(return_value, dict)
    assert len(return_value) == 2
    assert "return_type" in return_value
    assert "desc" in return_value


def test_doc_string_for_method_3():
    """Tests creating doc string for a class method no args."""
    constants.load_secrets()
    txt = """
    def say_hello(self):
        pass
    """
    prompt = prompts.MAKE_DOC_STRING_FOR_FUNCTION + txt
    response = chatbot.run_query(prompt)
    retrieved = json.loads(response)

    assert isinstance(retrieved, dict)
    assert len(retrieved) == 2
    assert "summary" in retrieved


def test_convert_func_json_to_doc():
    """Tests the convert_func_json_to_doc."""
    doc_as_json = {
        "summary": "Calculate the maximum profit.",
        "arguments": [
            {
                "arg_name": "prices",
                "arg_type": "list",
                "desc": "List of stock prices"}],
        "return": {
            "return_type": "int",
            "desc": "Maximum profit possible"},
        "prefixed_spaces": 4
    }
    response = prompts.convert_func_json_to_doc(doc_as_json)
    print("---------------------")
    print(response)

