"""Query service specializing in coding."""

import flask
import ollama


PORT = 15959

app = flask.Flask(__name__)


class ChatBot:
    """Chatbot using the Ollama API to generate responses.

    :cvar ollama.Client _client: The ollama client object.
    :cvar str _MODEL: The Ollama model to use..
    """
    _client = None
    _MODEL = "llama3.2"

    @classmethod
    def run_query(cls, query):
        """Executes the passed in query.

        :param str query: The query to execute.

        :returns: The response to the query.
        :rtype: str.
        """
        if not cls._client:
            cls._client = ollama.Client()
        response = cls._client.generate(model=cls._MODEL, prompt=query)
        return response['response']


@app.route('/', methods=['POST'])
def query_executor():
    """Serves a client query."""
    user_query = flask.request.data.decode('utf-8')
    answer = ChatBot.run_query(user_query)
    return flask.Response(answer, mimetype='text/plain')


if __name__ == '__main__':
    app.run(port=PORT, host="0.0.0.0")
