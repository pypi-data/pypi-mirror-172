# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/node/common/service/heritage_update_service.proto
"""Generated protocol buffer code."""
# third party
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


# syft absolute
from syft.proto.core.common import (
    common_object_pb2 as proto_dot_core_dot_common_dot_common__object__pb2,
)
from syft.proto.core.io import address_pb2 as proto_dot_core_dot_io_dot_address__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n<proto/core/node/common/service/heritage_update_service.proto\x12\x1dsyft.core.node.common.service\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"\x9b\x01\n\x15HeritageUpdateMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x33\n\x14new_ancestry_address\x18\x03 \x01(\x0b\x32\x15.syft.core.io.Addressb\x06proto3'
)


_HERITAGEUPDATEMESSAGE = DESCRIPTOR.message_types_by_name["HeritageUpdateMessage"]
HeritageUpdateMessage = _reflection.GeneratedProtocolMessageType(
    "HeritageUpdateMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _HERITAGEUPDATEMESSAGE,
        "__module__": "proto.core.node.common.service.heritage_update_service_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.node.common.service.HeritageUpdateMessage)
    },
)
_sym_db.RegisterMessage(HeritageUpdateMessage)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _HERITAGEUPDATEMESSAGE._serialized_start = 164
    _HERITAGEUPDATEMESSAGE._serialized_end = 319
# @@protoc_insertion_point(module_scope)
