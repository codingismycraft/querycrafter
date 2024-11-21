"""Tests the prompts and the generated responses."""

# pylint: disable=line-too-long
import json
import os


import querycrafter.src.impl.chatbot as chatbot
import querycrafter.src.impl.common as common
import querycrafter.src.impl.prompt_maker as prompt_maker

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))

DocType = common.DocType


def test_doc_string_for_class():
    """Tests creating doc string for a class."""
    common.load_secrets()
    txt = """
    class Person:
        name: None
        TITLES = ['mr.', 'mrs.']

        def __init__(self, name, age):
            self.name = name
            self.age = age
    """
    prompt = prompt_maker.make_prompt(DocType.CLASS, txt)
    response = chatbot.run_query(prompt)
    print(response)
    retrieved = json.loads(response)
    assert isinstance(retrieved, dict)
    assert len(retrieved) == 4
    assert "summary" in retrieved
    assert "ivars" in retrieved
    assert "cvars" in retrieved


def test_doc_string_for_function():
    """Tests creating doc string for a function."""
    common.load_secrets()

    txt = """
    def get_max_profit(prices):
        if not prices:
            raise ValueError
        m = 0
        index = 0
        left = left_side_max_deltas(prices)
        right = right_side_max_deltas(prices)
        while index < len(prices):
            m = max(m, left[index] + right[index])
            index += 1
        if not m:
            raise ConnectionError
        return m
    """
    prompt = prompt_maker.make_prompt(DocType.FUNCTION, txt)
    response = chatbot.run_query(prompt)
    retrieved = json.loads(response)

    assert isinstance(retrieved, dict)
    assert len(retrieved) == 5
    assert "summary" in retrieved
    assert "arguments" in retrieved
    assert "exceptions" in retrieved
    assert "return" in retrieved

    return_value = retrieved.get("return")
    assert isinstance(return_value, dict)
    assert len(return_value) == 2
    assert "return_type" in return_value
    assert "desc" in return_value


def test_doc_string_for_method_1():
    """Tests creating doc string for a class method."""
    common.load_secrets()
    txt = """
    def say_hello(self, crowd, time):
        if is_morning(time):
            print(crowd, "goodmorning")
        else:
            print(crowd, "hello")
    """
    prompt = prompt_maker.make_prompt(DocType.FUNCTION, txt)
    response = chatbot.run_query(prompt)
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
    common.load_secrets()
    txt = """
    def say_hello(self):
        return "OK"
    """
    prompt = prompt_maker.make_prompt(DocType.FUNCTION, txt)
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
    common.load_secrets()
    txt = """
    def say_hello(self):
        pass
    """
    prompt = prompt_maker.make_prompt(DocType.FUNCTION, txt)
    response = chatbot.run_query(prompt)
    retrieved = json.loads(response)

    assert isinstance(retrieved, dict)
    assert len(retrieved) == 2
    assert "summary" in retrieved
