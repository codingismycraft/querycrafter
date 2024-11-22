"""Query service specializing in coding."""

import flask

import querycrafter.src.impl.common as common
import querycrafter.src.impl.facade as facade

app = flask.Flask(__name__)

DocType = common.DocType


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
        data["document_type"] = common.get_doc_type(data.get("text"))
        doctype = DocType(data.get('document_type'))
        text = data.get('text')
        max_line_length = data.get("max_line_length")
        response = facade.make_docstring(doctype, text, max_line_length)
        return flask.Response(response, mimetype='text/plain')
    except Exception as e:
        return f"An error occurred: {str(e)}", 400


if __name__ == '__main__':
    common.load_secrets()
    app.run(port=common.LISTENING_PORT, host="0.0.0.0")
