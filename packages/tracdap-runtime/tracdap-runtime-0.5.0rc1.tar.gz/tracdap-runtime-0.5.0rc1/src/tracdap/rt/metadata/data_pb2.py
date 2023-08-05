# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: tracdap/metadata/data.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from tracdap.metadata import type_pb2 as tracdap_dot_metadata_dot_type__pb2
from tracdap.metadata import object_id_pb2 as tracdap_dot_metadata_dot_object__id__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1btracdap/metadata/data.proto\x12\x10tracdap.metadata\x1a\x1btracdap/metadata/type.proto\x1a tracdap/metadata/object_id.proto\"\xc5\x01\n\x0b\x46ieldSchema\x12\x11\n\tfieldName\x18\x01 \x01(\t\x12\x12\n\nfieldOrder\x18\x02 \x01(\x11\x12.\n\tfieldType\x18\x03 \x01(\x0e\x32\x1b.tracdap.metadata.BasicType\x12\r\n\x05label\x18\x04 \x01(\t\x12\x13\n\x0b\x62usinessKey\x18\x05 \x01(\x08\x12\x13\n\x0b\x63\x61tegorical\x18\x06 \x01(\x08\x12\x17\n\nformatCode\x18\x07 \x01(\tH\x00\x88\x01\x01\x42\r\n\x0b_formatCode\"<\n\x0bTableSchema\x12-\n\x06\x66ields\x18\x01 \x03(\x0b\x32\x1d.tracdap.metadata.FieldSchema\"\xba\x01\n\x10SchemaDefinition\x12\x30\n\nschemaType\x18\x01 \x01(\x0e\x32\x1c.tracdap.metadata.SchemaType\x12,\n\x08partType\x18\x02 \x01(\x0e\x32\x1a.tracdap.metadata.PartType\x12.\n\x05table\x18\x03 \x01(\x0b\x32\x1d.tracdap.metadata.TableSchemaH\x00\x42\x16\n\x14schemaTypeDefinition\"\x81\x02\n\x07PartKey\x12\x11\n\topaqueKey\x18\x01 \x01(\t\x12,\n\x08partType\x18\x02 \x01(\x0e\x32\x1a.tracdap.metadata.PartType\x12+\n\npartValues\x18\x03 \x03(\x0b\x32\x17.tracdap.metadata.Value\x12\x32\n\x0cpartRangeMin\x18\x04 \x01(\x0b\x32\x17.tracdap.metadata.ValueH\x00\x88\x01\x01\x12\x32\n\x0cpartRangeMax\x18\x05 \x01(\x0b\x32\x17.tracdap.metadata.ValueH\x01\x88\x01\x01\x42\x0f\n\r_partRangeMinB\x0f\n\r_partRangeMax\"\xba\x04\n\x0e\x44\x61taDefinition\x12\x31\n\x08schemaId\x18\x01 \x01(\x0b\x32\x1d.tracdap.metadata.TagSelectorH\x00\x12\x34\n\x06schema\x18\x02 \x01(\x0b\x32\".tracdap.metadata.SchemaDefinitionH\x00\x12:\n\x05parts\x18\x03 \x03(\x0b\x32+.tracdap.metadata.DataDefinition.PartsEntry\x12\x30\n\tstorageId\x18\x04 \x01(\x0b\x32\x1d.tracdap.metadata.TagSelector\x1a-\n\x05\x44\x65lta\x12\x12\n\ndeltaIndex\x18\x01 \x01(\r\x12\x10\n\x08\x64\x61taItem\x18\x02 \x01(\t\x1aQ\n\x04Snap\x12\x11\n\tsnapIndex\x18\x01 \x01(\r\x12\x36\n\x06\x64\x65ltas\x18\x02 \x03(\x0b\x32&.tracdap.metadata.DataDefinition.Delta\x1ag\n\x04Part\x12*\n\x07partKey\x18\x01 \x01(\x0b\x32\x19.tracdap.metadata.PartKey\x12\x33\n\x04snap\x18\x02 \x01(\x0b\x32%.tracdap.metadata.DataDefinition.Snap\x1aS\n\nPartsEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\x34\n\x05value\x18\x02 \x01(\x0b\x32%.tracdap.metadata.DataDefinition.Part:\x02\x38\x01\x42\x11\n\x0fschemaSpecifier*0\n\nSchemaType\x12\x17\n\x13SCHEMA_TYPE_NOT_SET\x10\x00\x12\t\n\x05TABLE\x10\x01*?\n\x08PartType\x12\r\n\tPART_ROOT\x10\x00\x12\x11\n\rPART_BY_RANGE\x10\x01\x12\x11\n\rPART_BY_VALUE\x10\x02\x42\x1e\n\x1aorg.finos.tracdap.metadataP\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'tracdap.metadata.data_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\032org.finos.tracdap.metadataP\001'
  _DATADEFINITION_PARTSENTRY._options = None
  _DATADEFINITION_PARTSENTRY._serialized_options = b'8\001'
  _SCHEMATYPE._serialized_start=1396
  _SCHEMATYPE._serialized_end=1444
  _PARTTYPE._serialized_start=1446
  _PARTTYPE._serialized_end=1509
  _FIELDSCHEMA._serialized_start=113
  _FIELDSCHEMA._serialized_end=310
  _TABLESCHEMA._serialized_start=312
  _TABLESCHEMA._serialized_end=372
  _SCHEMADEFINITION._serialized_start=375
  _SCHEMADEFINITION._serialized_end=561
  _PARTKEY._serialized_start=564
  _PARTKEY._serialized_end=821
  _DATADEFINITION._serialized_start=824
  _DATADEFINITION._serialized_end=1394
  _DATADEFINITION_DELTA._serialized_start=1057
  _DATADEFINITION_DELTA._serialized_end=1102
  _DATADEFINITION_SNAP._serialized_start=1104
  _DATADEFINITION_SNAP._serialized_end=1185
  _DATADEFINITION_PART._serialized_start=1187
  _DATADEFINITION_PART._serialized_end=1290
  _DATADEFINITION_PARTSENTRY._serialized_start=1292
  _DATADEFINITION_PARTSENTRY._serialized_end=1375
# @@protoc_insertion_point(module_scope)
