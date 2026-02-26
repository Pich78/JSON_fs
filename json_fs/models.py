from typing import Any, Dict, Literal, Union, Optional, Annotated
from pydantic import BaseModel, Field, TypeAdapter, ConfigDict

class ReadRequest(BaseModel):
    """
    Reads the complete contents of a file.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "read", "path": "/path/to/file.txt", "binary": False}],
            "returns": {"type": "string", "description": "The file content as string or base64"}
        }
    )
    action: Literal["read"] = Field(description="Action identifier.")
    path: str = Field(description="The absolute or relative path to the file to read.")
    binary: bool = Field(default=False, description="If true, reads as binary and returns a base64 encoded string.")

class WriteRequest(BaseModel):
    """
    Writes content to a file, overwriting it if it exists.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "write", "path": "/path/to/file.txt", "content": "Hello World"}],
            "returns": {"size": "integer"}
        }
    )
    action: Literal["write"] = Field(description="Action identifier.")
    path: str = Field(description="The path to write to.")
    content: str = Field(default="", description="The content to write.")
    binary: bool = Field(default=False, description="If true, decodes the base64 content and writes as binary.")

class AppendRequest(BaseModel):
    """
    Appends content to the end of a file.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "append", "path": "/path/to/file.txt", "content": "More text"}],
            "returns": {"size": "integer"}
        }
    )
    action: Literal["append"] = Field(description="Action identifier.")
    path: str = Field(description="The path to append to.")
    content: str = Field(default="", description="The content to append.")
    binary: bool = Field(default=False, description="If true, decodes the base64 content and appends as binary.")

class ListRequest(BaseModel):
    """
    Lists the contents of a directory.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "list", "path": "/path/to/dir"}],
            "returns": {"items": [{"name": "string", "type": "string", "size": "integer"}]}
        }
    )
    action: Literal["list"] = Field(description="Action identifier.")
    path: str = Field(description="The path to the directory to list.")

class DeleteRequest(BaseModel):
    """
    Deletes a file or directory explicitly.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "delete", "path": "/path/to/delete"}],
            "returns": "null"
        }
    )
    action: Literal["delete"] = Field(description="Action identifier.")
    path: str = Field(description="Path to delete.")

class MkdirRequest(BaseModel):
    """
    Creates a new directory.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "mkdir", "path": "/path/to/newdir", "parents": True}],
            "returns": "null"
        }
    )
    action: Literal["mkdir"] = Field(description="Action identifier.")
    path: str = Field(description="Path to the new directory.")
    parents: bool = Field(default=False, description="If true, also create intermediate directories.")

class CopyRequest(BaseModel):
    """
    Copies a file or directory from source to destination.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "copy", "source": "/path/to/src", "destination": "/path/to/dest"}],
            "returns": "null"
        }
    )
    action: Literal["copy"] = Field(description="Action identifier.")
    source: str = Field(description="Path of the file or directory to copy.")
    destination: str = Field(description="Path to copy to.")

class MoveRequest(BaseModel):
    """
    Moves or renames a file or directory.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "move", "source": "/path/to/src", "destination": "/path/to/dest"}],
            "returns": "null"
        }
    )
    action: Literal["move"] = Field(description="Action identifier.")
    source: str = Field(description="Path of the file or directory to move.")
    destination: str = Field(description="Path to move to.")

class StatRequest(BaseModel):
    """
    Retrieves metadata about a file or directory.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "stat", "path": "/path/to/file.txt"}],
            "returns": {"size": "integer", "mtime": "float", "type": "string"}
        }
    )
    action: Literal["stat"] = Field(description="Action identifier.")
    path: str = Field(description="Path to the file or directory.")

class ExistsRequest(BaseModel):
    """
    Checks if a path exists.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "exists", "path": "/path/to/file.txt"}],
            "returns": {"exists": "boolean"}
        }
    )
    action: Literal["exists"] = Field(description="Action identifier.")
    path: str = Field(description="Path to check.")

class SchemaRequest(BaseModel):
    """
    Retrieves the JSON Schema for the filesystem tools.
    If 'tool' is provided, returns the detailed schema for that specific tool.
    If 'tool' is omitted, returns a simple list of all available tools with a brief description.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"action": "schema"}, {"action": "schema", "tool": "read"}],
            "returns": "object varying based on request"
        }
    )
    action: Literal["schema"] = Field(description="Action identifier.")
    tool: Optional[str] = Field(default=None, description="The specific tool to retrieve schema for.")

FileSystemRequestType = Union[
    ReadRequest,
    WriteRequest,
    AppendRequest,
    ListRequest,
    DeleteRequest,
    MkdirRequest,
    CopyRequest,
    MoveRequest,
    StatRequest,
    ExistsRequest,
    SchemaRequest,
]

FileSystemRequest = Annotated[FileSystemRequestType, Field(discriminator="action")]

FileSystemRequestAdapter = TypeAdapter(FileSystemRequest)

class SuccessResponse(BaseModel):
    request: Dict[str, Any]
    status: Literal["success"] = "success"
    result: Any

class ErrorResponse(BaseModel):
    request: Dict[str, Any]
    status: Literal["error"] = "error"
    error: str
    message: str

FileSystemResponse = Union[SuccessResponse, ErrorResponse]

MODEL_CLASSES = {
    "read": ReadRequest,
    "write": WriteRequest,
    "append": AppendRequest,
    "list": ListRequest,
    "delete": DeleteRequest,
    "mkdir": MkdirRequest,
    "copy": CopyRequest,
    "move": MoveRequest,
    "stat": StatRequest,
    "exists": ExistsRequest,
    "schema": SchemaRequest,
}
