# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/core/tensor/tensor.proto
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
from syft.proto.lib.numpy import array_pb2 as proto_dot_lib_dot_numpy_dot_array__pb2

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1eproto/core/tensor/tensor.proto\x12\x10syft.core.tensor\x1a\x1bproto/lib/numpy/array.proto"\x9d\x01\n\x06Tensor\x12\x10\n\x08obj_type\x18\x02 \x01(\t\x12\x13\n\x0buse_tensors\x18\x04 \x01(\x08\x12*\n\x06\x61rrays\x18\x05 \x03(\x0b\x32\x1a.syft.lib.numpy.NumpyProto\x12)\n\x07tensors\x18\x06 \x03(\x0b\x32\x18.syft.core.tensor.Tensor\x12\x15\n\rrequires_grad\x18\x07 \x01(\x08\x62\x06proto3'
)


_TENSOR = DESCRIPTOR.message_types_by_name["Tensor"]
Tensor = _reflection.GeneratedProtocolMessageType(
    "Tensor",
    (_message.Message,),
    {
        "DESCRIPTOR": _TENSOR,
        "__module__": "proto.core.tensor.tensor_pb2"
        # @@protoc_insertion_point(class_scope:syft.core.tensor.Tensor)
    },
)
_sym_db.RegisterMessage(Tensor)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _TENSOR._serialized_start = 82
    _TENSOR._serialized_end = 239
# @@protoc_insertion_point(module_scope)
