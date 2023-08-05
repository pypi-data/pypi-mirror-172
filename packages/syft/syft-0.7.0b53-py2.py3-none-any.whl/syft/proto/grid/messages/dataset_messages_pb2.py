# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/grid/messages/dataset_messages.proto
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
    b'\n*proto/grid/messages/dataset_messages.proto\x12\x12syft.grid.messages\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"\xac\x02\n\x14\x43reateDatasetMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x0f\n\x07\x64\x61taset\x18\x03 \x01(\x0c\x12H\n\x08metadata\x18\x04 \x03(\x0b\x32\x36.syft.grid.messages.CreateDatasetMessage.MetadataEntry\x12\'\n\x08reply_to\x18\x05 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x10\n\x08platform\x18\x06 \x01(\t\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\x9f\x01\n\x11GetDatasetMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x12\n\ndataset_id\x18\x03 \x01(\x03\x12\'\n\x08reply_to\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address"\xdc\x01\n\x12GetDatasetResponse\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12\x46\n\x08metadata\x18\x02 \x03(\x0b\x32\x34.syft.grid.messages.GetDatasetResponse.MetadataEntry\x12&\n\x07\x61\x64\x64ress\x18\x03 \x01(\x0b\x32\x15.syft.core.io.Address\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\x8c\x01\n\x12GetDatasetsMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\'\n\x08reply_to\x18\x03 \x01(\x0b\x32\x15.syft.core.io.Address"\xd7\x02\n\x13GetDatasetsResponse\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12M\n\tmetadatas\x18\x02 \x03(\x0b\x32:.syft.grid.messages.GetDatasetsResponse.metadata_container\x12&\n\x07\x61\x64\x64ress\x18\x03 \x01(\x0b\x32\x15.syft.core.io.Address\x1a\xa1\x01\n\x12metadata_container\x12Z\n\x08metadata\x18\x01 \x03(\x0b\x32H.syft.grid.messages.GetDatasetsResponse.metadata_container.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x0c:\x02\x38\x01"\x9d\x02\n\x14UpdateDatasetMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x12\n\ndataset_id\x18\x03 \x01(\x03\x12H\n\x08metadata\x18\x04 \x03(\x0b\x32\x36.syft.grid.messages.UpdateDatasetMessage.MetadataEntry\x12\'\n\x08reply_to\x18\x05 \x01(\x0b\x32\x15.syft.core.io.Address\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xb9\x01\n\x14\x44\x65leteDatasetMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x12\n\ndataset_id\x18\x03 \x01(\t\x12\x15\n\rbin_object_id\x18\x04 \x01(\t\x12\'\n\x08reply_to\x18\x05 \x01(\x0b\x32\x15.syft.core.io.Addressb\x06proto3'
)


_CREATEDATASETMESSAGE = DESCRIPTOR.message_types_by_name["CreateDatasetMessage"]
_CREATEDATASETMESSAGE_METADATAENTRY = _CREATEDATASETMESSAGE.nested_types_by_name[
    "MetadataEntry"
]
_GETDATASETMESSAGE = DESCRIPTOR.message_types_by_name["GetDatasetMessage"]
_GETDATASETRESPONSE = DESCRIPTOR.message_types_by_name["GetDatasetResponse"]
_GETDATASETRESPONSE_METADATAENTRY = _GETDATASETRESPONSE.nested_types_by_name[
    "MetadataEntry"
]
_GETDATASETSMESSAGE = DESCRIPTOR.message_types_by_name["GetDatasetsMessage"]
_GETDATASETSRESPONSE = DESCRIPTOR.message_types_by_name["GetDatasetsResponse"]
_GETDATASETSRESPONSE_METADATA_CONTAINER = _GETDATASETSRESPONSE.nested_types_by_name[
    "metadata_container"
]
_GETDATASETSRESPONSE_METADATA_CONTAINER_METADATAENTRY = (
    _GETDATASETSRESPONSE_METADATA_CONTAINER.nested_types_by_name["MetadataEntry"]
)
_UPDATEDATASETMESSAGE = DESCRIPTOR.message_types_by_name["UpdateDatasetMessage"]
_UPDATEDATASETMESSAGE_METADATAENTRY = _UPDATEDATASETMESSAGE.nested_types_by_name[
    "MetadataEntry"
]
_DELETEDATASETMESSAGE = DESCRIPTOR.message_types_by_name["DeleteDatasetMessage"]
CreateDatasetMessage = _reflection.GeneratedProtocolMessageType(
    "CreateDatasetMessage",
    (_message.Message,),
    {
        "MetadataEntry": _reflection.GeneratedProtocolMessageType(
            "MetadataEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _CREATEDATASETMESSAGE_METADATAENTRY,
                "__module__": "proto.grid.messages.dataset_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.CreateDatasetMessage.MetadataEntry)
            },
        ),
        "DESCRIPTOR": _CREATEDATASETMESSAGE,
        "__module__": "proto.grid.messages.dataset_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.CreateDatasetMessage)
    },
)
_sym_db.RegisterMessage(CreateDatasetMessage)
_sym_db.RegisterMessage(CreateDatasetMessage.MetadataEntry)

GetDatasetMessage = _reflection.GeneratedProtocolMessageType(
    "GetDatasetMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETDATASETMESSAGE,
        "__module__": "proto.grid.messages.dataset_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetDatasetMessage)
    },
)
_sym_db.RegisterMessage(GetDatasetMessage)

GetDatasetResponse = _reflection.GeneratedProtocolMessageType(
    "GetDatasetResponse",
    (_message.Message,),
    {
        "MetadataEntry": _reflection.GeneratedProtocolMessageType(
            "MetadataEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _GETDATASETRESPONSE_METADATAENTRY,
                "__module__": "proto.grid.messages.dataset_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.GetDatasetResponse.MetadataEntry)
            },
        ),
        "DESCRIPTOR": _GETDATASETRESPONSE,
        "__module__": "proto.grid.messages.dataset_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetDatasetResponse)
    },
)
_sym_db.RegisterMessage(GetDatasetResponse)
_sym_db.RegisterMessage(GetDatasetResponse.MetadataEntry)

GetDatasetsMessage = _reflection.GeneratedProtocolMessageType(
    "GetDatasetsMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETDATASETSMESSAGE,
        "__module__": "proto.grid.messages.dataset_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetDatasetsMessage)
    },
)
_sym_db.RegisterMessage(GetDatasetsMessage)

GetDatasetsResponse = _reflection.GeneratedProtocolMessageType(
    "GetDatasetsResponse",
    (_message.Message,),
    {
        "metadata_container": _reflection.GeneratedProtocolMessageType(
            "metadata_container",
            (_message.Message,),
            {
                "MetadataEntry": _reflection.GeneratedProtocolMessageType(
                    "MetadataEntry",
                    (_message.Message,),
                    {
                        "DESCRIPTOR": _GETDATASETSRESPONSE_METADATA_CONTAINER_METADATAENTRY,
                        "__module__": "proto.grid.messages.dataset_messages_pb2"
                        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetDatasetsResponse.metadata_container.MetadataEntry)
                    },
                ),
                "DESCRIPTOR": _GETDATASETSRESPONSE_METADATA_CONTAINER,
                "__module__": "proto.grid.messages.dataset_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.GetDatasetsResponse.metadata_container)
            },
        ),
        "DESCRIPTOR": _GETDATASETSRESPONSE,
        "__module__": "proto.grid.messages.dataset_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetDatasetsResponse)
    },
)
_sym_db.RegisterMessage(GetDatasetsResponse)
_sym_db.RegisterMessage(GetDatasetsResponse.metadata_container)
_sym_db.RegisterMessage(GetDatasetsResponse.metadata_container.MetadataEntry)

UpdateDatasetMessage = _reflection.GeneratedProtocolMessageType(
    "UpdateDatasetMessage",
    (_message.Message,),
    {
        "MetadataEntry": _reflection.GeneratedProtocolMessageType(
            "MetadataEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _UPDATEDATASETMESSAGE_METADATAENTRY,
                "__module__": "proto.grid.messages.dataset_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.UpdateDatasetMessage.MetadataEntry)
            },
        ),
        "DESCRIPTOR": _UPDATEDATASETMESSAGE,
        "__module__": "proto.grid.messages.dataset_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.UpdateDatasetMessage)
    },
)
_sym_db.RegisterMessage(UpdateDatasetMessage)
_sym_db.RegisterMessage(UpdateDatasetMessage.MetadataEntry)

DeleteDatasetMessage = _reflection.GeneratedProtocolMessageType(
    "DeleteDatasetMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _DELETEDATASETMESSAGE,
        "__module__": "proto.grid.messages.dataset_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.DeleteDatasetMessage)
    },
)
_sym_db.RegisterMessage(DeleteDatasetMessage)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _CREATEDATASETMESSAGE_METADATAENTRY._options = None
    _CREATEDATASETMESSAGE_METADATAENTRY._serialized_options = b"8\001"
    _GETDATASETRESPONSE_METADATAENTRY._options = None
    _GETDATASETRESPONSE_METADATAENTRY._serialized_options = b"8\001"
    _GETDATASETSRESPONSE_METADATA_CONTAINER_METADATAENTRY._options = None
    _GETDATASETSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_options = b"8\001"
    _UPDATEDATASETMESSAGE_METADATAENTRY._options = None
    _UPDATEDATASETMESSAGE_METADATAENTRY._serialized_options = b"8\001"
    _CREATEDATASETMESSAGE._serialized_start = 135
    _CREATEDATASETMESSAGE._serialized_end = 435
    _CREATEDATASETMESSAGE_METADATAENTRY._serialized_start = 388
    _CREATEDATASETMESSAGE_METADATAENTRY._serialized_end = 435
    _GETDATASETMESSAGE._serialized_start = 438
    _GETDATASETMESSAGE._serialized_end = 597
    _GETDATASETRESPONSE._serialized_start = 600
    _GETDATASETRESPONSE._serialized_end = 820
    _GETDATASETRESPONSE_METADATAENTRY._serialized_start = 388
    _GETDATASETRESPONSE_METADATAENTRY._serialized_end = 435
    _GETDATASETSMESSAGE._serialized_start = 823
    _GETDATASETSMESSAGE._serialized_end = 963
    _GETDATASETSRESPONSE._serialized_start = 966
    _GETDATASETSRESPONSE._serialized_end = 1309
    _GETDATASETSRESPONSE_METADATA_CONTAINER._serialized_start = 1148
    _GETDATASETSRESPONSE_METADATA_CONTAINER._serialized_end = 1309
    _GETDATASETSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_start = 1262
    _GETDATASETSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_end = 1309
    _UPDATEDATASETMESSAGE._serialized_start = 1312
    _UPDATEDATASETMESSAGE._serialized_end = 1597
    _UPDATEDATASETMESSAGE_METADATAENTRY._serialized_start = 388
    _UPDATEDATASETMESSAGE_METADATAENTRY._serialized_end = 435
    _DELETEDATASETMESSAGE._serialized_start = 1600
    _DELETEDATASETMESSAGE._serialized_end = 1785
# @@protoc_insertion_point(module_scope)
