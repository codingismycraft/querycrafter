"""Query service specializing in coding."""

import flask

import querycrafter.src.common as common
import querycrafter.src.chatbot as chatbot

app = flask.Flask(__name__)


@app.route('/', methods=['POST'])
def query_executor():
    """Serves a client query."""
    user_query = flask.request.data.decode('utf-8')
    answer = chatbot.run_query(user_query)
    return flask.Response(answer, mimetype='text/plain')


if __name__ == '__main__':
    common.load_secrets()
    app.run(port=common.LISTENING_PORT, host="0.0.0.0")
