# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/grid/messages/association_messages.proto
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
    b'\n.proto/grid/messages/association_messages.proto\x12\x12syft.grid.messages\x1a%proto/core/common/common_object.proto\x1a\x1bproto/core/io/address.proto"\xbb\x02\n\x1dSendAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x0e\n\x06source\x18\x03 \x01(\t\x12\x0e\n\x06target\x18\x04 \x01(\t\x12\'\n\x08reply_to\x18\x05 \x01(\x0b\x32\x15.syft.core.io.Address\x12Q\n\x08metadata\x18\x06 \x03(\x0b\x32?.syft.grid.messages.SendAssociationRequestMessage.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xaa\x02\n ReceiveAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12T\n\x08metadata\x18\x03 \x03(\x0b\x32\x42.syft.grid.messages.ReceiveAssociationRequestMessage.MetadataEntry\x12\x10\n\x08response\x18\x04 \x01(\t\x12\x0e\n\x06source\x18\x05 \x01(\t\x12\x0e\n\x06target\x18\x06 \x01(\t\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xcc\x01\n RespondAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x10\n\x08response\x18\x03 \x01(\t\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x0e\n\x06target\x18\x05 \x01(\t\x12\'\n\x08reply_to\x18\x06 \x01(\x0b\x32\x15.syft.core.io.Address"\xae\x01\n\x1cGetAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x16\n\x0e\x61ssociation_id\x18\x03 \x01(\x05\x12\'\n\x08reply_to\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address"\x8f\x02\n\x1dGetAssociationRequestResponse\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12O\n\x07\x63ontent\x18\x02 \x03(\x0b\x32>.syft.grid.messages.GetAssociationRequestResponse.ContentEntry\x12&\n\x07\x61\x64\x64ress\x18\x03 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x0e\n\x06source\x18\x04 \x01(\t\x12\x0e\n\x06target\x18\x05 \x01(\t\x1a.\n\x0c\x43ontentEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\x97\x01\n\x1dGetAssociationRequestsMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\'\n\x08reply_to\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address"\xf6\x02\n\x1eGetAssociationRequestsResponse\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12V\n\x07\x63ontent\x18\x02 \x03(\x0b\x32\x45.syft.grid.messages.GetAssociationRequestsResponse.metadata_container\x12&\n\x07\x61\x64\x64ress\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Address\x1a\xac\x01\n\x12metadata_container\x12\x65\n\x08metadata\x18\x01 \x03(\x0b\x32S.syft.grid.messages.GetAssociationRequestsResponse.metadata_container.MetadataEntry\x1a/\n\rMetadataEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01"\xb1\x01\n\x1f\x44\x65leteAssociationRequestMessage\x12%\n\x06msg_id\x18\x01 \x01(\x0b\x32\x15.syft.core.common.UID\x12&\n\x07\x61\x64\x64ress\x18\x02 \x01(\x0b\x32\x15.syft.core.io.Address\x12\x16\n\x0e\x61ssociation_id\x18\x03 \x01(\x05\x12\'\n\x08reply_to\x18\x04 \x01(\x0b\x32\x15.syft.core.io.Addressb\x06proto3'
)


_SENDASSOCIATIONREQUESTMESSAGE = DESCRIPTOR.message_types_by_name[
    "SendAssociationRequestMessage"
]
_SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY = (
    _SENDASSOCIATIONREQUESTMESSAGE.nested_types_by_name["MetadataEntry"]
)
_RECEIVEASSOCIATIONREQUESTMESSAGE = DESCRIPTOR.message_types_by_name[
    "ReceiveAssociationRequestMessage"
]
_RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY = (
    _RECEIVEASSOCIATIONREQUESTMESSAGE.nested_types_by_name["MetadataEntry"]
)
_RESPONDASSOCIATIONREQUESTMESSAGE = DESCRIPTOR.message_types_by_name[
    "RespondAssociationRequestMessage"
]
_GETASSOCIATIONREQUESTMESSAGE = DESCRIPTOR.message_types_by_name[
    "GetAssociationRequestMessage"
]
_GETASSOCIATIONREQUESTRESPONSE = DESCRIPTOR.message_types_by_name[
    "GetAssociationRequestResponse"
]
_GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY = (
    _GETASSOCIATIONREQUESTRESPONSE.nested_types_by_name["ContentEntry"]
)
_GETASSOCIATIONREQUESTSMESSAGE = DESCRIPTOR.message_types_by_name[
    "GetAssociationRequestsMessage"
]
_GETASSOCIATIONREQUESTSRESPONSE = DESCRIPTOR.message_types_by_name[
    "GetAssociationRequestsResponse"
]
_GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER = (
    _GETASSOCIATIONREQUESTSRESPONSE.nested_types_by_name["metadata_container"]
)
_GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY = (
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER.nested_types_by_name[
        "MetadataEntry"
    ]
)
_DELETEASSOCIATIONREQUESTMESSAGE = DESCRIPTOR.message_types_by_name[
    "DeleteAssociationRequestMessage"
]
SendAssociationRequestMessage = _reflection.GeneratedProtocolMessageType(
    "SendAssociationRequestMessage",
    (_message.Message,),
    {
        "MetadataEntry": _reflection.GeneratedProtocolMessageType(
            "MetadataEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY,
                "__module__": "proto.grid.messages.association_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.SendAssociationRequestMessage.MetadataEntry)
            },
        ),
        "DESCRIPTOR": _SENDASSOCIATIONREQUESTMESSAGE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.SendAssociationRequestMessage)
    },
)
_sym_db.RegisterMessage(SendAssociationRequestMessage)
_sym_db.RegisterMessage(SendAssociationRequestMessage.MetadataEntry)

ReceiveAssociationRequestMessage = _reflection.GeneratedProtocolMessageType(
    "ReceiveAssociationRequestMessage",
    (_message.Message,),
    {
        "MetadataEntry": _reflection.GeneratedProtocolMessageType(
            "MetadataEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY,
                "__module__": "proto.grid.messages.association_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.ReceiveAssociationRequestMessage.MetadataEntry)
            },
        ),
        "DESCRIPTOR": _RECEIVEASSOCIATIONREQUESTMESSAGE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.ReceiveAssociationRequestMessage)
    },
)
_sym_db.RegisterMessage(ReceiveAssociationRequestMessage)
_sym_db.RegisterMessage(ReceiveAssociationRequestMessage.MetadataEntry)

RespondAssociationRequestMessage = _reflection.GeneratedProtocolMessageType(
    "RespondAssociationRequestMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _RESPONDASSOCIATIONREQUESTMESSAGE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.RespondAssociationRequestMessage)
    },
)
_sym_db.RegisterMessage(RespondAssociationRequestMessage)

GetAssociationRequestMessage = _reflection.GeneratedProtocolMessageType(
    "GetAssociationRequestMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETASSOCIATIONREQUESTMESSAGE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetAssociationRequestMessage)
    },
)
_sym_db.RegisterMessage(GetAssociationRequestMessage)

GetAssociationRequestResponse = _reflection.GeneratedProtocolMessageType(
    "GetAssociationRequestResponse",
    (_message.Message,),
    {
        "ContentEntry": _reflection.GeneratedProtocolMessageType(
            "ContentEntry",
            (_message.Message,),
            {
                "DESCRIPTOR": _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY,
                "__module__": "proto.grid.messages.association_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.GetAssociationRequestResponse.ContentEntry)
            },
        ),
        "DESCRIPTOR": _GETASSOCIATIONREQUESTRESPONSE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetAssociationRequestResponse)
    },
)
_sym_db.RegisterMessage(GetAssociationRequestResponse)
_sym_db.RegisterMessage(GetAssociationRequestResponse.ContentEntry)

GetAssociationRequestsMessage = _reflection.GeneratedProtocolMessageType(
    "GetAssociationRequestsMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _GETASSOCIATIONREQUESTSMESSAGE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetAssociationRequestsMessage)
    },
)
_sym_db.RegisterMessage(GetAssociationRequestsMessage)

GetAssociationRequestsResponse = _reflection.GeneratedProtocolMessageType(
    "GetAssociationRequestsResponse",
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
                        "DESCRIPTOR": _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY,
                        "__module__": "proto.grid.messages.association_messages_pb2"
                        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetAssociationRequestsResponse.metadata_container.MetadataEntry)
                    },
                ),
                "DESCRIPTOR": _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER,
                "__module__": "proto.grid.messages.association_messages_pb2"
                # @@protoc_insertion_point(class_scope:syft.grid.messages.GetAssociationRequestsResponse.metadata_container)
            },
        ),
        "DESCRIPTOR": _GETASSOCIATIONREQUESTSRESPONSE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.GetAssociationRequestsResponse)
    },
)
_sym_db.RegisterMessage(GetAssociationRequestsResponse)
_sym_db.RegisterMessage(GetAssociationRequestsResponse.metadata_container)
_sym_db.RegisterMessage(GetAssociationRequestsResponse.metadata_container.MetadataEntry)

DeleteAssociationRequestMessage = _reflection.GeneratedProtocolMessageType(
    "DeleteAssociationRequestMessage",
    (_message.Message,),
    {
        "DESCRIPTOR": _DELETEASSOCIATIONREQUESTMESSAGE,
        "__module__": "proto.grid.messages.association_messages_pb2"
        # @@protoc_insertion_point(class_scope:syft.grid.messages.DeleteAssociationRequestMessage)
    },
)
_sym_db.RegisterMessage(DeleteAssociationRequestMessage)

if _descriptor._USE_C_DESCRIPTORS == False:

    DESCRIPTOR._options = None
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._options = None
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_options = b"8\001"
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._options = None
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_options = b"8\001"
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._options = None
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._serialized_options = b"8\001"
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._options = None
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_options = (
        b"8\001"
    )
    _SENDASSOCIATIONREQUESTMESSAGE._serialized_start = 139
    _SENDASSOCIATIONREQUESTMESSAGE._serialized_end = 454
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_start = 407
    _SENDASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_end = 454
    _RECEIVEASSOCIATIONREQUESTMESSAGE._serialized_start = 457
    _RECEIVEASSOCIATIONREQUESTMESSAGE._serialized_end = 755
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_start = 407
    _RECEIVEASSOCIATIONREQUESTMESSAGE_METADATAENTRY._serialized_end = 454
    _RESPONDASSOCIATIONREQUESTMESSAGE._serialized_start = 758
    _RESPONDASSOCIATIONREQUESTMESSAGE._serialized_end = 962
    _GETASSOCIATIONREQUESTMESSAGE._serialized_start = 965
    _GETASSOCIATIONREQUESTMESSAGE._serialized_end = 1139
    _GETASSOCIATIONREQUESTRESPONSE._serialized_start = 1142
    _GETASSOCIATIONREQUESTRESPONSE._serialized_end = 1413
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._serialized_start = 1367
    _GETASSOCIATIONREQUESTRESPONSE_CONTENTENTRY._serialized_end = 1413
    _GETASSOCIATIONREQUESTSMESSAGE._serialized_start = 1416
    _GETASSOCIATIONREQUESTSMESSAGE._serialized_end = 1567
    _GETASSOCIATIONREQUESTSRESPONSE._serialized_start = 1570
    _GETASSOCIATIONREQUESTSRESPONSE._serialized_end = 1944
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER._serialized_start = 1772
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER._serialized_end = 1944
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_start = (
        407
    )
    _GETASSOCIATIONREQUESTSRESPONSE_METADATA_CONTAINER_METADATAENTRY._serialized_end = (
        454
    )
    _DELETEASSOCIATIONREQUESTMESSAGE._serialized_start = 1947
    _DELETEASSOCIATIONREQUESTMESSAGE._serialized_end = 2124
# @@protoc_insertion_point(module_scope)
