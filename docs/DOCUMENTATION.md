# Documentation

## Methods

|Sl. No.| Name | Parameters | Returns | Description|
|---|-----|-----|-----|----------|
|1|`generate`|`prompt: str`<br>`sql_file_path: str`<br>`explain_results: bool`<br>`use_rag: bool`<br>`display_results: bool`<br> `conversation_path: str`|`query_result: dict`<br>---<br> `{"query":"", "response_text":""}`|This function generates a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument. `sql_file_path` saves to a specified file. Use Retrieval Augmented Generation (RAG) (`use_rag`) to supply context to the LLM, turned on by default. Explain results (`explain_results`) optional, False by default, can be turned on to get a summary. Similarly `display_results`, False by default, can be switched to True to obtain an explanation in Markdown.<br> Use `conversation_path` to save the interaction as a Markdown file in a folder defined by `conversation_path`.  This overrides the `conversation_path` attribute of DuckDBAssistant.|
|2|`execute`|`prompt: str`<br>`sql_file_path: str`|`result: DuckDBPyConnection`|This function executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument.`sql_file_path` saves to a specified file. If a prompt is missing, `execute` seeks to execute valid SQL commands contained in `sql_file_path`.|
|3|`sql`|`prompt: str`<br>`sql_file_path: str`|`result: DuckDBPyRelation`|This function lazily executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument.`sql_file_path` saves to a specified file. If a prompt is missing, `sql` seeks to execute valid SQL commands contained in `sql_file_path`.|
|4|`change_name`|`new_name: str`|Success / Failure Message (`str`)|This function changes the name of a DuckDBAssistant. Provide the new name as an argument.|
|5|`sync_docs`| |Success / Failure Message (`str`)|This function retrieves data from a specified knowledge source and makes it available in a Chroma collection to help DuckDB Assistant.|
|6|`search`|`prompt:str`<br>`n_results:int`<br>`display_results: bool` |`results: dict`<br>----<br>`{"documents":[],"metadatas":[]}`|Given a user `prompt`, retrieve top `n_results` in terms of similarity to provide Retrieval Augmented Generation (RAG). Users can also choose to use the display results flag (default False) to access results in Markdown.|
|7|`set_duckdb`|`dd:DuckDBPyConnection` |Success message|Given a DuckDB connection object (`DuckDBPyConnection`), sets the `dd` attribute in the Class instance to the connection. |
|8|`add_models`|`model_list: list` |Attribute `model_list` modified|Adds a given model (`str`) or a `list` of models to `model_list` in `DuckDBAssistant |
|9|`set_model_list`|`model_list: list` |Attribute `model_list` modified|Resets the `model_list` property of `DuckDBAssistant` |
|10|`remove_models`|`model_list: list` |Attribute `model_list` modified|Removes specified models from the `model_list` of a `DuckDBAssistant` |

## Class Parameters

```python
dda = DuckDBAssistant()
```

|Sl. No.| Name |Type|Default| Description|
|---|----|----|----|--------|
|1|`additional_system_prompt`|`str`|None|Appends additional instructions to system prompt|
|2|`name`|`str`|None|Name of the DuckDB Assistant instance|
|3|`creationTimeStamp`|`str`|None|Date and time of creation|
|4|`createdBy`|`str`|None|Name of creator|
|5|`dd`|`DuckDBPyConnection`|None|DuckDB connection object associated with the assistant|
|6|`initial_sql`|`str`|For Later Use|
|7|`chroma_collection_path`|`str`|Falls back to `CHROMA_COLLECTION_PATH` environment variable or failing that, temporary `chroma` directory in current working directory|Path to folder holding or intended to hold Chroma (vector database) collection|
|8|`save_conversation`|`bool`| `False`|Indicates whether to save each interaction (where a prompt yields a response) to a Markdown file in a folder defined by `conversation_path`.  |
|9|`conversation_path`|`str`| When `save_conversation` is `True`, takes a default of the form `Interaction-<uuid>` where `uuid` is the `id` attribute of the `DuckDBAssistant` instance.|Indicates the folder where each interaction (where a prompt yields a response) is saved to a Markdown file named in the pattern of `Interaction-<conversation_counter>`.  |

## Other Class Attributes

|Sl. No.| Name |Type|Default| Description|
|---|----|----|----|--------|
|1|`model_list`|`list`|Default of `gemini-3.7-flash` assigned if environment variable `FALLBACK_MODELS` is not populated| Provide a comma-separated list to the `FALLBACK_MODELS` environment variable (e.g. `gemini-3.7-flash,gemini-3.6-flash`) which gets assigned at the time of initialising a `DuckDBAssistant`|