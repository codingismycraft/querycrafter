"""Exposes the docstr creation logic as a facade."""

import json


import querycrafter.src.impl.chatbot as chatbot
import querycrafter.src.impl.prompt_maker as prompt_maker
import querycrafter.src.impl.docwriter as docwriter


def make_docstring(doc_type, source_code):
    """Makes the docstring for the passed in type and source code.

    :param DocType doc_type: The doctype to write the documenation for.
    :param str source_code: The source_code to use for the docstr.

    :returns: The docstring for the passed in doctype and source code.
    :rtype: str
    """
    prompt = prompt_maker.make_prompt(doc_type, source_code)
    llm_response = chatbot.run_query(prompt)
    doc_as_json = json.loads(llm_response)
    doc_as_txt = docwriter.make(doc_type, doc_as_json)

    return doc_as_txt
