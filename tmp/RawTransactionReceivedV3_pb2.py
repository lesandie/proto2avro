# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: RawTransactionReceivedV3.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2
import Decimal_pb2 as Decimal__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='RawTransactionReceivedV3.proto',
  package='',
  syntax='proto3',
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\x1eRawTransactionReceivedV3.proto\x1a\x1fgoogle/protobuf/timestamp.proto\x1a\rDecimal.proto\"\x84\x05\n\x18RawTransactionReceivedV3\x12\x13\n\x0binternal_id\x18\x01 \x01(\t\x12\x13\n\x0b\x65xternal_id\x18\x02 \x01(\t\x12\x1c\n\x14transaction_provider\x18\x03 \x01(\t\x12\x0f\n\x07\x61\x63\x63ount\x18\x04 \x01(\t\x12\x18\n\x06\x61mount\x18\x05 \x01(\x0b\x32\x08.Decimal\x12\x10\n\x08\x63urrency\x18\x06 \x01(\t\x12&\n\x02ts\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x12\x11\n\tfinalized\x18\x08 \x01(\x08\x12\x16\n\treference\x18\t \x01(\tH\x00\x88\x01\x01\x12\x1a\n\rmerchant_name\x18\n \x01(\tH\x01\x88\x01\x01\x12\x18\n\x0bmerchant_id\x18\x0b \x01(\tH\x02\x88\x01\x01\x12#\n\x16merchant_category_code\x18\x0c \x01(\tH\x03\x88\x01\x01\x12\x1a\n\rmerchant_city\x18\r \x01(\tH\x04\x88\x01\x01\x12\x1d\n\x10merchant_address\x18\x0e \x01(\tH\x05\x88\x01\x01\x12\x1d\n\x10merchant_country\x18\x0f \x01(\tH\x06\x88\x01\x01\x12\x18\n\x0bterminal_id\x18\x10 \x01(\tH\x07\x88\x01\x01\x12\x19\n\x0copenapi_bank\x18\x11 \x01(\tH\x08\x88\x01\x01\x42\x0c\n\n_referenceB\x10\n\x0e_merchant_nameB\x0e\n\x0c_merchant_idB\x19\n\x17_merchant_category_codeB\x10\n\x0e_merchant_cityB\x13\n\x11_merchant_addressB\x13\n\x11_merchant_countryB\x0e\n\x0c_terminal_idB\x0f\n\r_openapi_bankb\x06proto3'
  ,
  dependencies=[google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,Decimal__pb2.DESCRIPTOR,])




_RAWTRANSACTIONRECEIVEDV3 = _descriptor.Descriptor(
  name='RawTransactionReceivedV3',
  full_name='RawTransactionReceivedV3',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='internal_id', full_name='RawTransactionReceivedV3.internal_id', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='external_id', full_name='RawTransactionReceivedV3.external_id', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='transaction_provider', full_name='RawTransactionReceivedV3.transaction_provider', index=2,
      number=3, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='account', full_name='RawTransactionReceivedV3.account', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='amount', full_name='RawTransactionReceivedV3.amount', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='currency', full_name='RawTransactionReceivedV3.currency', index=5,
      number=6, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='ts', full_name='RawTransactionReceivedV3.ts', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='finalized', full_name='RawTransactionReceivedV3.finalized', index=7,
      number=8, type=8, cpp_type=7, label=1,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='reference', full_name='RawTransactionReceivedV3.reference', index=8,
      number=9, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='merchant_name', full_name='RawTransactionReceivedV3.merchant_name', index=9,
      number=10, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='merchant_id', full_name='RawTransactionReceivedV3.merchant_id', index=10,
      number=11, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='merchant_category_code', full_name='RawTransactionReceivedV3.merchant_category_code', index=11,
      number=12, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='merchant_city', full_name='RawTransactionReceivedV3.merchant_city', index=12,
      number=13, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='merchant_address', full_name='RawTransactionReceivedV3.merchant_address', index=13,
      number=14, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='merchant_country', full_name='RawTransactionReceivedV3.merchant_country', index=14,
      number=15, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='terminal_id', full_name='RawTransactionReceivedV3.terminal_id', index=15,
      number=16, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='openapi_bank', full_name='RawTransactionReceivedV3.openapi_bank', index=16,
      number=17, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
    _descriptor.OneofDescriptor(
      name='_reference', full_name='RawTransactionReceivedV3._reference',
      index=0, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_merchant_name', full_name='RawTransactionReceivedV3._merchant_name',
      index=1, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_merchant_id', full_name='RawTransactionReceivedV3._merchant_id',
      index=2, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_merchant_category_code', full_name='RawTransactionReceivedV3._merchant_category_code',
      index=3, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_merchant_city', full_name='RawTransactionReceivedV3._merchant_city',
      index=4, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_merchant_address', full_name='RawTransactionReceivedV3._merchant_address',
      index=5, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_merchant_country', full_name='RawTransactionReceivedV3._merchant_country',
      index=6, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_terminal_id', full_name='RawTransactionReceivedV3._terminal_id',
      index=7, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
    _descriptor.OneofDescriptor(
      name='_openapi_bank', full_name='RawTransactionReceivedV3._openapi_bank',
      index=8, containing_type=None,
      create_key=_descriptor._internal_create_key,
    fields=[]),
  ],
  serialized_start=83,
  serialized_end=727,
)

_RAWTRANSACTIONRECEIVEDV3.fields_by_name['amount'].message_type = Decimal__pb2._DECIMAL
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['ts'].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_reference'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['reference'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['reference'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_reference']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_name'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_name'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_name'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_name']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_id'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_id'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_id'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_id']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_category_code'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_category_code'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_category_code'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_category_code']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_city'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_city'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_city'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_city']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_address'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_address'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_address'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_address']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_country'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_country'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['merchant_country'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_merchant_country']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_terminal_id'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['terminal_id'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['terminal_id'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_terminal_id']
_RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_openapi_bank'].fields.append(
  _RAWTRANSACTIONRECEIVEDV3.fields_by_name['openapi_bank'])
_RAWTRANSACTIONRECEIVEDV3.fields_by_name['openapi_bank'].containing_oneof = _RAWTRANSACTIONRECEIVEDV3.oneofs_by_name['_openapi_bank']
DESCRIPTOR.message_types_by_name['RawTransactionReceivedV3'] = _RAWTRANSACTIONRECEIVEDV3
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

RawTransactionReceivedV3 = _reflection.GeneratedProtocolMessageType('RawTransactionReceivedV3', (_message.Message,), {
  'DESCRIPTOR' : _RAWTRANSACTIONRECEIVEDV3,
  '__module__' : 'RawTransactionReceivedV3_pb2'
  # @@protoc_insertion_point(class_scope:RawTransactionReceivedV3)
  })
_sym_db.RegisterMessage(RawTransactionReceivedV3)


# @@protoc_insertion_point(module_scope)
