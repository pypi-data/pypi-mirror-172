from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from pfs.api.v1 import model_pb2 as _model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class CreateSourceConnectionRequest(_message.Message):
    __slots__ = ["connection"]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    connection: _model_pb2.SourceConnection
    def __init__(self, connection: _Optional[_Union[_model_pb2.SourceConnection, _Mapping]] = ...) -> None: ...

class CreateSourceConnectionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSourceConnectionsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetSourceConnectionsResponse(_message.Message):
    __slots__ = ["sources"]
    SOURCES_FIELD_NUMBER: _ClassVar[int]
    sources: _containers.RepeatedCompositeFieldContainer[_model_pb2.SourceConnection]
    def __init__(self, sources: _Optional[_Iterable[_Union[_model_pb2.SourceConnection, _Mapping]]] = ...) -> None: ...

class UpdateSourceConnectionRequest(_message.Message):
    __slots__ = ["connection", "name", "update_mask"]
    CONNECTION_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    connection: _model_pb2.SourceConnection
    name: str
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, name: _Optional[str] = ..., connection: _Optional[_Union[_model_pb2.SourceConnection, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateSourceConnectionResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
