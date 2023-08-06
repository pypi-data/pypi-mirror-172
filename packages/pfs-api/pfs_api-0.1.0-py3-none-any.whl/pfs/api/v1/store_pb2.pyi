from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import field_mask_pb2 as _field_mask_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from pfs.api.v1 import model_pb2 as _model_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ConnectionInfo(_message.Message):
    __slots__ = ["config", "table_name", "time_index", "type"]
    class ConfigEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    TABLE_NAME_FIELD_NUMBER: _ClassVar[int]
    TIME_INDEX_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    config: _containers.ScalarMap[str, str]
    table_name: str
    time_index: str
    type: _model_pb2.ConnectionType
    def __init__(self, type: _Optional[_Union[_model_pb2.ConnectionType, str]] = ..., table_name: _Optional[str] = ..., time_index: _Optional[str] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DeleteEntityRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ...) -> None: ...

class DeleteEntityResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetEntityConnectionRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ...) -> None: ...

class GetEntityConnectionResponse(_message.Message):
    __slots__ = ["offline_connection", "online_connection", "source_connection"]
    OFFLINE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    ONLINE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    offline_connection: NullableConnectionInfo
    online_connection: NullableConnectionInfo
    source_connection: NullableConnectionInfo
    def __init__(self, source_connection: _Optional[_Union[NullableConnectionInfo, _Mapping]] = ..., offline_connection: _Optional[_Union[NullableConnectionInfo, _Mapping]] = ..., online_connection: _Optional[_Union[NullableConnectionInfo, _Mapping]] = ...) -> None: ...

class GetEntityInstanceRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name", "instance_key"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    INSTANCE_KEY_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    instance_key: str
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., instance_key: _Optional[str] = ...) -> None: ...

class GetEntityInstanceResponse(_message.Message):
    __slots__ = ["json_data"]
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    json_data: str
    def __init__(self, json_data: _Optional[str] = ...) -> None: ...

class GetEntityRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ...) -> None: ...

class GetEntityResponse(_message.Message):
    __slots__ = ["entity", "features"]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    entity: _model_pb2.Entity
    features: _containers.RepeatedCompositeFieldContainer[_model_pb2.Feature]
    def __init__(self, entity: _Optional[_Union[_model_pb2.Entity, _Mapping]] = ..., features: _Optional[_Iterable[_Union[_model_pb2.Feature, _Mapping]]] = ...) -> None: ...

class GetEntitySetRequest(_message.Message):
    __slots__ = ["entityset_name"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    entityset_name: str
    def __init__(self, entityset_name: _Optional[str] = ...) -> None: ...

class GetEntitySetResponse(_message.Message):
    __slots__ = ["entityset"]
    ENTITYSET_FIELD_NUMBER: _ClassVar[int]
    entityset: _model_pb2.EntitySet
    def __init__(self, entityset: _Optional[_Union[_model_pb2.EntitySet, _Mapping]] = ...) -> None: ...

class GetEntitySetsRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class GetEntitySetsResponse(_message.Message):
    __slots__ = ["entitysets"]
    ENTITYSETS_FIELD_NUMBER: _ClassVar[int]
    entitysets: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, entitysets: _Optional[_Iterable[str]] = ...) -> None: ...

class GetEntityStatisticRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ...) -> None: ...

class GetEntityStatisticResponse(_message.Message):
    __slots__ = ["json_data"]
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    json_data: str
    def __init__(self, json_data: _Optional[str] = ...) -> None: ...

class GetFeatureGraphRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name", "feature_name"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    feature_name: str
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., feature_name: _Optional[str] = ...) -> None: ...

class GetFeatureGraphResponse(_message.Message):
    __slots__ = ["dot_source"]
    DOT_SOURCE_FIELD_NUMBER: _ClassVar[int]
    dot_source: str
    def __init__(self, dot_source: _Optional[str] = ...) -> None: ...

class IngestRequest(_message.Message):
    __slots__ = ["data", "entity_name", "entityset_name", "timestamp"]
    DATA_FIELD_NUMBER: _ClassVar[int]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    data: bytes
    entity_name: str
    entityset_name: str
    timestamp: _timestamp_pb2.Timestamp
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., data: _Optional[bytes] = ..., timestamp: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IngestResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class MaterializeFeatureRequest(_message.Message):
    __slots__ = ["cutoff_time", "entity_name", "entityset_name", "start_time"]
    CUTOFF_TIME_FIELD_NUMBER: _ClassVar[int]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    cutoff_time: _timestamp_pb2.Timestamp
    entity_name: str
    entityset_name: str
    start_time: _timestamp_pb2.Timestamp
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., cutoff_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class MaterializeFeatureResponse(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: int
    def __init__(self, job_id: _Optional[int] = ...) -> None: ...

class NullableConnectionInfo(_message.Message):
    __slots__ = ["null_value", "value"]
    NULL_VALUE_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    null_value: _struct_pb2.NullValue
    value: ConnectionInfo
    def __init__(self, null_value: _Optional[_Union[_struct_pb2.NullValue, str]] = ..., value: _Optional[_Union[ConnectionInfo, _Mapping]] = ...) -> None: ...

class PreviewEntityDataRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name", "nrows"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    NROWS_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    nrows: int
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., nrows: _Optional[int] = ...) -> None: ...

class PreviewEntityDataResponse(_message.Message):
    __slots__ = ["json_data"]
    JSON_DATA_FIELD_NUMBER: _ClassVar[int]
    json_data: str
    def __init__(self, json_data: _Optional[str] = ...) -> None: ...

class RegisterEntityRequest(_message.Message):
    __slots__ = ["entity", "entityset_name"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    entity: _model_pb2.Entity
    entityset_name: str
    def __init__(self, entityset_name: _Optional[str] = ..., entity: _Optional[_Union[_model_pb2.Entity, _Mapping]] = ...) -> None: ...

class RegisterEntityResponse(_message.Message):
    __slots__ = ["entity", "entityset_name", "features"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    FEATURES_FIELD_NUMBER: _ClassVar[int]
    entity: _model_pb2.Entity
    entityset_name: str
    features: _containers.RepeatedCompositeFieldContainer[_model_pb2.Feature]
    def __init__(self, entityset_name: _Optional[str] = ..., entity: _Optional[_Union[_model_pb2.Entity, _Mapping]] = ..., features: _Optional[_Iterable[_Union[_model_pb2.Feature, _Mapping]]] = ...) -> None: ...

class RegisterRelationshipRequest(_message.Message):
    __slots__ = ["entityset_name", "relationship"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIP_FIELD_NUMBER: _ClassVar[int]
    entityset_name: str
    relationship: _model_pb2.Relationship
    def __init__(self, entityset_name: _Optional[str] = ..., relationship: _Optional[_Union[_model_pb2.Relationship, _Mapping]] = ...) -> None: ...

class RegisterRelationshipResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SelectFeaturesRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SelectFeaturesResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateEntityColumnTypeRequest(_message.Message):
    __slots__ = ["colunm_typing_info", "entity_name", "entityset_name", "update_mask"]
    COLUNM_TYPING_INFO_FIELD_NUMBER: _ClassVar[int]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    colunm_typing_info: _model_pb2.ColumnTypingInfo
    entity_name: str
    entityset_name: str
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., colunm_typing_info: _Optional[_Union[_model_pb2.ColumnTypingInfo, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateEntityColumnTypeResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class UpdateEntityIndexRequest(_message.Message):
    __slots__ = ["entity", "entity_name", "entityset_name", "update_mask"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    UPDATE_MASK_FIELD_NUMBER: _ClassVar[int]
    entity: _model_pb2.Entity
    entity_name: str
    entityset_name: str
    update_mask: _field_mask_pb2.FieldMask
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., entity: _Optional[_Union[_model_pb2.Entity, _Mapping]] = ..., update_mask: _Optional[_Union[_field_mask_pb2.FieldMask, _Mapping]] = ...) -> None: ...

class UpdateEntityIndexResponse(_message.Message):
    __slots__ = ["entity"]
    ENTITY_FIELD_NUMBER: _ClassVar[int]
    entity: _model_pb2.Entity
    def __init__(self, entity: _Optional[_Union[_model_pb2.Entity, _Mapping]] = ...) -> None: ...

class UpdateEntityStoreConfigRequest(_message.Message):
    __slots__ = ["entity_name", "entityset_name", "online"]
    ENTITYSET_NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    entityset_name: str
    online: bool
    def __init__(self, entityset_name: _Optional[str] = ..., entity_name: _Optional[str] = ..., online: bool = ...) -> None: ...

class UpdateEntityStoreConfigResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
