# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tracdap/config/result.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tracdap.metadata import object_id_pb2 as tracdap_dot_metadata_dot_object__id__pb2
from tracdap.metadata import object_pb2 as tracdap_dot_metadata_dot_object__pb2
from tracdap.metadata import job_pb2 as tracdap_dot_metadata_dot_job__pb2
from tracdap.metadata import tag_update_pb2 as tracdap_dot_metadata_dot_tag__update__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1btracdap/config/result.proto\x12\x0etracdap.config\x1a tracdap/metadata/object_id.proto\x1a\x1dtracdap/metadata/object.proto\x1a\x1atracdap/metadata/job.proto\x1a!tracdap/metadata/tag_update.proto\";\n\rTagUpdateList\x12*\n\x05\x61ttrs\x18\x01 \x03(\x0b\x32\x1b.tracdap.metadata.TagUpdate\"\x92\x03\n\tJobResult\x12*\n\x05jobId\x18\x01 \x01(\x0b\x32\x1b.tracdap.metadata.TagHeader\x12\x33\n\nstatusCode\x18\x02 \x01(\x0e\x32\x1f.tracdap.metadata.JobStatusCode\x12\x15\n\rstatusMessage\x18\x03 \x01(\t\x12\x37\n\x07results\x18\x04 \x03(\x0b\x32&.tracdap.config.JobResult.ResultsEntry\x12\x33\n\x05\x61ttrs\x18\x05 \x03(\x0b\x32$.tracdap.config.JobResult.AttrsEntry\x1aR\n\x0cResultsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".tracdap.metadata.ObjectDefinition:\x02\x38\x01\x1aK\n\nAttrsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12,\n\x05value\x18\x02 \x01(\x0b\x32\x1d.tracdap.config.TagUpdateList:\x02\x38\x01\x42\x1c\n\x18org.finos.tracdap.configP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tracdap.config.result_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.finos.tracdap.configP\001'
  _JOBRESULT_RESULTSENTRY._options = None
  _JOBRESULT_RESULTSENTRY._serialized_options = b'8\001'
  _JOBRESULT_ATTRSENTRY._options = None
  _JOBRESULT_ATTRSENTRY._serialized_options = b'8\001'
  _TAGUPDATELIST._serialized_start=175
  _TAGUPDATELIST._serialized_end=234
  _JOBRESULT._serialized_start=237
  _JOBRESULT._serialized_end=639
  _JOBRESULT_RESULTSENTRY._serialized_start=480
  _JOBRESULT_RESULTSENTRY._serialized_end=562
  _JOBRESULT_ATTRSENTRY._serialized_start=564
  _JOBRESULT_ATTRSENTRY._serialized_end=639
# @@protoc_insertion_point(module_scope)
