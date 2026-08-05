# Documentation

## Methods

|Sl. No.| Name | Parameters | Returns | Description|
|---|-----|-----|-----|----------|
|1|`generate`|`prompt: str`<br>`explain_results: bool`<br>`use_rag: bool`|`query_result: dict`<br>---<br> `{"query":"", "response_text":""}`|This function generates a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument. Use Retrieval Augmented Generation (RAG) (`use_rag`) to supply context to the LLM, turned on by default. Explain results (`explain_results`) optional, False by default, can be turned on to get a summary.|
|2|`execute`|`prompt: str`|`result: DuckDBPyConnection`|This function executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument.|
|3|`sql`|`prompt: str`|`result: DuckDBPyRelation`|This function lazily executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument.|
|4|`change_name`|`new_name: str`|Success / Failure Message (`str`)|This function changes the name of a DuckDBAssistant. Provide the new name as an argument.|
|5|`sync_docs`| |Success / Failure Message (`str`)|This function retrieves data from a specified knowledge source and makes it available in a Chroma collection to help DuckDB Assistant.|
|6|`search`|`prompt:str`<br>`n_results:int` |`results: dict`<br>----<br>`{"documents":[],"metadatas":[]}`|Given a user `prompt`, retrieve top `n_results` in terms of similarity to provide Retrieval Augmented Generation (RAG)|
