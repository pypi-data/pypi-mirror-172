# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tasks_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
from ..common import objects_pb2 as objects__pb2
from ..common import task_status_pb2 as task__status__pb2
from ..common import tasks_common_pb2 as tasks__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13tasks_service.proto\x12\x19\x61rmonik.api.grpc.v1.tasks\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\robjects.proto\x1a\x11task_status.proto\x1a\x12tasks_common.proto2\xb6\x03\n\x05Tasks\x12h\n\tListTasks\x12+.armonik.api.grpc.v1.tasks.ListTasksRequest\x1a,.armonik.api.grpc.v1.tasks.ListTasksResponse\"\x00\x12\x62\n\x07GetTask\x12).armonik.api.grpc.v1.tasks.GetTaskRequest\x1a*.armonik.api.grpc.v1.tasks.GetTaskResponse\"\x00\x12n\n\x0b\x43\x61ncelTasks\x12-.armonik.api.grpc.v1.tasks.CancelTasksRequest\x1a..armonik.api.grpc.v1.tasks.CancelTasksResponse\"\x00\x12o\n\x0cGetResultIds\x12..armonik.api.grpc.v1.tasks.GetResultIdsRequest\x1a/.armonik.api.grpc.v1.tasks.GetResultIdsResponseB\x1c\xaa\x02\x19\x41rmoniK.Api.gRPC.V1.Tasksb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tasks_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\031ArmoniK.Api.gRPC.V1.Tasks'
  _TASKS._serialized_start=138
  _TASKS._serialized_end=576
# @@protoc_insertion_point(module_scope)
