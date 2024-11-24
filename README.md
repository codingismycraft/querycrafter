# QueryCrafter

QueryCrafter is a chat bot specializing mostly in  coding queries. Designed to
assist developers serving as thin layer to any of the supported LLMs (like
llama or gpt).

To set up QueryCrafter, follow these steps:

## Clone the repository
   ```sh
   git clone https://github.com/codingismycraft/querycrafter.git
   cd querycrafter
   ```

## Add the settings to the .env file

The configuration of the QueryCrafter is based on the file `.env` which must be
created under the root directory of the project.

The structure of this file is the following:

```
OPENAI_API_KEY=<valid-gpt-api-key>
LLM_MODEL=<valid-model-name>
EXTERNAL_FRONT_END_PORT=15959
INTERNAL_FRONT_END_PORT=15959
```

The `OPENAI_API_KEY` value is only needed if the `LLM_MODEL` is served by GPT
(if you are using a `LLAMA` served model you will not need to set it.)

The supported models are the following:

```
codellama:7b
llama3:8b
llama3.2
gpt-3.5-turbo
gpt-4-turbo"
```

## Activate the virtual environment

From the root directory of the repo you must create a virtual env and then run
the server:

```sh
python3 -m venv qcenv
source ./qcenv/bin/activate
```

## Install dependencies

```sh
pip3 install -r requirements.txt
```

## Run the server

```sh
python3 server.py
```


## Usage
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

