from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from pfs.api.v1 import model_pb2 as _model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class DeleteFeaturesRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name", "features"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    features: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., features: _Optional[_Iterable[str]] = ...) -> None: ...

class DeleteFeaturesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class DeriveEntityRequest(_message.Message):
    __slots__ = ["base_entity", "derived_entity_name", "entityset_name", "max_depth", "params"]
    BASE_ENTITY_FIELD_NUMBER: _ClassVar[int]
    DERIVED_ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    base_entity: str
    derived_entity_name: str
    entityset_name: str
    max_depth: int
    params: _struct_pb2.Struct
    def __init__(self, entityset_name: _Optional[str] = ..., base_entity: _Optional[str] = ..., max_depth: _Optional[int] = ..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., derived_entity_name: _Optional[str] = ...) -> None: ...

class DeriveEntityResponse(_message.Message):
    __slots__ = ["entity", "features"]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    entity: _model_pb2.Entity
    features: _containers.RepeatedCompositeFieldContainer[_model_pb2.Feature]
    def __init__(self, entity: _Optional[_Union[_model_pb2.Entity, _Mapping]] = ..., features: _Optional[_Iterable[_Union[_model_pb2.Feature, _Mapping]]] = ...) -> None: ...

class DeriveFeaturesRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name", "max_depth", "params"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    MAX_DEPTH_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    max_depth: int
    params: _struct_pb2.Struct
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., max_depth: _Optional[int] = ..., params: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class DeriveFeaturesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PreviewEntityRequest(_message.Message):
    __slots__ = ["auto_scope", "cutoff_time", "entity_name", "entityset_name", "label_entity_name", "label_feature_name", "start_time"]
    AUTO_SCOPE_FIELD_NUMBER: _ClassVar[int]
    CUTOFF_TIME_FIELD_NUMBER: _ClassVar[int]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    LABEL_ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    LABEL_FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    auto_scope: bool
    cutoff_time: _timestamp_pb2.Timestamp
    entity_name: str
    entityset_name: str
    label_entity_name: str
    label_feature_name: str
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., cutoff_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., label_entity_name: _Optional[str] = ..., label_feature_name: _Optional[str] = ..., auto_scope: bool = ...) -> None: ...

class PreviewEntityResponse(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: int
    def __init__(self, job_id: _Optional[int] = ...) -> None: ...

class RegisterPreviewEntityRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name", "online"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    online: bool
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., online: bool = ...) -> None: ...

class RegisterPreviewEntityResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
