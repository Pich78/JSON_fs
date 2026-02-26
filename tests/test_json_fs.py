import os
import json
import pytest
import shutil
from pathlib import Path
from json_fs import core

@pytest.fixture
def temp_dir(tmp_path):
    return tmp_path

def test_make_dir_and_list(temp_dir):
    new_dir = temp_dir / "myfolder"
    req_mkdir = {"action": "mkdir", "path": str(new_dir)}
    res_mkdir = core.execute(req_mkdir)
    
    assert res_mkdir["status"] == "success"
    assert new_dir.exists()
    
    # Test listing the parent dir
    req_list = {"action": "list", "path": str(temp_dir)}
    res_list = core.execute(req_list)
    assert res_list["status"] == "success"
    
    items = res_list["result"]["items"]
    assert len(items) == 1
    assert items[0]["name"] == "myfolder"
    assert items[0]["type"] == "directory"

def test_write_and_read_file(temp_dir):
    file_path = temp_dir / "test.txt"
    content = "Hello JSON FS!"
    
    res_write = core.execute({"action": "write", "path": str(file_path), "content": content})
    assert res_write["status"] == "success"
    assert res_write["result"]["size"] == len(content)
    
    res_read = core.execute({"action": "read", "path": str(file_path)})
    assert res_read["status"] == "success"
    assert res_read["result"]["content"] == content

def test_error_handling(temp_dir):
    missing_file = temp_dir / "not_here.txt"
    
    res_read = core.execute({"action": "read", "path": str(missing_file)})
    assert res_read["status"] == "error"
    assert res_read["error"] == "FileNotFoundError"
    
    # Check that request is preserved
    assert res_read["request"]["action"] == "read"
    assert res_read["request"]["path"] == str(missing_file)

def test_stat_and_delete(temp_dir):
    file_path = temp_dir / "del.txt"
    file_path.write_text("DELETE ME")
    
    res_stat = core.execute({"action": "stat", "path": str(file_path)})
    assert res_stat["status"] == "success"
    assert res_stat["result"]["type"] == "file"
    assert res_stat["result"]["size"] == 9
    
    res_del = core.execute({"action": "delete", "path": str(file_path)})
    assert res_del["status"] == "success"
    
    assert not file_path.exists()
    
def test_statelessness_out_of_band(temp_dir):
    # Tests that json_fs strictly looks at the filesystem by making out-of-band changes.
    file_path = temp_dir / "out_of_band.txt"
    
    # Write using json_fs
    core.execute({"action": "write", "path": str(file_path), "content": "123"})
    
    # Change externally using standard library instead of json_fs
    file_path.write_text("changed externally")
    
    # Read using json_fs -> we should see external change immediately
    res_read = core.execute({"action": "read", "path": str(file_path)})
    assert res_read["status"] == "success"
    assert res_read["result"]["content"] == "changed externally"
    
def test_binary_files(temp_dir):
    file_path = temp_dir / "binary.dat"
    # base64 for b'\x00\xFF\x00' is 'AP8A'
    res_write = core.execute({"action": "write", "path": str(file_path), "content": "AP8A", "binary": True})
    assert res_write["status"] == "success"
    assert res_write["result"]["size"] == 3
    
    assert file_path.read_bytes() == b'\x00\xFF\x00'
    
    res_read = core.execute({"action": "read", "path": str(file_path), "binary": True})
    assert res_read["status"] == "success"
    assert res_read["result"]["content"] == "AP8A"
