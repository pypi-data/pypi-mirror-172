# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tracdap/config/job.proto
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


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x18tracdap/config/job.proto\x12\x0etracdap.config\x1a tracdap/metadata/object_id.proto\x1a\x1dtracdap/metadata/object.proto\x1a\x1atracdap/metadata/job.proto\"\xae\x04\n\tJobConfig\x12*\n\x05jobId\x18\x01 \x01(\x0b\x32\x1b.tracdap.metadata.TagHeader\x12,\n\x03job\x18\x02 \x01(\x0b\x32\x1f.tracdap.metadata.JobDefinition\x12;\n\tresources\x18\x03 \x03(\x0b\x32(.tracdap.config.JobConfig.ResourcesEntry\x12G\n\x0fresourceMapping\x18\x04 \x03(\x0b\x32..tracdap.config.JobConfig.ResourceMappingEntry\x12\x43\n\rresultMapping\x18\x05 \x03(\x0b\x32,.tracdap.config.JobConfig.ResultMappingEntry\x1aT\n\x0eResourcesEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\".tracdap.metadata.ObjectDefinition:\x02\x38\x01\x1aS\n\x14ResourceMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.tracdap.metadata.TagHeader:\x02\x38\x01\x1aQ\n\x12ResultMappingEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x1b.tracdap.metadata.TagHeader:\x02\x38\x01\x42\x1c\n\x18org.finos.tracdap.configP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tracdap.config.job_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\030org.finos.tracdap.configP\001'
  _JOBCONFIG_RESOURCESENTRY._options = None
  _JOBCONFIG_RESOURCESENTRY._serialized_options = b'8\001'
  _JOBCONFIG_RESOURCEMAPPINGENTRY._options = None
  _JOBCONFIG_RESOURCEMAPPINGENTRY._serialized_options = b'8\001'
  _JOBCONFIG_RESULTMAPPINGENTRY._options = None
  _JOBCONFIG_RESULTMAPPINGENTRY._serialized_options = b'8\001'
  _JOBCONFIG._serialized_start=138
  _JOBCONFIG._serialized_end=696
  _JOBCONFIG_RESOURCESENTRY._serialized_start=444
  _JOBCONFIG_RESOURCESENTRY._serialized_end=528
  _JOBCONFIG_RESOURCEMAPPINGENTRY._serialized_start=530
  _JOBCONFIG_RESOURCEMAPPINGENTRY._serialized_end=613
  _JOBCONFIG_RESULTMAPPINGENTRY._serialized_start=615
  _JOBCONFIG_RESULTMAPPINGENTRY._serialized_end=696
# @@protoc_insertion_point(module_scope)
