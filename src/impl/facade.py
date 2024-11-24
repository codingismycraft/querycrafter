"""Exposes the docstr creation logic as a facade."""

import json

import querycrafter.src.impl.chatbot as chatbot
import querycrafter.src.impl.common as common
import querycrafter.src.impl.docwriter as docwriter
import querycrafter.src.impl.linespliter as linespliter
import querycrafter.src.impl.prompt_maker as prompt_maker

DocType = common.DocType


def make_docstring(doc_type, user_request, max_line_length=None):
    """Makes the docstring for the passed in type and source code.

    :param DocType doc_type: The doctype to write the documenation for.
    :param str user_request: The user_request to use for the docstr.
    :param int max_line_length: The max line length (by default will be 80).

    :returns: The docstring for the passed in doctype and source code.
    :rtype: str
    """
    prefix_spaces = common.get_prefix_spaces(user_request)
    prompt = prompt_maker.make_prompt(doc_type, user_request)
    llm_response = chatbot.run_query(prompt)
    if doc_type == DocType.GENERIC:
        lines = linespliter.split_line(
            llm_response,
            common.DEFAULT_MAX_LINE_LENGTH
        )
        return '\n'.join(lines)
    else:
        doc_as_json = json.loads(llm_response)
        doc_as_txt = docwriter.make(
            doc_type, doc_as_json, prefix_spaces, max_line_length
        )
        return doc_as_txt
