from pathlib import Path
import shutil

root = Path(__file__).resolve().parents[1]
delete_dirs = {"__pycache__", ".ipynb_checkpoints", ".pytest_cache", "buildproj", "node_modules"}
delete_files = {".DS_Store"}

for path in root.rglob("*"):
    if path.is_dir() and path.name in delete_dirs:
        shutil.rmtree(path, ignore_errors=True)
    elif path.is_file():
        if path.name in delete_files or path.suffix == ".pyc":
            try:
                path.unlink()
            except FileNotFoundError:
                pass