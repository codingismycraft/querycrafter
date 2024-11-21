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
        "document_type": "CLASS",
        "text": "class Person: pass"
    }

    The document type field must much the enumerated values in DocType.

    :returns: Plain text response echoing the 'document_type' and 'text'.
    """
    try:
        data = flask.request.json
        doctype = DocType(data.get('document_type'))
        text = data.get('text')
        response = facade.make_docstring(doctype, text)
        return flask.Response(response, mimetype='text/plain')
    except Exception as e:
        return f"An error occurred: {str(e)}", 400


if __name__ == '__main__':
    common.load_secrets()
    app.run(port=common.LISTENING_PORT, host="0.0.0.0")
