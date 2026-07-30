# duckdb-assistant: Generate & Execute DuckDB SQL

This repository provides a Python class and associated methods to generate and execute DuckDB SQL. 

[DuckDB](https://duckdb.org) is an open-source, low-footprint, in-process query processing engine which provides access to several data stores and structures like Parquet, CSV, JSON and data located in conventional Relational Database Management Systems (RDBMS). This package uses the [`duckdb`](https://pypi.org/project/duckdb/) Python package along with methods to call a Large Language Model (LLM) from Google Gemini to generate code in a convenient and conversational manner. 

A wiki of this repo has been generated using DeepWiki and is available here: [![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/SundareshSankaran/duckdb-assistant)

Refer this [doc](https://github.com/SundareshSankaran/duckdb-assistant/blob/main/docs/VISION.md) for more details on how this project will evolve.


## Installation

### Local installation
1. Clone this repository
2. To install locally in editable mode, refer [here](https://github.com/SundareshSankaran/duckdb-assistant/blob/main/build/local_install_quick_start.md)

### From PyPi
Run the following command for a pip installation of the package from PyPi.

```shell

pip install --upgrade duckdb-assistant

```

## Usage - quick example

To initialise the DuckDBAssistant class:

```python
from duckdb_assistant import DuckDBAssistant

dda = DuckDBAssistant()
```

Then, to generate a query in natural language,

```python
duckdb_query = dda.generate("Create an empty customer table.")
print(duckdb_query)
```
**Result:**

```bash
>>> duckdb_query = dda.generate("Create an empty customer table.")
>>> print(duckdb_query)
CREATE TABLE IF NOT EXISTS customer (
    customer_id INTEGER PRIMARY KEY,
    first_name VARCHAR,
    last_name VARCHAR,
    email VARCHAR,
    phone VARCHAR,
    address VARCHAR,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

Then, you execute the generated query either through a DuckDB connection or through the inbuilt duckdb Python connection object as follows:

```python
dda.dd.execute(duckdb_query)

```

which is another way of running

```python
import duckdb as dd
dd.execute(duckdb_query)
```

Or, you can choose to call the execute and sql methods available with the class that directly call duckdb's execute and sql methods after generation.

```python

dda.execute("Create an empty customer table.")

dda.sql("Print Hello World through SQL")

```

**Result:**

```bash
>>> dda.execute("Create an empty customer table.")
<_duckdb.DuckDBPyConnection object at 0x10c194af0>
>>> 
>>> dda.sql("Print Hello World through SQL")
┌───────────────┐
│ 'Hello World' │
│    varchar    │
├───────────────┤
│ Hello World   │
└───────────────┘

>>> 
```

## Documentation
Refer this [page](https://github.com/SundareshSankaran/duckdb-assistant/tree/main/docs/DOCUMENTATION.md) for a list of all available methods and attributes.

## Generative AI usage
Core functions (described in [Documentation](https://github.com/SundareshSankaran/duckdb-assistant/tree/main/docs/DOCUMENTATION.md)) use Large Language Models (LLM, starting with Gemini 3.6 Flash) from the Google Gemini family.  While you are free to modify the code to accommodate other LLMs, these are at present the only LLMs supported.  Read this important note regarding functions that make use of Generative AI.

**IMPORTANT**: All outputs returned from Generative AI tools such as LLMs should be carefully reviewed prior to actual use.  Quality of Generative AI outputs are determined by the Large Language Model in use and may be incorrect. Always review the same.

Add the following environmental variable to a .env file supplying variables to your environment. Get your Gemini API key from [Google AI Studio](https://aistudio.google.com/welcome).

```
GEMINI_API_KEY = <your_key>
```

An example env file ([sample.env](https://github.com/SundareshSankaran/duckdb-assistant/blob/main/sample.env)) is provided for this purpose.  Rename this to `.env` and use.


## Convenience: tasks.json
This repository contains a `tasks.json` meant for use in Visual Studio Code which helps clean up temporary files and stands up a virtual environment for quick development and exploration.  Remove this file if you do not want to have Visual Studio Code run the tasks in `tasks.json`.

## Change Log
* Version: 0.1.0 (30JUL2026)
  - First publish of package


Refer  [`CHANGELOG.md`](https://github.com/SundareshSankaran/duckdb-assistant/blob/main/docs/CHANGELOG.md) for other changes.

## Contact
* [Sundaresh Sankaran](mailto:sundaresh.sankaran@gmail.com)
