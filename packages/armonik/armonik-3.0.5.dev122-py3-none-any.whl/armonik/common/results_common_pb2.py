# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: results_common.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import result_status_pb2 as result__status__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x14results_common.proto\x12\x1b\x61rmonik.api.grpc.v1.results\x1a\x13result_status.proto\"\x99\x01\n\tResultRaw\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\rowner_task_id\x18\x03 \x01(\t\x12?\n\x06status\x18\x04 \x01(\x0e\x32/.armonik.api.grpc.v1.result_status.ResultStatus\x12\x12\n\ncreated_at\x18\x05 \x01(\t\"\xc0\x05\n\x12ListResultsRequest\x12\x0c\n\x04page\x18\x01 \x01(\x05\x12\x11\n\tpage_size\x18\x02 \x01(\x05\x12\x46\n\x06\x66ilter\x18\x03 \x01(\x0b\x32\x36.armonik.api.grpc.v1.results.ListResultsRequest.Filter\x12\x42\n\x04sort\x18\x04 \x01(\x0b\x32\x34.armonik.api.grpc.v1.results.ListResultsRequest.Sort\x1a\xb1\x01\n\x06\x46ilter\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x15\n\rowner_task_id\x18\x03 \x01(\t\x12?\n\x06status\x18\x04 \x01(\x0e\x32/.armonik.api.grpc.v1.result_status.ResultStatus\x12\x15\n\rcreated_after\x18\x05 \x01(\t\x12\x16\n\x0e\x63reated_before\x18\x06 \x01(\t\x1a\x9a\x01\n\x04Sort\x12H\n\x05\x66ield\x18\x01 \x01(\x0e\x32\x39.armonik.api.grpc.v1.results.ListResultsRequest.SortField\x12H\n\x05order\x18\x02 \x01(\x0e\x32\x39.armonik.api.grpc.v1.results.ListResultsRequest.SortOrder\"p\n\tSortField\x12\x1a\n\x16SORT_FIELD_UNSPECIFIED\x10\x00\x12\x0e\n\nSESSION_ID\x10\x01\x12\x08\n\x04NAME\x10\x02\x12\x11\n\rOWNER_TASK_ID\x10\x03\x12\n\n\x06STATUS\x10\x04\x12\x0e\n\nCREATED_AT\x10\x05\":\n\tSortOrder\x12\x1a\n\x16SORT_ORDER_UNSPECIFIED\x10\x00\x12\x07\n\x03\x41SC\x10\x01\x12\x08\n\x04\x44\x45SC\x10\x02\"~\n\x13ListResultsResponse\x12\x37\n\x07results\x18\x01 \x03(\x0b\x32&.armonik.api.grpc.v1.results.ResultRaw\x12\x0c\n\x04page\x18\x02 \x01(\x05\x12\x11\n\tpage_size\x18\x03 \x01(\x05\x12\r\n\x05total\x18\x04 \x01(\x05\">\n\x15GetOwnerTaskIdRequest\x12\x12\n\nsession_id\x18\x01 \x01(\t\x12\x11\n\tresult_id\x18\x02 \x03(\t\"\xb9\x01\n\x16GetOwnerTaskIdResponse\x12V\n\x0bresult_task\x18\x01 \x03(\x0b\x32\x41.armonik.api.grpc.v1.results.GetOwnerTaskIdResponse.MapResultTask\x12\x12\n\nsession_id\x18\x02 \x01(\t\x1a\x33\n\rMapResultTask\x12\x11\n\tresult_id\x18\x01 \x01(\t\x12\x0f\n\x07task_id\x18\x02 \x01(\tB\x1e\xaa\x02\x1b\x41rmoniK.Api.gRPC.V1.Resultsb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'results_common_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\252\002\033ArmoniK.Api.gRPC.V1.Results'
  _RESULTRAW._serialized_start=75
  _RESULTRAW._serialized_end=228
  _LISTRESULTSREQUEST._serialized_start=231
  _LISTRESULTSREQUEST._serialized_end=935
  _LISTRESULTSREQUEST_FILTER._serialized_start=427
  _LISTRESULTSREQUEST_FILTER._serialized_end=604
  _LISTRESULTSREQUEST_SORT._serialized_start=607
  _LISTRESULTSREQUEST_SORT._serialized_end=761
  _LISTRESULTSREQUEST_SORTFIELD._serialized_start=763
  _LISTRESULTSREQUEST_SORTFIELD._serialized_end=875
  _LISTRESULTSREQUEST_SORTORDER._serialized_start=877
  _LISTRESULTSREQUEST_SORTORDER._serialized_end=935
  _LISTRESULTSRESPONSE._serialized_start=937
  _LISTRESULTSRESPONSE._serialized_end=1063
  _GETOWNERTASKIDREQUEST._serialized_start=1065
  _GETOWNERTASKIDREQUEST._serialized_end=1127
  _GETOWNERTASKIDRESPONSE._serialized_start=1130
  _GETOWNERTASKIDRESPONSE._serialized_end=1315
  _GETOWNERTASKIDRESPONSE_MAPRESULTTASK._serialized_start=1264
  _GETOWNERTASKIDRESPONSE_MAPRESULTTASK._serialized_end=1315
# @@protoc_insertion_point(module_scope)
