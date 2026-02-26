# JSON Filesystem Library (`json_fs`)

A Python library that provides a uniform JSON interface for interacting with the computer's filesystem. It accepts JSON requests, performs the specified filesystem operations, and returns JSON responses.

## Features

- **JSON Interface**: All operations are defined and executed via JSON-compatible dictionaries.
- **Pydantic Validation**: Uses Pydantic under the hood for robust request validation and schema generation.
- **Comprehensive Operations**: Supports standard filesystem operations: `read`, `write`, `append`, `list`, `delete`, `mkdir`, `copy`, `move`, `stat`, and `exists`.
- **Dynamic Schema Generation**: Built-in capability to generate JSON schemas for all available tools and their arguments.

## Installation

Ensure you have Python installed. You can install the dependencies using:

```bash
pip install -r requirements.txt
```

*(Note: Requires `pydantic`)*

## Usage

### Using `execute()`

You can execute a single filesystem operation by passing a dictionary to the `execute()` function:

```python
import json
from json_fs.core import execute

request = {
    "action": "list",
    "path": "./"
}

response = execute(request)
print(json.dumps(response, indent=2))
```

### Using `execute_file()`

You can also read a request from a JSON file, execute it, and write the response to another JSON file:

```python
from json_fs.core import execute_file

execute_file("request.json", "response.json")
```

## Available Actions

The library supports the following actions. Each action corresponds to a specific JSON schema.

- **`read`**: Reads the complete contents of a file. Arguments: `path`, `binary` (optional).
- **`write`**: Writes content to a file, overwriting it if it exists. Arguments: `path`, `content`, `binary` (optional).
- **`append`**: Appends content to the end of a file. Arguments: `path`, `content`, `binary` (optional).
- **`list`**: Lists the contents of a directory. Arguments: `path`.
- **`delete`**: Deletes a file or directory explicitly. Arguments: `path`.
- **`mkdir`**: Creates a new directory. Arguments: `path`, `parents` (optional).
- **`copy`**: Copies a file or directory from source to destination. Arguments: `source`, `destination`.
- **`move`**: Moves or renames a file or directory. Arguments: `source`, `destination`.
- **`stat`**: Retrieves metadata about a file or directory. Arguments: `path`.
- **`exists`**: Checks if a path exists. Arguments: `path`.
- **`schema`**: Retrieves the JSON Schema for the filesystem tools. Allows dynamically checking how to structure requests. Arguments: `tool` (optional).

### Schema Exploration

You can easily explore the required formats for any operation using the `schema` action.

```python
from json_fs.core import execute

# List all available actions
print(execute({"action": "schema"}))

# Get detailed schema for the "read" action
print(execute({"action": "schema", "tool": "read"}))
```

## Response Format

All successful responses follow this structure:
```json
{
  "request": { /* Original request */ },
  "status": "success",
  "result": { /* Result data from the operation */ }
}
```

Error responses follow this structure:
```json
{
  "request": { /* Original request */ },
  "status": "error",
  "error": "ErrorType",
  "message": "Detailed error description"
}
```
