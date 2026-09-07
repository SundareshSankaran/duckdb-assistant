

def soft_warning(message):
    import warnings
    from IPython.display import display, HTML
    try:
        # Check if running inside a Jupyter/IPython environment
        get_ipython()
        display(HTML(f"""
            <div style="background-color: #fff3cd; color: #856404; 
                        padding: 10px; border-left: 5px solid #ffc107; 
                        font-family: monospace; margin-bottom: 5px;">
                <strong>Warning:</strong> {message}
            </div>
        """))
    except NameError:
        # Fallback for standard Python scripts / terminals
        warnings.warn(message, UserWarning)



def check_collection_exists(path: str, collection_name: str = "abc") -> bool:
    """
    Spins up a transient client to check if a specific collection exists, 
    then closes the client connection immediately.
    """
    import chromadb
    from chromadb.errors import ChromaError

    # Using 'with' keeps the client transient and closes files safely
    with chromadb.PersistentClient(path=path) as client:
        try:
            client.get_collection(name=collection_name)
            return True
        except (ValueError, ChromaError):
            # Chroma throws an error if the collection isn't found
            return False

def save_conversation(prompt: str, query_result:str, dda_instance: DuckDBAssistant = None, conversation_path:str = None) -> bool:
    """
    Checks if a conversation path is provided for either the class as a whole, or for conversation_path and save as needed.

    """
    import os
    from IPython.display import Markdown
    if not hasattr(dda_instance, "conversation_path"):
        return False
    elif dda_instance.conversation_path == None and conversation_path == None:
        return False
    else:
        final_conversation_path = conversation_path or dda_instance.conversation_path
        print(f"Conversation will be saved as Interaction-{dda_instance.conversation_counter}.md in {final_conversation_path}")
        os.makedirs(final_conversation_path,exist_ok = True)
        with open(os.path.join(final_conversation_path,f"Interaction-{dda_instance.conversation_counter}.md"),"w", encoding="utf-8") as f:
            f.write("## Prompt\n")
            f.write(prompt)
            f.write("\n---\n## Response\n")
            f.write(query_result)
        return True

