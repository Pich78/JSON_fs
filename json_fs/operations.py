import os
import shutil
from pathlib import Path
import base64

def read_file(path, binary=False):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
    if p.is_dir():
        raise IsADirectoryError(f"[Errno 21] Is a directory: '{path}'")

    if binary:
        content = p.read_bytes()
        encoded = base64.b64encode(content).decode('ascii')
        return {"content": encoded}
    else:
        return {"content": p.read_text(encoding='utf-8')}

def write_file(path, content, binary=False):
    p = Path(path)
    if p.is_dir():
        raise IsADirectoryError(f"[Errno 21] Is a directory: '{path}'")
        
    if binary:
        decoded = base64.b64decode(content)
        p.write_bytes(decoded)
        size = len(decoded)
    else:
        p.write_text(content, encoding='utf-8')
        size = len(content.encode('utf-8'))
        
    return {"size": size}
    
def append_file(path, content, binary=False):
    p = Path(path)
    if p.is_dir():
        raise IsADirectoryError(f"[Errno 21] Is a directory: '{path}'")
        
    mode = 'ab' if binary else 'a'
    with open(path, mode) as f:
        if binary:
            decoded = base64.b64decode(content)
            f.write(decoded)
            size = len(decoded)
        else:
            f.write(content)
            size = len(content.encode('utf-8'))
            
    return {"size": size}

def list_dir(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
    if not p.is_dir():
        raise NotADirectoryError(f"[Errno 20] Not a directory: '{path}'")
        
    items = []
    for child in p.iterdir():
        stat = child.stat()
        items.append({
            "name": child.name,
            "type": "directory" if child.is_dir() else "file",
            "size": stat.st_size
        })
    return {"items": items}

def delete_path(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
        
    if p.is_dir():
        shutil.rmtree(p)
    else:
        p.unlink()
    return None

def make_dir(path, parents=False):
    p = Path(path)
    p.mkdir(parents=parents, exist_ok=parents)
    return None

def copy_path(source, destination):
    src = Path(source)
    if not src.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{source}'")
        
    if src.is_dir():
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)
    return None

def move_path(source, destination):
    src = Path(source)
    if not src.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{source}'")
    shutil.move(source, destination)
    return None

def stat_path(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"[Errno 2] No such file or directory: '{path}'")
    
    st = p.stat()
    return {
        "size": st.st_size,
        "mtime": st.st_mtime,
        "type": "directory" if p.is_dir() else "file"
    }
    
def path_exists(path):
    p = Path(path)
    return {"exists": p.exists()}
