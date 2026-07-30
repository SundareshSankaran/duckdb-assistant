# Documentation

## Methods

|Sl. No.| Name | Parameters | Returns | Description|
|---|-----|-----|-----|----------|
|1|`generate`|`prompt: str`|`duckdb_query: str`|This function generates a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument.|
|2|`execute`|`prompt: str`|`result: DuckDBPyConnection`|This function executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument.|
|3|`sql`|`prompt: str`|`result: DuckDBPyRelation`|This function lazily executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument.|
|4|`change_name`|`new_name: str`|Success / Failure Message (`str`)|This function changes the name of a DuckDBAssistant. Provide the new name as an argument.|

