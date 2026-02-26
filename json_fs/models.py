from typing import Any, Dict, Literal, Union, Optional, Annotated
from pydantic import BaseModel, Field, TypeAdapter

class ReadRequest(BaseModel):
    action: Literal["read"]
    path: str
    binary: bool = False

class WriteRequest(BaseModel):
    action: Literal["write"]
    path: str
    content: str = ""
    binary: bool = False

class AppendRequest(BaseModel):
    action: Literal["append"]
    path: str
    content: str = ""
    binary: bool = False

class ListRequest(BaseModel):
    action: Literal["list"]
    path: str

class DeleteRequest(BaseModel):
    action: Literal["delete"]
    path: str

class MkdirRequest(BaseModel):
    action: Literal["mkdir"]
    path: str
    parents: bool = False

class CopyRequest(BaseModel):
    action: Literal["copy"]
    source: str
    destination: str

class MoveRequest(BaseModel):
    action: Literal["move"]
    source: str
    destination: str

class StatRequest(BaseModel):
    action: Literal["stat"]
    path: str

class ExistsRequest(BaseModel):
    action: Literal["exists"]
    path: str

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
