# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: agent_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ..common import agent_common_pb2 as agent__common__pb2
from ..common import objects_pb2 as objects__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x13\x61gent_service.proto\x12\x19\x61rmonik.api.grpc.v1.agent\x1a\x12\x61gent_common.proto\x1a\robjects.proto2\xf1\x03\n\x05\x41gent\x12h\n\nCreateTask\x12,.armonik.api.grpc.v1.agent.CreateTaskRequest\x1a*.armonik.api.grpc.v1.agent.CreateTaskReply(\x01\x12\x61\n\x0fGetResourceData\x12&.armonik.api.grpc.v1.agent.DataRequest\x1a$.armonik.api.grpc.v1.agent.DataReply0\x01\x12_\n\rGetCommonData\x12&.armonik.api.grpc.v1.agent.DataRequest\x1a$.armonik.api.grpc.v1.agent.DataReply0\x01\x12_\n\rGetDirectData\x12&.armonik.api.grpc.v1.agent.DataRequest\x1a$.armonik.api.grpc.v1.agent.DataReply0\x01\x12Y\n\nSendResult\x12!.armonik.api.grpc.v1.agent.Result\x1a&.armonik.api.grpc.v1.agent.ResultReply(\x01\x42\x1c\xaa\x02\x19\x41rmoniK.Api.gRPC.V1.Agentb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'agent_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\031ArmoniK.Api.gRPC.V1.Agent'
  _AGENT._serialized_start=86
  _AGENT._serialized_end=583
# @@protoc_insertion_point(module_scope)
