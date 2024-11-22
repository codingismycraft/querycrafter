"""Defines the functions to covert json to docstrings.

The response from the LLM based on the used prompts when it comes to
writting docstrings is represented as json (not as text). In this module
we define the functions the convert the retrieved json to text that can
be incorporated in the function / method / class body.
"""

import querycrafter.src.impl.common as common
import querycrafter.src.impl.linespliter as linespliter

DocType = common.DocType

# The default maximum line length.
DEFAULT_MAX_LINE_LENGTH = 80

# Allowed doc string lengths.
MIN_LINE_LENGTH = 40
MAX_LINE_LENGTH = 120


def make(doc_type, doc_as_json, extra_prefix=0, max_line_length=None):
    """Receives the doc string as a json and returns it as a string.

    :param DocType doc_type: The doctype to write the documenation for.

    :param dict doc_as_json: The componets of the docstr in json format.

    :param int extra_prefix: The number of spaces to force in front of each
    line for the dostr. This variable is applicable in the case the function
    method or class that is documented is nested meaning it has some spaces in
    front of the definition of def or class.

    :param int max_line_length: The maximum length for each line in the docstr;
    if None then the DEFAULT_MAX_LINE_LENGTH will be used.

    :returns: The docstring for the passed in doctype and source code.
    :rtype: str

    :raise: ValueError
    """
    max_line_length = max_line_length or DEFAULT_MAX_LINE_LENGTH
    if max_line_length > MAX_LINE_LENGTH or max_line_length < MIN_LINE_LENGTH:
        raise ValueError(f"Invalid line length: {max_line_length}")
    if doc_type == DocType.FUNCTION:
        return _json_to_function_docstr(
            doc_as_json, extra_prefix, max_line_length)
    elif doc_type == DocType.CLASS:
        return _json_to_class_docstr(
            doc_as_json, extra_prefix, max_line_length)
    raise ValueError(f"Unsupported doc_type: {str(doc_type)}")


def _json_to_class_docstr(doc_as_json, extra_prefix, max_line_length):
    """Converts the passed in dict for the class to a doc string.

    Applies to class level docstr.

    :param dict doc_as_json: The class level documentation details passed
    as a dictionary.

    :param int extra_prefix: The number of spaces to force in front of each
    line for the dostr. This variable is applicable in the case the function
    method or class that is documented is nested meaning it has some spaces in
    front of the definition of def or class.

    :param int max_line_length: The maximum length for each line in the docstr;

    :returns: The doc string that correspods to the passed in dict.
    :rtype: str
    """
    prefixed_spaces = int(doc_as_json.get("prefixed_spaces", "0"))
    prefixed_spaces += extra_prefix
    prefix = " " * (prefixed_spaces)

    lines = [
        '"""' + doc_as_json.get("summary", "") + "\n"
    ]
    lines.append('\n')
    notes = doc_as_json.get("notes")

    effective_length = max_line_length - prefixed_spaces

    # Add the notes section.
    notes = doc_as_json.get("notes")
    if notes:
        lines.extend(linespliter.split_line(notes, effective_length))
        lines.append('\n')

    # Add the instance level variables.
    ivars = doc_as_json.get("ivars", [])
    for index, var_info in enumerate(ivars):
        arg_name = var_info.get("arg_name")
        arg_type = var_info.get("arg_type")
        desc = var_info.get("desc")
        if arg_type:
            p = f":ivar {arg_type} {arg_name}: {desc}"
        else:
            p = f":ivar {arg_name}: {desc}"
        if index > 0:
            lines.append('\n')
        lines.extend(linespliter.split_line(p, effective_length))

    # Add the class level variables.
    cvars = doc_as_json.get("cvars", [])
    for var_info in cvars:
        arg_name = var_info.get("arg_name")
        arg_type = var_info.get("arg_type")
        desc = var_info.get("desc")
        if arg_type:
            p = f":cvar {arg_type} {arg_name}: {desc}"
        else:
            p = f":cvar {arg_name}: {desc}"
        lines.append('\n')
        lines.extend(linespliter.split_line(p, effective_length))

    # Add the closing quotes.
    lines.append('"""')
    lines.append('\n')

    docstr = ""
    for line in lines:
        line = line.strip()
        if line:
            docstr += prefix + line.strip() + '\n'
        else:
            docstr += '\n'
    return docstr


def _json_to_function_docstr(doc_as_json, extra_prefix, max_line_length):
    """Converts the passed in dict to a doc string.

    :param dict doc_as_json: The documenation of a function (or method) passed
    as a dictionary.

    :param int extra_prefix: The number of spaces to force in front of each
    line for the dostr. This variable is applicable in the case the function
    method or class that is documented is nested meaning it has some spaces in
    front of the definition of def or class.

    :param int max_line_length: The maximum length for each line in the docstr;

    :returns: The doc string that correspods to the passed in dict.
    :rtype: str
    """
    prefixed_spaces = int(doc_as_json.get("prefixed_spaces", "0"))
    prefixed_spaces += extra_prefix

    effective_length = max_line_length - prefixed_spaces
    prefix = " " * prefixed_spaces
    lines = [
        '"""' + doc_as_json.get("summary", ""),
        "\n"
    ]

    # Add the notes section.
    notes = doc_as_json.get("notes")
    if notes:
        lines.extend(linespliter.split_line(notes, effective_length))
        lines.append('\n')

    # Add the arguments section.
    for argument in doc_as_json.get("arguments", []):
        arg_name = argument.get("arg_name")
        arg_type = argument.get("arg_type")
        desc = argument.get("desc")
        if arg_type:
            p = f":param {arg_type} {arg_name}: {desc}"
        else:
            p = f":param {arg_name}: {desc}"
        lines.extend(linespliter.split_line(p, effective_length))
        lines.append('\n')

    # Add the return section.
    return_info = doc_as_json.get("return")
    if return_info:
        desc = return_info.get("desc")
        if desc:
            p = linespliter.split_line(f":returns: {desc}", effective_length)
            lines.extend(p)

            return_type = return_info.get("return_type")
            if return_type:
                lines.append(f":rtype: {return_type}")

    exceptions = doc_as_json.get("exceptions")

    if exceptions:
        for ex in exceptions:
            lines.append('\n')
            lines.append(f":raises: {ex}")
    lines.append('"""')
    lines.append('\n')

    docstr = ""
    for line in lines:
        line = line.strip()
        if line:
            docstr += prefix + line.strip() + '\n'
        else:
            docstr += '\n'
    return docstr
