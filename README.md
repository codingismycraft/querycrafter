# QueryCrafter

## Introduction
QueryCrafter is your adept companion in crafting precise solutions to coding
queries. Designed to assist developers by providing accurate and insightful
answers, QueryCrafter is a powerful tool that enhances the coding experience
through efficient query processing and expert knowledge delivery.

## Features

- **Instant Query Responses**: Receive quick and accurate answers to your
  coding questions.

- **Expert Knowledge Base**: Leverage a rich repository of coding information
  and best practices.

- **User-Friendly Interface**: Easy-to-use server interface designed to
  streamline the query process.

- **Efficient Processing**: Fast and reliable query handling to support your
  development workflow.

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

## Configuration
You can configure the server settings in the `config.py` file to adjust
parameters such as server port and log levels.

## Contribution
We welcome contributions to improve QueryCrafter! Please feel free to submit
issues or pull requests.

## Future Enhancements

- **Expand Language Support**: Add support for other programming languages
  beyond Python.

- **Enhanced Natural Language Processing**: Improve the accuracy and
  understanding of complex queries.

- **Interactive User Interface**: Develop a graphical user interface for a more
  interactive experience.

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE License - see the LICENSE file for details.

