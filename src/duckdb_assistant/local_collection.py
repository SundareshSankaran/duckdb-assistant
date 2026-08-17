# The following functions enable storage of local knowledge in a Chroma collection to be used by DuckDBAssistant as needed.

def clone_sparse_checkout(repo_url: str, target_dir: str, folder_path: str, branch: str = "main"):
    """
    Clone only a specific folder from a GitHub repo using sparse checkout.
    """

    import os
    import shutil
    import subprocess
    
    target_dir = os.path.abspath(target_dir)

    if os.path.exists(target_dir):
        shutil.rmtree(target_dir)

    subprocess.run(
        ["git", "clone", "--no-checkout", "--depth", "1", repo_url, target_dir],
        check=True,
    )

    cwd = os.getcwd()
    try:
        os.chdir(target_dir)
        subprocess.run(["git", "sparse-checkout", "init", "--cone"], check=True)
        subprocess.run(["git", "sparse-checkout", "set", folder_path], check=True)
        subprocess.run(["git", "checkout", branch], check=True)
    finally:
        os.chdir(cwd)

def find_markdown_files(root_folder: str) -> List[Path]:
    """
    Recursively find all .md files under root_folder.
    """
    from pathlib import Path
    root = Path(root_folder)
    return [p for p in root.rglob("*.md") if p.is_file()]

def extract_title(md_text: str, fallback: str) -> str:
    for line in md_text.splitlines():
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return fallback

def load_markdown_docs(root_folder: str, repo_name: str) -> List[Dict]:
    """
    Load markdown files and create records with id, title, content, and metadata.
    """
    
    
    docs = []
    md_files = find_markdown_files(root_folder)

    for idx, md_path in enumerate(md_files):
        content = md_path.read_text(encoding="utf-8", errors="ignore")
        rel_path = md_path.as_posix()
        title = extract_title(content, fallback=md_path.stem)

        doc_id = f"{repo_name}:{idx}:{md_path.relative_to(root_folder).as_posix()}"

        docs.append(
            {
                "id": doc_id,
                "title": title,
                "content": content,
                "metadata": {
                    "title": title,
                    "source_path": rel_path,
                    "file_name": md_path.name,
                    "extension": md_path.suffix,
                },
            }
        )
    return docs

def store_in_chroma(docs: List[Dict], collection_name: str = "markdown_docs", persist_dir: str = "./chroma_db")->int:
    """
    Store docs in ChromaDB.
    """
    import chromadb
    
    with chromadb.PersistentClient(path=persist_dir) as client:
        collection = client.get_or_create_collection(name=collection_name)
        ids = [doc["id"] for doc in docs]
        documents = [doc["content"] for doc in docs]
        metadatas = [doc["metadata"] for doc in docs]
        collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
        )
        collection_count = collection.count()
    return collection_count



def find_elbow_distance(ys) -> int:
    """
    Elbow as point farthest from the line connecting first and last points.
    Returns 0-based index.
    """

    import numpy as np
    ys = np.asarray(ys, dtype=float)
    x = np.arange(len(ys))

    # Line from (x0, y0) to (xn, yn)
    x0, y0 = x[0], ys[0]
    xn, yn = x[-1], ys[-1]

    # Vector from start to end
    vx, vy = xn - x0, yn - y0
    norm2 = vx**2 + vy**2

    # Distance of each point to the line (proportional, we don't need exact scale)
    distances = np.abs(vx * (ys - y0) - vy * (x - x0)) / np.sqrt(norm2)

    elbow_idx = int(np.argmax(distances))
    return elbow_idx
