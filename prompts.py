"""Defines promts to be used on demand."""

MAKE_DOC_STRING_FOR_CLASS = """
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

    {
       'summary': ' The summary of the function less than 80 chars",
       'ivars': [
            {
                'arg_name1': 'name',
                'arg_type': 'str',
                'desc': 'short description'
            }
       ],
       'cvars': [
            {
                'arg_name2': 'name',
                'arg_type': 'str',
                'desc': 'short description'
            }
       ],
       'notes': 'Notes as text'
    }

You only return the json document and no other text.
Do not enclose the returned json in triple quotes, just return the pure text.


The class to write the docstring for is the following:

"""


MAKE_DOC_STRING_FOR_FUNCTION = """
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


    {
       'summary': ' The summary of the function less than 80 chars",
       'arguments': [
            {
                'arg_name1': 'name',
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
       'notes': 'Notes as text'
    }

You only return the json document and no other text.
Do not enclose the returned json in triple quotes, just return the pure text.

The function to write the docstring for is the following:

"""
