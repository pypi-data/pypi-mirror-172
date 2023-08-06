from google.api import field_behavior_pb2 as _field_behavior_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

CONNECTION_TYPE_DEMO: ConnectionType
CONNECTION_TYPE_HIVE: ConnectionType
CONNECTION_TYPE_IMPALA: ConnectionType
CONNECTION_TYPE_INFLUXDB: ConnectionType
CONNECTION_TYPE_MARIADB: ConnectionType
CONNECTION_TYPE_MYSQL: ConnectionType
CONNECTION_TYPE_ORACLE: ConnectionType
CONNECTION_TYPE_POSTGRESQL: ConnectionType
CONNECTION_TYPE_PRESTO: ConnectionType
CONNECTION_TYPE_SPARKSQL: ConnectionType
CONNECTION_TYPE_SQLSERVER: ConnectionType
CONNECTION_TYPE_UNSPECIFIED: ConnectionType
DATA_SOURCE_TYPE_CONNECT: DataSourceType
DATA_SOURCE_TYPE_DERIVE: DataSourceType
DATA_SOURCE_TYPE_UNSPECIFIED: DataSourceType
DATA_SOURCE_TYPE_UPLOAD: DataSourceType
DESCRIPTOR: _descriptor.FileDescriptor
ENTITY_STATE_ACTIVE: EntityState
ENTITY_STATE_DISABLE: EntityState
ENTITY_STATE_PREVIEW: EntityState
ENTITY_STATE_UNSPECIFIED: EntityState

class ColumnTypingInfo(_message.Message):
    __slots__ = ["description", "logical_type", "metadata", "name", "ordinal", "origin", "physical_type", "semantic_tags", "use_standard_tags"]
    class LogicalType(_message.Message):
        __slots__ = ["parameters", "type"]
        PARAMETERS_FIELD_NUMBER: _ClassVar[int]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        parameters: _struct_pb2.Struct
        type: str
        def __init__(self, parameters: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., type: _Optional[str] = ...) -> None: ...
    class PhysicalType(_message.Message):
        __slots__ = ["type"]
        TYPE_FIELD_NUMBER: _ClassVar[int]
        type: str
        def __init__(self, type: _Optional[str] = ...) -> None: ...
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    LOGICAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    METADATA_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ORDINAL_FIELD_NUMBER: _ClassVar[int]
    ORIGIN_FIELD_NUMBER: _ClassVar[int]
    PHYSICAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    SEMANTIC_TAGS_FIELD_NUMBER: _ClassVar[int]
    USE_STANDARD_TAGS_FIELD_NUMBER: _ClassVar[int]
    description: str
    logical_type: ColumnTypingInfo.LogicalType
    metadata: _struct_pb2.Struct
    name: str
    ordinal: int
    origin: str
    physical_type: ColumnTypingInfo.PhysicalType
    semantic_tags: _containers.RepeatedScalarFieldContainer[str]
    use_standard_tags: bool
    def __init__(self, name: _Optional[str] = ..., ordinal: _Optional[int] = ..., use_standard_tags: bool = ..., physical_type: _Optional[_Union[ColumnTypingInfo.PhysicalType, _Mapping]] = ..., logical_type: _Optional[_Union[ColumnTypingInfo.LogicalType, _Mapping]] = ..., semantic_tags: _Optional[_Iterable[str]] = ..., description: _Optional[str] = ..., origin: _Optional[str] = ..., metadata: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class Entity(_message.Message):
    __slots__ = ["base_entity", "data_source_type", "index", "last_materialize_time", "name", "online", "secondary_time_index", "source_connection", "source_name", "state", "time_index"]
    BASE_ENTITY_FIELD_NUMBER: _ClassVar[int]
    DATA_SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    LAST_MATERIALIZE_TIME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ONLINE_FIELD_NUMBER: _ClassVar[int]
    SECONDARY_TIME_INDEX_FIELD_NUMBER: _ClassVar[int]
    SOURCE_CONNECTION_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TIME_INDEX_FIELD_NUMBER: _ClassVar[int]
    base_entity: str
    data_source_type: DataSourceType
    index: str
    last_materialize_time: _timestamp_pb2.Timestamp
    name: str
    online: bool
    secondary_time_index: str
    source_connection: str
    source_name: str
    state: EntityState
    time_index: str
    def __init__(self, name: _Optional[str] = ..., data_source_type: _Optional[_Union[DataSourceType, str]] = ..., source_connection: _Optional[str] = ..., source_name: _Optional[str] = ..., base_entity: _Optional[str] = ..., index: _Optional[str] = ..., time_index: _Optional[str] = ..., secondary_time_index: _Optional[str] = ..., online: bool = ..., state: _Optional[_Union[EntityState, str]] = ..., last_materialize_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class EntitySet(_message.Message):
    __slots__ = ["entities", "name", "relationships"]
    class EntitiesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Entity
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Entity, _Mapping]] = ...) -> None: ...
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIPS_FIELD_NUMBER: _ClassVar[int]
    entities: _containers.MessageMap[str, Entity]
    name: str
    relationships: _containers.RepeatedCompositeFieldContainer[Relationship]
    def __init__(self, name: _Optional[str] = ..., entities: _Optional[_Mapping[str, Entity]] = ..., relationships: _Optional[_Iterable[_Union[Relationship, _Mapping]]] = ...) -> None: ...

class Feature(_message.Message):
    __slots__ = ["column_typing_info", "definition", "last_materialize_time", "name"]
    COLUMN_TYPING_INFO_FIELD_NUMBER: _ClassVar[int]
    DEFINITION_FIELD_NUMBER: _ClassVar[int]
    LAST_MATERIALIZE_TIME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    column_typing_info: ColumnTypingInfo
    definition: str
    last_materialize_time: _timestamp_pb2.Timestamp
    name: str
    def __init__(self, name: _Optional[str] = ..., definition: _Optional[str] = ..., column_typing_info: _Optional[_Union[ColumnTypingInfo, _Mapping]] = ..., last_materialize_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class FeatureDefinition(_message.Message):
    __slots__ = ["arguments", "dependencies", "name", "type"]
    ARGUMENTS_FIELD_NUMBER: _ClassVar[int]
    DEPENDENCIES_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    arguments: _struct_pb2.Struct
    dependencies: _containers.RepeatedScalarFieldContainer[str]
    name: str
    type: str
    def __init__(self, name: _Optional[str] = ..., type: _Optional[str] = ..., dependencies: _Optional[_Iterable[str]] = ..., arguments: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ...) -> None: ...

class FeatureStatistic(_message.Message):
    __slots__ = ["coef", "iv", "max", "mean", "median", "min", "miss_rate", "mode", "psi", "skew", "std", "xgb_importance"]
    COEF_FIELD_NUMBER: _ClassVar[int]
    IV_FIELD_NUMBER: _ClassVar[int]
    MAX_FIELD_NUMBER: _ClassVar[int]
    MEAN_FIELD_NUMBER: _ClassVar[int]
    MEDIAN_FIELD_NUMBER: _ClassVar[int]
    MIN_FIELD_NUMBER: _ClassVar[int]
    MISS_RATE_FIELD_NUMBER: _ClassVar[int]
    MODE_FIELD_NUMBER: _ClassVar[int]
    PSI_FIELD_NUMBER: _ClassVar[int]
    SKEW_FIELD_NUMBER: _ClassVar[int]
    STD_FIELD_NUMBER: _ClassVar[int]
    XGB_IMPORTANCE_FIELD_NUMBER: _ClassVar[int]
    coef: str
    iv: str
    max: str
    mean: str
    median: str
    min: str
    miss_rate: str
    mode: str
    psi: str
    skew: str
    std: str
    xgb_importance: str
    def __init__(self, miss_rate: _Optional[str] = ..., mode: _Optional[str] = ..., min: _Optional[str] = ..., max: _Optional[str] = ..., median: _Optional[str] = ..., mean: _Optional[str] = ..., std: _Optional[str] = ..., skew: _Optional[str] = ..., psi: _Optional[str] = ..., iv: _Optional[str] = ..., coef: _Optional[str] = ..., xgb_importance: _Optional[str] = ...) -> None: ...

class Relationship(_message.Message):
    __slots__ = ["entity_name", "feature_name", "foreign_entity_name", "foreign_feature_name"]
    ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    FOREIGN_ENTITY_NAME_FIELD_NUMBER: _ClassVar[int]
    FOREIGN_FEATURE_NAME_FIELD_NUMBER: _ClassVar[int]
    entity_name: str
    feature_name: str
    foreign_entity_name: str
    foreign_feature_name: str
    def __init__(self, entity_name: _Optional[str] = ..., feature_name: _Optional[str] = ..., foreign_entity_name: _Optional[str] = ..., foreign_feature_name: _Optional[str] = ...) -> None: ...

class SourceConnection(_message.Message):
    __slots__ = ["config", "name", "type"]
    class ConfigEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    CONFIG_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TYPE_FIELD_NUMBER: _ClassVar[int]
    config: _containers.ScalarMap[str, str]
    name: str
    type: ConnectionType
    def __init__(self, name: _Optional[str] = ..., type: _Optional[_Union[ConnectionType, str]] = ..., config: _Optional[_Mapping[str, str]] = ...) -> None: ...

class DataSourceType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class EntityState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ConnectionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
