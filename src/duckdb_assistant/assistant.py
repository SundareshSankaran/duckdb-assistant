class DuckDBAssistant:
    """This initialises a class to help you generate and execute DuckDB queries."""
    def __init__(self, additional_system_prompt: str = None, name: str = None, creationTimeStamp: str = None, createdBy: str = None, dd: DuckDBPyConnection = None, initial_sql: str = None, chroma_collection_path: str = None) -> object:
        import json
        import duckdb 
        import os
        from .helpers import soft_warning, check_collection_exists

        system_prompt = "You are a DuckDB SQL expert. A user prompt may additionally refer a database, table, schema or view as part of context. Your task is to use context to generate a DuckDB SQL query. Query should optimise task at hand and should account for the facts provided in context. Always use DuckDB SQL dialect. DuckDB SQL frequently uses extensions. Make note and account for any dependencies required."
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
        self.dd = dd if dd != None else duckdb.connect()

        self.dd.execute(initial_sql) if initial_sql else None

        # Check for existence of Chroma collection path and assign default if not provided. 
        if not (os.getenv("CHROMA_COLLECTION_PATH")) and chroma_collection_path==None:
            soft_warning("Chroma collection path not set, will be assigned to current location. \nIf you want to use an existing collection, set CHROMA_COLLECTION_PATH environment variable or chroma_collection_path class attribute.")

        self.chroma_collection_path = chroma_collection_path if chroma_collection_path != None else os.getenv("CHROMA_COLLECTION_PATH", os.path.join(os.getcwd(),"chroma"))

        collection_exists = check_collection_exists(self.chroma_collection_path, collection_name = "duckdb_docs")

        if collection_exists == False:
            self.collection_exists=False
            soft_warning("DuckDB documentation collection does not exists.\n Run sync_docs before using Retrieval Augmented Generation.")
        else:
            self.collection_exists = True

        # Create the Chroma collection path directory if it does not exist
        os.makedirs(self.chroma_collection_path, exist_ok=True)     

           
        
    def __setitem__(self, key, value):
        setattr(self, key, value)
   
    def generate(self, prompt:str, explain_results: bool = False, use_rag: bool = True, sql_file_path: str = None ) -> dict:
        """This function generates a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
        from .gemini_api import generate_duckdb_query
        from .helpers import soft_warning, check_collection_exists
        if explain_results == True:
            system_prompt = f"{self.system_prompt}\n Include a summary explanation of the code, focussing on what the code does, with the SQL query contained in a single markdown code block at the beginning. Sometimes users may ask for just an explanation or information on DuckDB, omit the code block in such a case."
        else:
            system_prompt = f"{self.system_prompt}\n Include ONLY the SQL query contained in a single markdown code block . Do not include any additional text or explanation."

        if use_rag:
            if self.collection_exists == False:
                rag_context ="No further context"
            else:
                rag_results = self.search(prompt)
                rag_context = "|".join(rag_results["documents"])
            prompt+=f"Context: {rag_context}"
        
        try:
            query_result = generate_duckdb_query(system_prompt = system_prompt,user_prompt = f"User prompt: {prompt}", explain_results = explain_results)
            self.last_query = {"user_prompt": prompt,"response_text": query_result["response_text"], "duckdb_query": query_result["query"]}
            if sql_file_path:
                with open(sql_file_path,"w",encoding="utf-8") as f:
                    f.write(query_result["query"])
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

    def execute(self, prompt:str=None, sql_file_path:str = None) -> DuckDBPyConnection:
        """This function executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
        if prompt == None or prompt == "":
            if sql_file_path:
                with open(sql_file_path,"r",encoding="utf-8") as f:
                    duckdb_query = f.read()
                result = self.dd.execute(duckdb_query)
                return result
            else:
                return "SQL File path not provided."
        else:
            if sql_file_path:
                try:
                    llm_response = self.generate(prompt, sql_file_path = sql_file_path)
                    if "query" not in llm_response or not llm_response["query"] or llm_response["query"].strip() == "":
                        return f"Error occurred: No query generated. Response: {llm_response}"
                    else:
                        duckdb_query = llm_response["query"]
                        result = self.dd.execute(duckdb_query)
                        return result
                except Exception as e:
                    return f"Error occurred: {e}"
            else:
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

    def sql(self, prompt:str = None, sql_file_path:str = None) -> DuckDBPyRelation:
        """This function lazily executes a DuckDB SQL query based on a given prompt using Gemini API. Provide the prompt as an argument."""
        if prompt == None or prompt == "":
            if sql_file_path:
                with open(sql_file_path,"r",encoding="utf-8") as f:
                    duckdb_query = f.read()
                result = self.dd.execute(duckdb_query)
                return result
            else:
                return "SQL File path not provided."
        else:
            if sql_file_path:
                try:
                    llm_response = self.generate(prompt, sql_file_path=sql_file_path)
                    if "query" not in llm_response or not llm_response["query"] or llm_response["query"].strip() == "":
                        return f"Error occurred: No query generated. Response: {llm_response}"
                    else:
                        duckdb_query = llm_response["query"]
                        result = self.dd.sql(duckdb_query)
                        return result
                except Exception as e:
                    return f"Error occurred: {e}"
            else:
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
    
    def search(self, prompt:str, n_results:int = 10, display_results = False):
        "Given a user prompt, retrieve top n_results in terms of similarity to provide RAG"
        import chromadb
        from .local_collection import find_elbow_distance
        from IPython.display import display, Markdown
        with chromadb.PersistentClient(self.chroma_collection_path) as client:
            collection = client.get_collection("duckdb_docs")
            if collection.count()>0:
                results = collection.query(query_texts = [prompt], n_results = n_results, include = ["documents","metadatas", "distances"])
                client.close()
                elbow = find_elbow_distance(results["distances"][0])
                results = {k: v[0][:elbow+1] for k, v in results.items() if k in ["documents","metadatas"]}
                if display_results:
                    for document in results["documents"]:
                        display(Markdown(document))
                return results
            else:
                return {"error":"Collection is empty"}
        
    def set_duckdb(self, dd: DuckDBPyConnection):
        "Given a DuckDB connection object (`DuckDBPyConnection`), sets the `dd` attribute in the Class instance to the connection."
        self.dd = dd
        return f"DuckDB connection set to {dd}"



