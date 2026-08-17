

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