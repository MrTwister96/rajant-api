# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: Image.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from . import ModelDatabase_pb2 as ModelDatabase__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0bImage.proto\x12\x0frajant.bc.proto\x1a\x13ModelDatabase.proto\"\xd9\x04\n\x18\x42readCrumbImageContainer\x12H\n\x05image\x18\x01 \x03(\x0b\x32\x39.rajant.bc.proto.BreadCrumbImageContainer.BreadCrumbImage\x1a\x8d\x03\n\x0f\x42readCrumbImage\x12\x10\n\x08\x66ilename\x18\x01 \x01(\t\x12\x10\n\x08\x66ullpath\x18\x02 \x01(\t\x12\x18\n\x07version\x18\x03 \x01(\t:\x07unknown\x12\r\n\x05model\x18\x04 \x01(\t\x12\x0b\n\x03md5\x18\x05 \x01(\t\x12\x0c\n\x04size\x18\x06 \x01(\x04\x12\x0e\n\x06offset\x18\x07 \x01(\x04\x12\x12\n\nbuild_user\x18\t \x01(\t\x12\x16\n\x0e\x62uild_hostinfo\x18\n \x01(\t\x12\x12\n\nbuild_when\x18\x0b \x01(\t\x12\x14\n\x0c\x62uild_number\x18\x0c \x01(\t\x12I\n\nv10factory\x18\x0e \x03(\x0b\x32\x35.rajant.bc.proto.BreadCrumbImageContainer.FactoryBlob\x12\x19\n\x11\x62uild_description\x18\x0f \x01(\t\x12\x46\n\x07modeldb\x18\x10 \x01(\x0b\x32\x35.rajant.bc.proto.BreadCrumbImageContainer.ModelDbInfo\x1a\x38\n\x0bModelDbInfo\x12\x0e\n\x06offset\x18\x01 \x01(\x04\x12\x0c\n\x04size\x18\x02 \x01(\x04\x12\x0b\n\x03md5\x18\x03 \x01(\t\x1a)\n\x0b\x46\x61\x63toryBlob\x12\x0c\n\x04name\x18\x01 \x01(\t\x12\x0c\n\x04\x62lob\x18\x02 \x01(\x0c\x42\x31\n\x17\x63om.rajant.bcapi.protosB\x0bImageProtosH\x02Z\x07\x62\x63proto')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'Image_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\027com.rajant.bcapi.protosB\013ImageProtosH\002Z\007bcproto'
  _globals['_BREADCRUMBIMAGECONTAINER']._serialized_start=54
  _globals['_BREADCRUMBIMAGECONTAINER']._serialized_end=655
  _globals['_BREADCRUMBIMAGECONTAINER_BREADCRUMBIMAGE']._serialized_start=157
  _globals['_BREADCRUMBIMAGECONTAINER_BREADCRUMBIMAGE']._serialized_end=554
  _globals['_BREADCRUMBIMAGECONTAINER_MODELDBINFO']._serialized_start=556
  _globals['_BREADCRUMBIMAGECONTAINER_MODELDBINFO']._serialized_end=612
  _globals['_BREADCRUMBIMAGECONTAINER_FACTORYBLOB']._serialized_start=614
  _globals['_BREADCRUMBIMAGECONTAINER_FACTORYBLOB']._serialized_end=655
# @@protoc_insertion_point(module_scope)
