from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
JOB_STATE_CANCELLED: JobState
JOB_STATE_COMPLETE: JobState
JOB_STATE_FAILED: JobState
JOB_STATE_NEW: JobState
JOB_STATE_RUNNING: JobState
JOB_STATE_UNSPECIFIED: JobState

class Job(_message.Message):
    __slots__ = ["complete_tasks", "end_time", "id", "name", "properties", "start_time", "state", "total_tasks"]
    class PropertiesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: _struct_pb2.Value
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[_struct_pb2.Value, _Mapping]] = ...) -> None: ...
    COMPLETE_TASKS_FIELD_NUMBER: _ClassVar[int]
    END_TIME_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    START_TIME_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    TOTAL_TASKS_FIELD_NUMBER: _ClassVar[int]
    complete_tasks: int
    end_time: _timestamp_pb2.Timestamp
    id: int
    name: str
    properties: _containers.MessageMap[str, _struct_pb2.Value]
    start_time: _timestamp_pb2.Timestamp
    state: JobState
    total_tasks: int
    def __init__(self, id: _Optional[int] = ..., name: _Optional[str] = ..., state: _Optional[_Union[JobState, str]] = ..., total_tasks: _Optional[int] = ..., complete_tasks: _Optional[int] = ..., properties: _Optional[_Mapping[str, _struct_pb2.Value]] = ..., start_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., end_time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class WatchJobStateRequest(_message.Message):
    __slots__ = ["job_id"]
    JOB_ID_FIELD_NUMBER: _ClassVar[int]
    job_id: int
    def __init__(self, job_id: _Optional[int] = ...) -> None: ...

class WatchJobStateResponse(_message.Message):
    __slots__ = ["job"]
    JOB_FIELD_NUMBER: _ClassVar[int]
    job: Job
    def __init__(self, job: _Optional[_Union[Job, _Mapping]] = ...) -> None: ...

class JobState(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
