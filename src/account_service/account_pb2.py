# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: account.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'account.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\raccount.proto\x12\x07\x61\x63\x63ount\"V\n\x07\x41\x63\x63ount\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\x12\x11\n\thighScore\x18\x03 \x01(\x05\x12\x14\n\x0c\x61\x63\x63ount_type\x18\x04 \x01(\t\"\x07\n\x05\x45mpty2u\n\x0e\x41\x63\x63ountService\x12\x31\n\rCreateAccount\x12\x10.account.Account\x1a\x0e.account.Empty\x12\x30\n\nGetAccount\x12\x10.account.Account\x1a\x10.account.Accountb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'account_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_ACCOUNT']._serialized_start=26
  _globals['_ACCOUNT']._serialized_end=112
  _globals['_EMPTY']._serialized_start=114
  _globals['_EMPTY']._serialized_end=121
  _globals['_ACCOUNTSERVICE']._serialized_start=123
  _globals['_ACCOUNTSERVICE']._serialized_end=240
# @@protoc_insertion_point(module_scope)
