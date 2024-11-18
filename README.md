# QueryCrafter

## Introduction
QueryCrafter is a chat bot specializing mostly in  coding queries. Designed to
assist developers serving as thin layer to any of the supported LLMs (like
llama or gpt).

## Installation
To set up QueryCrafter, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/codingismycraft/querycrafter.git
   cd querycrafter
   ```

2. Install dependencies:
   ```sh
   pip3 install -r requirements.txt
   ```

3. Activate the virtual environment
From the root directory of the repo you must create a virtual env and then run
the server:

    ```sh
    python3 -m venv qcenv
    source ./qcenv/bin/activate
    ```

4. Run the server:
    ```sh
    python3 server.py
    ```

## Configuration
You can configure the server settings in the `constants.py` file to adjust
parameters such as server port and log levels.

In the `constants.py` we are specifying the LLM model to use. This is driven by
the following list of models:

```
SUPPORTED_MODELS = [
    {
        "provider": "ollama",
        "model_name": "codellama:7b"
    },
    {
        "provider": "ollama",
        "model_name": "llama3:8b"
    },
    {
        "provider": "openai",
        "model_name": "gpt-3.5-turbo"
    },
    {
        "provider": "openai",
        "model_name": "gpt-4-turbo",
        "is_active": True
    },
]
```

- The `is_active` key is that sets the LLM model to use. If more that one models
are active an error will be raised.

- If using an openai model (like in the above example) then you will need to
  create a hidden file named `.env` under the same directory as the
  `constants.py` file and there add the `OPENAI_API_KEY` as follows:

  ```
  OPENAI_API_KEY=<the-key>
  ```

## Usage
Once running, QueryCrafter can be accessed to post queries. Send your
query to the server and receive the response from the LLM.

The user can post his query using the following json example:

**Query:**
```bash
curl --location 'http://localhost:15959/' \
--header 'Content-Type: text/plain' \
--data 'write the doc string for the following function:

def foo():
    return "test"'
```

**Response:**
```python
```

See for more examples under the tests directory.

