import json
from pydantic import ValidationError
from . import operations
from .models import FileSystemRequestAdapter

def execute(request_dict):
    """
    Executes a single filesystem operation defined by the JSON/dict payload.
    """
    try:
        request_obj = FileSystemRequestAdapter.validate_python(request_dict)
    except ValidationError as e:
        return _error_response(request_dict, type(e), str(e))
        
    action = request_obj.action
    
    try:
        if action == "read":
            result = operations.read_file(request_obj.path, binary=request_obj.binary)
        elif action == "write":
            result = operations.write_file(request_obj.path, request_obj.content, binary=request_obj.binary)
        elif action == "append":
            result = operations.append_file(request_obj.path, request_obj.content, binary=request_obj.binary)
        elif action == "list":
            result = operations.list_dir(request_obj.path)
        elif action == "delete":
            result = operations.delete_path(request_obj.path)
        elif action == "mkdir":
            result = operations.make_dir(request_obj.path, parents=request_obj.parents)
        elif action == "copy":
            result = operations.copy_path(request_obj.source, request_obj.destination)
        elif action == "move":
            result = operations.move_path(request_obj.source, request_obj.destination)
        elif action == "stat":
            result = operations.stat_path(request_obj.path)
        elif action == "exists":
            result = operations.path_exists(request_obj.path)
        elif action == "schema":
            result = FileSystemRequestAdapter.json_schema()
        else:
            return _error_response(request_dict, ValueError, f"Unknown action: '{action}'")
            
        return _success_response(request_dict, result)
        
    except Exception as e:
        return _error_response(request_dict, type(e), str(e))

def _success_response(request, result):
    return {
        "request": request,
        "status": "success",
        "result": result
    }

def _error_response(request, error_type, message):
    error_name = error_type.__name__ if hasattr(error_type, '__name__') else str(error_type)
    return {
        "request": request,
        "status": "error",
        "error": error_name,
        "message": message
    }

def execute_file(input_path, output_path):
    """
    Reads a JSON request from input_path, executes it, and writes the JSON response to output_path.
    """
    import json
    with open(input_path, 'r', encoding='utf-8') as f:
        request_dict = json.load(f)
        
    result = execute(request_dict)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(result, f, indent=2)

