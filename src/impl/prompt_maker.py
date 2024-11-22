"""Provides promts to be used on demand.

A prompt is meant to be assosiated a DocType enumerator and the make_prompt
function is used to build it based on the text that is passed from the client.
"""

import querycrafter.src.impl.common as common


def make_prompt(doc_type, source_code):
    """Makes the prompt to use to create a docstr.

    :param DocType doc_type: The doctype to write the documenation for.
    :param str source_code: The source_code to use for the docstr.

    :returns: The prompt for the passed in source code.
    :rtype: str

    :raises: ValueError.
    """
    if doc_type == common.DocType.FUNCTION:
        return _DOC_STRING_FOR_FUNCTION + source_code
    elif doc_type == common.DocType.CLASS:
        return _DOC_STRING_FOR_CLASS + source_code
    elif doc_type == common.DocType.GENERIC:
        return _DOC_STRING_FOR_GENERIC + source_code

    raise ValueError(f"DocType: {str(doc_type)} is not supported.")


_DOC_STRING_FOR_GENERIC = """
Complete this statement or answer the question:

"""

_DOC_STRING_FOR_CLASS = """
You are a python programmer who is writting the docstring for a class.

You must return ONLY the docstring including the spaces and the triplle code
you should not return source code at all.

The style to use is the following:

- ALL LINES in the docstring MUST have less than 78 chars length including the
opening spaces.

- Single-Line Summary: Start with a brief single-line explanation of what the
method does;

- instance attributes: List and describe each instance level parameter using
  the following format you can find these attributes in the __init_ method.

:ivar str name: The name of the user.

- class level attributes: List and describe class level parameters using
  the following format:

:cvar str ROOT: The root directory

These attributes are either globals or are meant to be used only by
classmethods and they are defined in the class namespace.

- **Extra Information**: If necessary, add details about the class.

- Ensure there is no space between the opening triple quotes
and the start of the text.
- Use line breaks between sections in the docstring to improve readability.
- Align multiline descriptions neatly, maintaining uniform indentation.

You must return a json document with the following structure:

 - in the ivars you should add the instance variables. if there are none
 then you should ommit this section altogether.

 - in the cvars you should add the class level variables. if there are none
 then you should ommit this section altogether.

You will also need to return the number of the spaces that will be needed for
each line of the docstring. You can just count the number of spaces that are
prefixing the very first line of code of the passed in function. You must
return this integer value as a separate key called: prefixed_spaces

If notes are empty you should not return them as a separate key.

    {
       'summary': ' The summary of the function less than 80 chars",
       'ivars': [
            {
                'arg_name': 'name',
                'arg_type': 'str',
                'desc': 'short description'
            }
       ],
       'cvars': [
            {
                'arg_name': 'name',
                'arg_type': 'str',
                'desc': 'short description'
            }
       ],
       'notes': 'Notes as text',
       'prefixed_spaces': 4,
    }

You only return the json document and no other text.
Do not enclose the returned json in triple quotes, just return the pure text.


The class to write the docstring for is the following:

"""


_DOC_STRING_FOR_FUNCTION = """
You are a python programmer who is writting the docstring for a function
or a method.

The user is going to pass to you a function (or a class method) and you
must return a json document with the following structure keeping in mind
that:
    - if the return value is going to be None then the return key is omitted.

    - if no exceptions are raised than no 'exceptions' key must be omitted.

    - you never add the self as an argument (simply omit it).

    - if there are no arguments at all just ommit the arguments key.

    - if the returned notes just repeat the summary just ommit it.

You will also need to return the number of the spaces that will be needed for
each line of the docstring. You can just count the number of spaces that are
prefixing the very first line of code of the passed in function. You must
return this integer value as a separate key called: prefixed_spaces

    {
       'summary': ' The summary of the function less than 80 chars",
       'arguments': [
            {
                'arg_name': 'name',
                'arg_type': 'str',
                'desc': 'short description'
            }
       ],
       'return': {
            'return_type': 'SomeType',
            'desc':'short description'
       }
       'exceptions: [
            'FileDoesNotExist',
       ],
       'notes': 'Notes as text',
       'prefixed_spaces': 4
    }

You only return the json document and no other text.
Do not enclose the returned json in triple quotes, just return the pure text.

The function to write the docstring for is the following:

"""
