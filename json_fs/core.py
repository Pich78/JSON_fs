import json
from . import operations

def execute(request_dict):
    """
    Executes a single filesystem operation defined by the JSON/dict payload.
    """
    if "action" not in request_dict:
        return _error_response(request_dict, ValueError, "Missing 'action' key in request")
        
    action = request_dict["action"]
    path = request_dict.get("path")
    
    try:
        if action == "read":
            binary = request_dict.get("binary", False)
            result = operations.read_file(path, binary=binary)
        elif action == "write":
            content = request_dict.get("content", "")
            binary = request_dict.get("binary", False)
            result = operations.write_file(path, content, binary=binary)
        elif action == "append":
            content = request_dict.get("content", "")
            binary = request_dict.get("binary", False)
            result = operations.append_file(path, content, binary=binary)
        elif action == "list":
            result = operations.list_dir(path)
        elif action == "delete":
            result = operations.delete_path(path)
        elif action == "mkdir":
            parents = request_dict.get("parents", False)
            result = operations.make_dir(path, parents=parents)
        elif action == "copy":
            source = request_dict.get("source")
            destination = request_dict.get("destination")
            result = operations.copy_path(source, destination)
        elif action == "move":
            source = request_dict.get("source")
            destination = request_dict.get("destination")
            result = operations.move_path(source, destination)
        elif action == "stat":
            result = operations.stat_path(path)
        elif action == "exists":
            result = operations.path_exists(path)
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

