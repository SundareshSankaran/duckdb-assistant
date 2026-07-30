class DuckDBAssistant:
    """This initialises a class to help you generate and execute DuckDB queries."""
    def __init__(self, additional_system_prompt: str = None, name: str = None, creationTimeStamp: str = None, createdBy: str = None, dd: duckdb.DuckDBPyConnection = None, initial_sql: str = None) -> object:
        import json
        import duckdb as dd

        system_prompt = "You are a DuckDB SQL expert. You will be provided with a user request and additionally a database, table or view schema as part of context. Your task is to use this context to generate a DuckDB SQL query. The query should be optimised for the task at hand and should take into account the facts provided in each user prompt's context. At a minimum, your task is to return just the SQL query without additional text or commentary. But if the user asks for the additional informaiton such as a summary, an executive report or simply information, do so."
        if additional_system_prompt:
            system_prompt += f" {additional_system_prompt}"

        # Initialisation of attributes
        self.id = None
        self.name=None 
        self.creationTimeStamp=None 
        self.createdBy=None
        self.dd = None
        self.last_query = None
        
        
        # Assign attributes which have been provided
        import uuid
        self.id=uuid.uuid4() if not self.id else self.id
        self.name=name if name else f"Auto_Generated_{self.id}"
        self.creationTimeStamp=creationTimeStamp if creationTimeStamp else self.creationTimeStamp 
        self.createdBy=createdBy  if createdBy else self.createdBy
        self.system_prompt = system_prompt if system_prompt else self.system_prompt
        self.dd = dd if dd else duckdb.connect()

        self.dd.execute(initial_sql) if initial_sql else None
        
    def __setitem__(self, key, value):
        setattr(self, key, value)
   
    def generate(self, prompt:str) -> str:
        """This function generates a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
        from .gemini_api import generate_duckdb_query
        try:
            duckdb_query = generate_duckdb_query(system_prompt = self.system_prompt,user_prompt = f"User prompt: {prompt}")
            self.last_query = {"user_prompt": prompt,"result": duckdb_query}
            return duckdb_query
        except Exception as e:
            return f"Error occurred: {e}"
        
    def change_name(self, new_name: str) -> str:
        """This function changes the name of a DuckDBAssistant. Provide the new name as an argument."""
        try:
            self["name"] = new_name
            return f"Name changed to {new_name}"
        except Exception as e:
            return f"Error occurred: {e}"

    def execute(self, prompt:str) -> DuckDBPyConnection:
        """This function executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
        try:
            duckdb_query = self.generate(prompt)
            result = self.dd.execute(duckdb_query)
            return result
        except Exception as e:
            return f"Error occurred: {e}"

    def sql(self, prompt:str) -> DuckDBPyRelation:
            """This function lazily executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
            try:
                duckdb_query = self.generate(prompt)
                result = self.dd.sql(duckdb_query)
                return result
            except Exception as e:
                return f"Error occurred: {e}"