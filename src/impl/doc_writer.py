"""Defines the functions to covert json to docstrings.

The response from the LLM based on the used prompts when it comes to
writting docstrings is represented as json (not as text). In this module
we define the functions the convert the retrieved json to text that can
be incorporated in the function / method / class body.
"""


class DocStringWritter:
    """Converts json to textual docstr."""
