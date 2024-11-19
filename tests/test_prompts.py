"""Tests the prompts and the generated responses."""

# pylint: disable=line-too-long
import json
import os

import querycrafter.chatbot as chatbot
import querycrafter.constants as constants
import querycrafter.prompts as prompts

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


def test_format_line_1():
    """Tests the format_line passing less than max max_length."""
    line = "    :param parent: The frame (paned window) fom the tree."
    retrieved = prompts.format_line(line, 80)
    assert line == retrieved


def test_format_line_2():
    """Tests the format_line passing less than max max_length."""
    max_length = 80
    txt = "    :param parent: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est."
    retrieved = prompts.format_line(txt, max_length)
    lines = retrieved.split("\n")

    lines_without_spaces = []
    for line in lines:
        assert line.startswith("    ")
        assert len(line) <= max_length
        lines_without_spaces.append(line.replace(' ', '').replace('\n', ''))

    retrieved_clean = ''.join(lines_without_spaces)
    txt_clean = txt.replace(' ', '').replace('\n', '')

    assert retrieved_clean == txt_clean


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
                "desc": "List of stock prices Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est."}],
        "return": {
            "return_type": "int",
            "desc": "Maximum profit possible Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est. "},
        "prefixed_spaces": 4,
        "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est. ",
    }
    response = prompts.convert_func_json_to_doc(doc_as_json)
    print("---------------------")
    print(response)
