# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: results_service.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from ..common import results_common_pb2 as results__common__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15results_service.proto\x12\x1b\x61rmonik.api.grpc.v1.results\x1a\x14results_common.proto2\xf8\x01\n\x07Results\x12r\n\x0bListResults\x12/.armonik.api.grpc.v1.results.ListResultsRequest\x1a\x30.armonik.api.grpc.v1.results.ListResultsResponse\"\x00\x12y\n\x0eGetOwnerTaskId\x12\x32.armonik.api.grpc.v1.results.GetOwnerTaskIdRequest\x1a\x33.armonik.api.grpc.v1.results.GetOwnerTaskIdResponseB\x1e\xaa\x02\x1b\x41rmoniK.Api.gRPC.V1.Resultsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'results_service_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\033ArmoniK.Api.gRPC.V1.Results'
  _RESULTS._serialized_start=77
  _RESULTS._serialized_end=325
# @@protoc_insertion_point(module_scope)
