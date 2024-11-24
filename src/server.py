"""Query service specializing in coding."""

import os
import logging

import flask

import querycrafter.src.impl.common as common
import querycrafter.src.impl.facade as facade
import querycrafter.src.impl.model_manager as model_manager


app = flask.Flask(__name__)

DocType = common.DocType
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


@app.route('/', methods=['POST'])
def query_executor():
    """Handles POST requests with JSON payload.

    Extracts the 'document_type' and 'text' from a JSON request and returns
    the procesed reslut them as a plain text response.

    If an error occurs during processing, returns an error message with an HTTP
    400 status code.

    Expected JSON format:
    {
        "text": "class Person: pass",
        "max_line_length": 120 (optional)
    }

    The document type field must much the enumerated values in DocType.

    :returns: Plain text response echoing the 'document_type' and 'text'.
    """
    try:
        data = flask.request.json
        logging.info(str(data))
        data["document_type"] = common.get_doc_type(data.get("text"))
        doctype = DocType(data.get('document_type'))
        text = data.get('text')
        max_line_length = data.get("max_line_length")
        response = facade.make_docstring(doctype, text, max_line_length)
        logging.info(str(response))
        return flask.Response(response, mimetype='text/plain')
    except Exception as e:
        logging.exception(e)
        return f"An error occurred: {str(e)}", 400


if __name__ == '__main__':
    common.load_secrets()

    # Assign env settings (comming from the .env file).
    listening_port = os.environ.get("INTERNAL_FRONT_END_PORT")
    if not listening_port:
        listening_port = common.DEFAULT_LISTENING_PORT

    llm_model = os.environ.get("LLM_MODEL")
    if llm_model:
        model_manager.ModelManager.set_active_model(llm_model)

    logging.info(
            "Starting QueryCrafter in port: %s using model %s",
            listening_port,
            model_manager.ModelManager.get_model_name()
    )

    app.run(port=listening_port, host="0.0.0.0")
