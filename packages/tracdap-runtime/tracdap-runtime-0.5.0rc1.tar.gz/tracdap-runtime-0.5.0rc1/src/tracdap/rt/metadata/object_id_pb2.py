# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tracdap/metadata/object_id.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tracdap.metadata import type_pb2 as tracdap_dot_metadata_dot_type__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n tracdap/metadata/object_id.proto\x12\x10tracdap.metadata\x1a\x1btracdap/metadata/type.proto\"\xeb\x01\n\tTagHeader\x12\x30\n\nobjectType\x18\x01 \x01(\x0e\x32\x1c.tracdap.metadata.ObjectType\x12\x10\n\x08objectId\x18\x02 \x01(\t\x12\x15\n\robjectVersion\x18\x03 \x01(\x05\x12\x38\n\x0fobjectTimestamp\x18\x04 \x01(\x0b\x32\x1f.tracdap.metadata.DatetimeValue\x12\x12\n\ntagVersion\x18\x05 \x01(\x05\x12\x35\n\x0ctagTimestamp\x18\x06 \x01(\x0b\x32\x1f.tracdap.metadata.DatetimeValue\"\xb9\x02\n\x0bTagSelector\x12\x30\n\nobjectType\x18\x01 \x01(\x0e\x32\x1c.tracdap.metadata.ObjectType\x12\x10\n\x08objectId\x18\x02 \x01(\t\x12\x16\n\x0clatestObject\x18\x03 \x01(\x08H\x00\x12\x17\n\robjectVersion\x18\x04 \x01(\x05H\x00\x12\x35\n\nobjectAsOf\x18\x05 \x01(\x0b\x32\x1f.tracdap.metadata.DatetimeValueH\x00\x12\x13\n\tlatestTag\x18\x06 \x01(\x08H\x01\x12\x14\n\ntagVersion\x18\x07 \x01(\x05H\x01\x12\x32\n\x07tagAsOf\x18\x08 \x01(\x0b\x32\x1f.tracdap.metadata.DatetimeValueH\x01\x42\x10\n\x0eobjectCriteriaB\r\n\x0btagCriteria*|\n\nObjectType\x12\x17\n\x13OBJECT_TYPE_NOT_SET\x10\x00\x12\x08\n\x04\x44\x41TA\x10\x01\x12\t\n\x05MODEL\x10\x02\x12\x08\n\x04\x46LOW\x10\x03\x12\x07\n\x03JOB\x10\x04\x12\x08\n\x04\x46ILE\x10\x05\x12\n\n\x06\x43USTOM\x10\x06\x12\x0b\n\x07STORAGE\x10\x07\x12\n\n\x06SCHEMA\x10\x08\x42\x1e\n\x1aorg.finos.tracdap.metadataP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tracdap.metadata.object_id_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032org.finos.tracdap.metadataP\001'
  _OBJECTTYPE._serialized_start=637
  _OBJECTTYPE._serialized_end=761
  _TAGHEADER._serialized_start=84
  _TAGHEADER._serialized_end=319
  _TAGSELECTOR._serialized_start=322
  _TAGSELECTOR._serialized_end=635
# @@protoc_insertion_point(module_scope)
