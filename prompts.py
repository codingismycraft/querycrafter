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

You will also need to return the number of the spaces that will be needed for
each line of the docstring. You can just count the number of spaces that are
prefixing the very first line of code of the passed in function. You must
return this integer value as a separate key called: prefixed_spaces

If notes are empty you should not return them as a separate key.

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
       'notes': 'Notes as text',
       'prefixed_spaces': 4,
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

You will also need to return the number of the spaces that will be needed for
each line of the docstring. You can just count the number of spaces that are
prefixing the very first line of code of the passed in function. You must
return this integer value as a separate key called: prefixed_spaces

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
       'notes': 'Notes as text',
       'prefixed_spaces': 4
    }

You only return the json document and no other text.
Do not enclose the returned json in triple quotes, just return the pure text.

The function to write the docstring for is the following:

"""


def convert_func_json_to_doc(doc_as_json):
    """Converts the passed in dict to a doc string.

    :param dict doc_as_json: The documenation of a function (or method) passed
    as a dictionary.

    :returns: The doc string that correspods to the passed in dict.
    :rtype: str
    """
    prefixed_spaces = int(doc_as_json.get("prefixed_spaces", "0"))
    prefix = " " * prefixed_spaces
    lines = [
        '"""' + doc_as_json.get("summary", ""),
        "\n"
    ]
    lines.append('\n')

    notes = doc_as_json.get("notes")

    if notes:
        p = format_line(notes, 80)
        for p1 in p.split('\n'):
            lines.append(p1)
            lines.append('\n')
        lines.append('\n')

    for argument in doc_as_json.get("arguments", []):
        arg_name = argument.get("arg_name")
        arg_type = argument.get("arg_type")
        desc = argument.get("desc")
        p = f":param {arg_type} {arg_name}: {desc}"
        p = format_line(p, 80)

        for p1 in p.split('\n'):
            lines.append(p1)
            lines.append('\n')
        lines.append('\n')

    return_info = doc_as_json.get("return")

    if return_info:
        desc = return_info.get("desc")
        if desc:
            p = format_line(f":returns: {desc}", 80)
            for p1 in p.split('\n'):
                lines.append(p1)
                lines.append('\n')
            return_type = return_info.get("return_type")
            if return_type:
                lines.append(f":rtype: {return_type}\n")

    exceptions = doc_as_json.get("exceptions")

    if exceptions:
        lines.append('\n')
        for ex in exceptions:
            lines.append(f":raises: {ex}")
            lines.append('\n')

    lines.append('"""')
    lines.append('\n')
    docstr = ""
    for line in lines:
        docstr += prefix + line
    return docstr


def format_line(line, max_length):
    """Formats the line of text to fit within a specified maximum length.

    If the passed in line exceeds the max length this function is breaking it
    down to multiple lines each of them having the same number of leading
    spaces as the first line while been less that the max length.

    Used to format strings in a doc string and fit them properly.

    :param str line: The line of text to be formatted.
    :param int max_length: The maximum allowed length of the formatted line.

    :returns: The formatted line, potentially wrapped to multiple lines if necessary.
    :rtype: str
    """
    line = line.rstrip()
    if len(line) < max_length:
        return line

    counter = 0
    for c in line:
        if c == ' ':
            counter += 1
        else:
            break
    leading_spaces = ' ' * counter

    index = max_length - 1
    while index >= 0:
        if line[index] == ' ':
            break
        index -= 1

    return line[:index] + "\n" + format_line(
        leading_spaces + line[index:].lstrip(), max_length
    )
