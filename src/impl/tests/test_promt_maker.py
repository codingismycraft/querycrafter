"""Tests the prompts and the generated responses."""

# pylint: disable=line-too-long
import json
import os


import querycrafter.src.impl.chatbot as chatbot
import querycrafter.src.impl.common as common
import querycrafter.src.impl.prompts as prompts

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


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

    prompt = prompts.MAKE_DOC_STRING_FOR_CLASS + txt
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

    prompt = prompts.MAKE_DOC_STRING_FOR_FUNCTION + txt
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
    prompt = prompts.MAKE_DOC_STRING_FOR_FUNCTION + txt
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
    common.load_secrets()
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
                "desc": "List of stock prices Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit.  Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere.  Quisque eget imperdiet est."
            },
            {
                "arg_name": "some_other",
                "arg_type": "list",
                "desc": "List of stock prices Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit.  Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere.  Quisque eget imperdiet est."
            }
        ],
        "return": {
            "return_type": "int",
            "desc": "Maximum profit possible Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est. "},
        "prefixed_spaces": 4,
        "exceptions": [
            "ValueError",
            "ConnectionError"
        ],
        "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est. ",
    }
    response = prompts.convert_func_json_to_doc(doc_as_json)
    print(response)
    for line in response.split("\n"):
        if line:
            assert line.startswith("    ")
            assert len(line) < 80


def test_convert_class_json_to_doc():
    """Tests the convert_class_json_to_doc."""
    doc_as_json = {"summary": "Represents a person with a name and age.",
                   "notes": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est. ",
                   "ivars": [{"arg_name": "name",
                              "arg_type": "str",
                              "desc": "The name of the person Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est. ."},
                             {"arg_name": "age",
                              "arg_type": "int",
                              "desc": "The age of the person.Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla nec ipsum at lectus malesuada scelerisque. Curabitur euismod vestibulum hendrerit. Duis ultricies velit vel volutpat venenatis. Nulla suscipit magna et malesuada pulvinar. Curabitur semper sit amet lectus non suscipit. Curabitur justo ante, varius eget iaculis quis, laoreet vitae ipsum. Donec malesuada metus nec rutrum posuere. Quisque eget imperdiet est. "}],
                   "cvars": [{"arg_name": "TITLES",
                              "arg_type": "list",
                              "desc": "List of title options for a person."}],
                   "prefixed_spaces": 4}
    response = prompts.convert_class_json_to_doc(doc_as_json)
    print(response)
    for line in response.split("\n"):
        if line:
            assert line.startswith("    ")
