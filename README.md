# QueryCrafter

QueryCrafter is a chat bot specializing mostly in  coding queries. Designed to
assist developers serving as thin layer to any of the supported LLMs (like
llama or gpt).

# Create the env file

Under the root directory (either where the docker compose exists or where the
repo is cloned) create a file named `.env` with the following contents:

```
OPENAI_API_KEY=<valid-open-ai-key>
EXTERNAL_FRONT_END_PORT=<host-port>
INTERNAL_FRONT_END_PORT=<guest-port>
LLM_MODEL=<model-to-use>
```

The `OPENAI_API_KEY` value is only needed if the `LLM_MODEL` is served by GPT

If you are using a `LLAMA` served model you will not need to set it the
`OPENAI_API_KEY`.

When running a `LLAMA` model a GPU card is preffered otherwise the performance
will be very slow.

The supported models are the following:

```
codellama:7b
llama3:8b
llama3.2
gpt-3.5-turbo
gpt-4-turbo
```


# Running QueryCrafter using Docker

Under any direcory create the following file and save it as
`docker-compose.yaml`:

```
version: "3.8"

services:
  querycrafter:
    image: jpazarzis/querycrafter:0.2
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - SERVICE_PORT=${INTERNAL_FRONT_END_PORT}
      - LLM_MODEL=${LLM_MODEL}
    ports:
      - "${EXTERNAL_FRONT_END_PORT}:${INTERNAL_FRONT_END_PORT}"
```

The default port where the querycrafter is listening is `15959`


Run the docker container using the following command:

```
docker compose up querycrafter
```

If you need to clean up local docker images:

```
docker stop $(docker ps -aq); docker rm $(docker ps -aq); docker image rm -f $(docker images -q)
docker compose down -v
```
 To pull latest docker image:

 ```
 docker compose pull
 ```

# Running QueryCrafter using python venv

To run the querycrafter for development purposes the easier way will be be to
use venv as described here:

**Install the code**

```sh
git clone https://github.com/codingismycraft/querycrafter.git
cd querycrafter
python3 -m venv qcenv
source ./qcenv/bin/activate
pip3 install -r requirements.txt
 ```

**Run the server**

```sh
python3 server.py
```


# Usage
Once running, QueryCrafter can be accessed to post queries. Send your
query to the server and receive the response from the LLM.

The user can post his query using the following json example:

```bash
curl --location 'http://localhost:15959/' \
--header 'Content-Type: application/json' \
--data '{
    "text": "def foo(i, j): return i +i"
}
'
```

See for more examples under the tests directory.

