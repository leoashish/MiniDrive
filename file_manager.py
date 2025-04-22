import os
from pathlib import Path

STORAGE_DIR = Path("storage")

def get_all_files():
    return [{
        'name': f.name,
        'size': f.stat().st_size
    } for f in STORAGE_DIR.glob("*") if f.is_file()]

def delete_file(filename):
    path = STORAGE_DIR / filename
    if path.exists():
        path.unlink()