"""Tests the doc_writer module."""


import querycrafter.src.doc_writer as doc_writer


"""Tests the prompts and the generated responses."""

# pylint: disable=line-too-long
import json
import os


import querycrafter.chatbot as chatbot
import querycrafter.constants as constants
import querycrafter.prompts as prompts

_CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))


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
