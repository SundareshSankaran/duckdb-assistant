class DuckDBAssistant:
    """This initialises a class to help you generate and execute DuckDB queries."""
    def __init__(self, additional_system_prompt: str = None, name: str = None, creationTimeStamp: str = None, createdBy: str = None, dd: duckdb.DuckDBPyConnection = None, initial_sql: str = None) -> object:
        import json
        import duckdb as dd
        import os

        system_prompt = "You are a DuckDB SQL expert. You will be provided with a user request and additionally a database, table or view schema as part of context. Your task is to use this context to generate a DuckDB SQL query. The query should be optimised for the task at hand and should take into account the facts provided in each user prompt's context. DuckDB SQL dialect should be used always. DuckDB SQL frequently uses extensions. Make note and account for any dependencies required."
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

        # Check for existence of Chroma collection path and assign default if not provided. 
        self.chroma_collection_path = os.getenv("CHROMA_COLLECTION_PATH", os.path.join(os.getcwd(),"chroma"))
        # Create the Chroma collection path directory if it does not exist
        os.makedirs(self.chroma_collection_path, exist_ok=True)        
        
    def __setitem__(self, key, value):
        setattr(self, key, value)
   
    def generate(self, prompt:str, explain_results: bool = False, use_rag: bool = True ) -> dict:
        """This function generates a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
        from .gemini_api import generate_duckdb_query
        if explain_results == True:
            system_prompt = f"{self.system_prompt}\n Your answer should consist of a summary explanation of the code, focussing on what the code does, and the SQL query contained in a single code block in markdown at the beginning. Sometimes the user may ask for just an explanation or information on DuckDB, and that's fine, you do not need to generate code in such a case."
        else:
            system_prompt = f"{self.system_prompt}\n Your answer should consist of ONLY the SQL query contained in a single code block in markdown. Do not include any additional text or explanation."

        if use_rag:
            rag_results = self.search(prompt)
            rag_context = "|".join(rag_results["documents"])
            prompt+=f"Context: {rag_context}"
        
        try:
            query_result = generate_duckdb_query(system_prompt = system_prompt,user_prompt = f"User prompt: {prompt}", explain_results = explain_results)
            self.last_query = {"user_prompt": prompt,"response_text": query_result["response_text"], "duckdb_query": query_result["query"]}
            return query_result
        except Exception as e:
            return {"query": f"Error occurred: {e}"}
        
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
            llm_response = self.generate(prompt)
            if "query" not in llm_response or not llm_response["query"] or llm_response["query"].strip() == "":
                return f"Error occurred: No query generated. Response: {llm_response}"
            else:
                duckdb_query = llm_response["query"]
                result = self.dd.execute(duckdb_query)
                return result
        except Exception as e:
            return f"Error occurred: {e}"

    def sql(self, prompt:str) -> DuckDBPyRelation:
            """This function lazily executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
            try:
                llm_response = self.generate(prompt)
                if "query" not in llm_response or not llm_response["query"] or llm_response["query"].strip() == "":
                    return f"Error occurred: No query generated. Response: {llm_response}"
                else:
                    duckdb_query = llm_response["query"]
                    result = self.dd.sql(duckdb_query)
                    return result
            except Exception as e:
                return f"Error occurred: {e}"

    def sync_docs(self) -> str:
        """This function retrieves data from a specified knowledge source and makes it available in a Chroma collection to help DuckDB Assistant"""
        import os
        from .local_collection import clone_sparse_checkout, find_markdown_files, extract_title, load_markdown_docs,store_in_chroma 
        repo_url = os.getenv("DOC_REPO_URL", "https://github.com/duckdb/duckdb-web.git")
        folder_path = os.getenv("DOC_FOLDER_PATH","docs/current")
        final_collection_path = os.path.join(self.chroma_collection_path,folder_path)
        clone_sparse_checkout(repo_url = repo_url, target_dir =self.chroma_collection_path, folder_path = folder_path, branch="main")
        docs = load_markdown_docs(final_collection_path, "duckdb-docs")
        collection_count = store_in_chroma(docs, collection_name = "duckdb_docs", persist_dir = self.chroma_collection_path)
        return f"{collection_count} documents available in collection duckdb_docs"
    
    def search(self, prompt:str, n_results:int = 10):
        "Given a user prompt, retrieve top n_results in terms of similarity to provide RAG"
        import chromadb
        from .local_collection import find_elbow_distance
        client = chromadb.PersistentClient(self.chroma_collection_path)
        collection = client.get_collection("duckdb_docs")
        if collection.count()>0:
            results = collection.query(query_texts = [prompt], n_results = n_results, include = ["documents","metadatas", "distances"])
            client.close()
            elbow = find_elbow_distance(results["distances"][0])
            results = {k: v[0][:elbow+1] for k, v in results.items() if k in ["documents","metadatas"]}
            return results
        else:
            return {"error":"Collection is empty"}
        



